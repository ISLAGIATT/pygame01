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
        self.dialogue_index = 0
        self.dialogue_instance = Dialogue()

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def advance_dialogue(self):
        self.dialogue_index += 1  # Correct use of self to reference instance attribute
        if self.dialogue_index >= len(self.dialogue):
            self.dialogue_index = -1

class Book01(InteractiveObject):
    open_dialogue = ["the book opens with a creak. you find a newly cut brass key inside and pocket it."]
    book_dialogue = ["...",
                      "an old book.",
                      "the pages are stiff and sharp. they has seen very little use.",
                      "the pages of this closed book aren't sitting quite flush."]

    def __init__(self, dialogue, options, position, book_button):
        super().__init__(dialogue, options, position)
        self.book_button = book_button
        self.dialogue_instance = Dialogue()
        self.is_book_open = False
        self.key_obtained = False
        self.open_dialogues = ["The book opens with a creak. You find a newly cut brass key inside and pocket it.",
                               "The pages point skyward, waiting for a reader that will never come."]
        self.open_dialogue_index = -1  # Start before the first dialogue


    def handle_click(self, mouse_pos, button):
        # Toggle book dialogue visibility with left-click on the book button (outside dropdown visibility)
        if button == 1 and self.book_button.is_over(mouse_pos):
            if self.is_visible:
                # Check if key has been obtained for dialogue cycling logic
                if self.key_obtained:
                    # If the key is obtained, prevent accessing the last dialogue
                    # Cycle through to the third item only
                    if self.dialogue_index < 2:  # Adjust if your dialogues have different indices
                        self.dialogue_index += 1
                    else:
                        self.dialogue_index = 0  # Loop back after the third item
                else:
                    # Key not obtained, cycle through all but the last dialogue
                    if self.dialogue_index < len(self.book_dialogue) - 1:
                        self.dialogue_index += 1
                    else:
                        self.dialogue_index = 0  # Loop back to the start

                # Update the dialogue based on the new index
                self.dialogue = [self.book_dialogue[self.dialogue_index]]
            if self.is_book_open:
                self.advance_dialogue()
            else:
                self.is_visible = not self.is_visible  # Just toggle visibility if the book isn't opened yet

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            # Assuming draw_dialogue method of Dialogue instance is correctly implemented to handle text display
            self.dialogue_instance.draw_dialogue(
                text=self.dialogue[0],  # Here, self.dialogue is always a list with at least one item
                color=(204, 0, 204),
                pos=(200, 200))

    def open(self):
        self.open_dialogue_index += 1
        if self.open_dialogue_index >= len(self.open_dialogues):
            self.open_dialogue_index = 0
        self.dialogue = [self.open_dialogues[self.open_dialogue_index]]
        self.is_visible = True
        if not self.key_obtained:
            self.key_obtained = True
            self.is_book_open = False
        print("open")

    def close(self):
        print("close")

    def listen(self):
        print("listen")

    def push(self):
        print("push")