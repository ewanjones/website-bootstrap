class BaseScreen():
    def __init__(self):
        self.text = ""

    def handle_choice(self, state):
        input(self.text)
        return state