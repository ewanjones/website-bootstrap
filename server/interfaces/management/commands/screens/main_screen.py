from .base_screen import BaseScreen
from .db_screeen import DBScreen
from .csv_screen import CSVScreen

class MainScreen(BaseScreen):
    def __init__(self):
        super().__init__()
        self.text = """
Please choose an option:
1. Generate data for database.
2. Generate data for CSV
3. Exit
"""

    def handle_choice(self):
        result = -1
        while(result == -1):
            result = int(input(self.text) or -1)
            if result == 1:
                DBScreen().handle_choice()
            elif result == 2:
                CSVScreen().handle_choice()
            elif result == 3:
                break
            else:
                continue