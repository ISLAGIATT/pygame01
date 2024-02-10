from dialogue import Dialogue

class InteractiveObject:
    def __init__(self, dialogue, position, game_state_manager, size=(100, 30)):
        self.dialogue = dialogue
        self.position = position
        self.size = size
        self.is_visible = False
        self.book01_key_obtained = False
        self.dialogue_index = 0
        self.dialogue_instance = Dialogue()
        self.game_state_manager = game_state_manager
        self.current_dialogue_rect = None

    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def advance_dialogue(self):
        self.dialogue_index += 1  # Correct use of self to reference instance attribute
        if self.dialogue_index >= len(self.dialogue):
            self.dialogue_index = -1

class Book01(InteractiveObject):
    open_dialogue = ["the book opens with a creak. you find a newly cut brass key inside and pocket it."]
    book_dialogue = ["...", "an old book.", "the pages are stiff and sharp. they has seen very little use.",
                     "the pages of this closed book aren't sitting quite flush."]

    def __init__(self, dialogue, position, book_button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.book_button = book_button
        self.dialogue_instance = Dialogue()
        self.is_book_open = False

        self.open_dialogues = ["The book opens with a creak. You find a newly cut brass key inside and pocket it.",
                               "The pages point skyward, waiting for a reader that will never come."]
        self.open_dialogue_index = -1  # Start before the first dialogue

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.book_button.is_over(mouse_pos):
            if self.is_visible:
                # Check if key has been obtained for dialogue cycling logic
                if self.game_state_manager.book01_key_obtained:
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
        print(f"key obtained: {self.game_state_manager.book01_key_obtained}")

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            # Assuming draw_dialogue method of Dialogue instance is correctly implemented to handle text display
            self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                text=self.dialogue[0],  # Here, self.dialogue is always a list with at least one item
                color=(204, 0, 204),
                pos=(200, 200))

    def open(self):
        self.dialogue = [self.open_dialogues[0]]
        self.is_visible = True
        if self.game_state_manager.book01_key_obtained:
            self.dialogue = [self.open_dialogues[1]]
        if not self.game_state_manager.book01_key_obtained:
            self.game_state_manager.pick_up_key01()
            self.is_book_open = False
        print("open")

    def close(self):
        print("close")

    def listen(self):
        print("listen")

    def push(self):
        print("push")

class Door01(InteractiveObject):
    open_dialogue = ["you reach for the doorknob, and just above it you find a deadbolt with the keyhole facing you.",
                     "the deadbolt disengages with a satisfying yet somewhat off-putting 'THUNK'",
                     "the door is ajar. cold, damp air creeps in through the opening."]
    exam_dialogue = ["...", "a substantial looking door.",
                     "it looks like its been scratched at, but the marks aren't low enough to be from an animal.",
                     "you push your shoulder into it, but there is no give."]

    def __init__(self, dialogue, position, button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.door_button = button
        self.dialogue_instance = Dialogue()
        self.door_unlocked = False
        self.door_opened = False
        self.open_dialogue_index = 0

    def handle_click(self, mouse_pos, button):
        if self.is_visible and self.current_dialogue_rect and self.current_dialogue_rect.collidepoint(mouse_pos):
            self.advance_dialogue()
        # Toggle book dialogue visibility with left-click on the book button (outside dropdown visibility)
        if button == 1 and self.door_button.is_over(mouse_pos):
            if self.is_visible:
                if self.door_opened:
                    if self.dialogue_index < len(self.exam_dialogue) - 2:
                        self.dialogue_index += 1
                        self.is_visible = not self.is_visible
                    else:
                        self.dialogue_index = 0
                        self.is_visible = not self.is_visible
                elif self.dialogue_index < len(self.exam_dialogue) - 2:
                    self.dialogue_index += 1
                    self.is_visible = not self.is_visible
                else:
                    self.dialogue_index = -1  # Loop back to the start
                    self.is_visible = not self.is_visible
            else:
                self.is_visible = not self.is_visible
            self.dialogue = [self.exam_dialogue[self.dialogue_index]]
        print(f"door open: {self.door_opened}")

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            # Assuming draw_dialogue method of Dialogue instance is correctly implemented to handle text display
            self.dialogue_instance.draw_dialogue(
                text=self.dialogue[0],  # Here, self.dialogue is always a list with at least one item
                color=(204, 0, 204),
                pos=(200, 200))

    def open(self):
        if self.game_state_manager.book01_key_obtained and self.door_opened:
            self.dialogue = [self.open_dialogue[2]]
            self.is_visible = True

        elif self.game_state_manager.book01_key_obtained and not self.door_opened:
            self.dialogue = [self.open_dialogue[1]]
            self.is_visible = True
            self.door_opened = True
        else:
            self.dialogue = [self.open_dialogue[0]]
            self.is_visible = True


    def close(self):
        print("close")

    def listen(self):
        print("listen")

    def push(self):
        print("push")