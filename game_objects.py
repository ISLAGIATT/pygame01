from dialogue import Dialogue

class InteractiveObject:
    def __init__(self, dialogue, position, game_state_manager, size=(100, 30)):
        self.dialogue = dialogue
        self.position = position
        self.size = size
        self.is_visible = False
        self.dialogue_index = 0
        self.dialogue_instance = Dialogue()
        self.game_state_manager = game_state_manager


    def toggle_visibility(self):
        self.is_visible = not self.is_visible

    def advance_dialogue(self):
        print(f"Advance dialogue called. Current dialogue index: {self.dialogue_index}")
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogue):
            self.dialogue_index = 0

        # Ensure this new text is being used in the draw/update function

class Book01(InteractiveObject):
    book_dialogue = ["...", "an old book.", "the pages are stiff and sharp. they has seen very little use.",
                     "the pages of this closed book aren't sitting quite flush."]

    def __init__(self, dialogue, position, book_button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.book_button = book_button
        self.dialogue_instance = Dialogue()
        self.is_book_open = False
        self.open_dialogue_index = 0
        self.open_dialogue = ["The book opens with a creak. You find a newly cut brass key inside and pocket it.",
                               "The pages point skyward, waiting for a reader that will never come."]

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.book_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.book_dialogue
                if self.game_state_manager.book01_key_obtained:
                    # If has key will no longer allude to key hidden in book
                    if self.dialogue_index < 2:
                        self.dialogue_index += 1
                        self.is_visible = False
                    else:
                        self.dialogue_index = 0
                        self.toggle_visibility()
                else:
                    # Key not obtained, cycle through all but the last dialogue
                    if self.dialogue_index < len(self.book_dialogue) - 1:
                        self.advance_dialogue()
                        self.toggle_visibility()
                        print('3')
                        print(f"no key normal advancement {self.dialogue_index}")
                    else:
                        self.dialogue_index = 0  # Loop back to the start
                        self.toggle_visibility()
            else:
                self.is_visible = not self.is_visible  # Just toggle visibility if the book isn't opened yet
        print(f"key obtained: {self.game_state_manager.book01_key_obtained}")

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            # Ensure dialogue_index is within the correct range
            if 0 <= self.dialogue_index < len(self.dialogue):
                current_text = self.dialogue[self.dialogue_index]  # Access the current dialogue
                self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                    text=current_text,
                    color=(204, 0, 204),
                    pos=(200, 200))

    def open(self):
        self.is_visible = True

        if self.game_state_manager.book01_key_obtained:
            self.dialogue = [self.open_dialogue[1]]
            self.dialogue_index = 0
        else:
            self.dialogue = [self.open_dialogue[0]]
            self.dialogue_index = 0
            self.game_state_manager.pick_up_key01()
            self.is_book_open = True


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
            self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
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