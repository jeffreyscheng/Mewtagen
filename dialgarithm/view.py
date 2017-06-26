class Prompt:
    @staticmethod
    def prompt(message, condition=lambda x: True):
        while True:
            user_input = input(message)
            if condition(user_input):
                return user_input


class Message:
    @staticmethod
    def message(message):
        print(message)
