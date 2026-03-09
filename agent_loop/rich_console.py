from rich.console import Console


class RichConsole:
    def __init__(self):
        self.console = Console()

    def show(self, text):
        try:
            self.console.print(text)
        except Exception:
            print(text)
