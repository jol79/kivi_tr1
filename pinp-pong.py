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

    # sets random x, y vel. for ball, and also resets the pos:
    def serve_ball(self):
        self.ball.center = self.center
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))

    def update(self, dt):
        # call ball.move and other stuff ...
        self.ball.move()

        # bounce off top and bottom:
        if (self.ball.y < 0) or (self.ball.top > self.height):
            # go in the back way:
            self.ball.velocity_y *= -1

        # bounce off the left and right:
        if (self.ball.x < 0) or (self.ball.right > self.width):
            # go in the back way:
            self.ball.velocity_x *= -1


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


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()

        # move method of our ball to be called regularly:
        Clock.schedule_interval(game.update, 1.0/60.0)

        return game


if __name__ == "__main__":
    PongApp().run()

