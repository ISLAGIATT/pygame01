import pygame
from dialogue import Dialogue
from dropdown import DropdownMenu

class InteractiveObject:
    def __init__(self, dialogue, options, position, size=(100, 30)):
        self.dialogue = dialogue
        self.options = options
        self.position = position
        self.size = size
        self.is_visible = False
        self.dialogue_index = -1
        self.dialogue_instance = Dialogue()

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def advance_dialogue(self):
        self.dialogue_index += 1  # Correct use of self to reference instance attribute
        if self.dialogue_index >= len(self.dialogue):
            self.dialogue_index = -1

    def select_option(self, selected_option):
        # Placeholder for option selection logic
        print(f"Selected option: {selected_option}")

class Book01(InteractiveObject):

    book_dialogue = ["...",
                      "an old book.",
                      "the pages are stiff and sharp. it has seen very little use.",
                      "the pages of this closed book aren't sitting quite flush."]

    def __init__(self, dialogue, options, position, book_button):
        super().__init__(dialogue, options, position)
        self.book_button = book_button
        self.dialogue_instance = Dialogue()

    def execute_option(self, selected_option):
        print(f"Executing option: {selected_option}")  # Confirm the option being executed
        if selected_option:
            action = getattr(self, selected_option, None)
            if callable(action):
                action()
            else:
                print(f"No action found for: {selected_option}")  # Log if no matching action is found

    def handle_click(self, mouse_pos, button):
        # Toggle book dialogue visibility with left-click on the book button (outside dropdown visibility)

        if button == 1 and self.book_button.is_over(mouse_pos):
            self.is_visible = not self.is_visible
            # Optionally, advance dialogue or perform other actions when the book is clicked and dropdown is not visible
            if self.is_visible:
                # Assuming you want to start or advance dialogue here
                self.dialogue_instance.advance_dialogue(self.book_dialogue, None)



    def open(self):
        print("open")

    def close(self):
        print("close")

    def listen(self):
        print("listen")

    def push(self):
        print("push")
