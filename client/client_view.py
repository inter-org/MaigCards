from __future__ import print_function, unicode_literals
from pyfiglet import Figlet
from PyInquirer import prompt
from pprint import pprint

class View:
    def __init__(self):
        pass

    def welcome(self, welcome_msg):
        f = Figlet(font="slant", width=200)
        print(f.renderText(welcome_msg))

    def show_menu(self):
        questions = [
            {
                'type': 'list',
                'name': 'menu',
                'message': 'What do you want to do?',
                'choices': [
                    'Init a game',
                    'Find an existing game'
                ]
            }
        ]
        answers = prompt(questions)
        pprint(answers)




if __name__ == "__main__":
    view = View()
    view.welcome("Welcome 2 MagiCards")
    view.show_menu()