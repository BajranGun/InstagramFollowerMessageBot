from MainWindow import MainWindow

class InstaBot():
    def __init__(self):
        self.main_window = MainWindow()
        
    
    def run(self):
        self.main_window.run()

instaBot = InstaBot()
instaBot.run()