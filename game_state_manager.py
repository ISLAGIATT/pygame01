class GameStateManager:
    def __init__(self):
        self.current_open_dropdown = None
        self.book01_key_obtained = False
        self.door01_unlocked = False

    def open_dropdown(self, dropdown):
        if self.current_open_dropdown and self.current_open_dropdown != dropdown:
            self.current_open_dropdown.close()
        self.current_open_dropdown = dropdown
        dropdown.is_visible = True  # Make the dropdown visible

    def close_dropdown(self, dropdown):
        if self.current_open_dropdown:
            self.current_open_dropdown.close()
            self.current_open_dropdown = None

    def pick_up_key01(self):
        self.book01_key_obtained = True

    def is_key01_obtained(self):
        return self.book01_key_obtained

    def door01_unlocked(self):
        self.door01_unlocked = True
        print('door unlocked')
