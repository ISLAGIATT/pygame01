class GameStateManager:
    def __init__(self):
        self.current_open_dropdown = None
        self.book01_key_obtained = False
        self.door01_unlocked = False
        self.current_active_dialogue = None  # Track the currently active dialogue object

    def show_dialogue(self, new_dialogue_object):
        if self.current_active_dialogue and self.current_active_dialogue != new_dialogue_object:
            self.current_active_dialogue.hide_dialogue()  # Hide the current active dialogue
        self.current_active_dialogue = new_dialogue_object
        new_dialogue_object.show_dialogue()  # Show the new dialogue and make it active

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
