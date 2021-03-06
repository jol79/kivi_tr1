from random import randint

from kivy.app import App
from kivy.clock import Clock
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.vector import Vector


# table:
class PongGame(Widget):
    ###
    # helps to hook up to the widget created in kv rule,
    # because at that moment we don't have a reference to
    # the PongBall child widget
    ###
    ball = ObjectProperty(None)
    player_1 = ObjectProperty(None)
    player_2 = ObjectProperty(None)

    # sets random x, y vel. for ball, and also resets the pos:
    def serve_ball(self, vel=(4, 0)):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        # call ball.move and other stuff ...
        self.ball.move()

        # bounce of paddles:
        self.player_1.bounce_ball(self.ball)
        self.player_2.bounce_ball(self.ball)

        # bounce off top and bottom:
        if (self.ball.y < self.y) or (self.ball.top > self.top):
            # go in the back way:
            self.ball.velocity_y *= -1
            # self.player_1.score += 1
            # self.player_2.score += 1

        # # bounce off the left and right:
        # if (self.ball.x < 0) or (self.ball.right > self.width):
        #     # go in the back way:
        #     self.ball.velocity_x *= -1

        ###
        # - Aim: check if ball crossed defined lines on the left and right sides
        # - Requirements:
        #   1) if ball crossed left window line:
        #       player_1.score += 1
        #   2) if ball crossed right window line:
        #       player_2.score += 1
        ###
        if self.ball.x < self.width:
            self.player_2.score += 1
            ###
            # when ball bounced from the racket of the
            # player_2 it velocity must be bounced back
            # with velocity = (4, 0)
            ###
            self.serve_ball(vel=(4, 0))
        if self.ball.x > self.width:
            self.player_1.score += 1
            self.serve_ball(vel=(-4, 0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player_1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player_2.center_y = touch.y


# ball:
class PongBall(Widget):

    # velocity of the ball on x and y axis:
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    ###
    # reference list pr. so we can us ball.velocity as
    # a shorthand, just like e.g. w.pos for w.x and w.y
    ###
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongPaddle(Widget):
    # start score = 0, for each player
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            # check ball position
            vx, vy, = ball.velocity

            # outside of the racket zone:
            offset = (ball.center_y - self.center_y) / (
                self.height / 2
            )

            # bounce from the racket:
            bounced = Vector(-1 * vx,  vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()

        # move method of our ball to be called regularly:
        Clock.schedule_interval(game.update, 1.0/60.0)

        return game


if __name__ == "__main__":
    PongApp().run()

