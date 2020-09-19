import kivy as kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput


class LoginScreen(GridLayout):

    ###
    # overriding init method to add widgets and to
    # define their behavior:
    ###
    def __init__(self, **kwargs):

        ###
        # method "super" in order to implement the
        # functionality of the orig class overloaded
        ###
        super(LoginScreen, self).__init__(**kwargs)

        self.cols = 2
        self.add_widget(Label(text="Username"))
        self.username = TextInput(multiline=False)
        self.add_widget(self.username)
        self.add_widget(Label(text="Password"))
        self.password = TextInput(password=True, multiline=False)
        self.add_widget(self.password)


###
# to change name of the app you need to refactor
# name of the this main class:
###
class PingPong(App):

    def build(self):
        return LoginScreen()


if __name__ == '__main__':
    PingPong().run()
