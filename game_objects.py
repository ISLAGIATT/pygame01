from dialogue import Dialogue

class InteractiveObject:
    MUSTARD = (199, 142, 0)
    RED = (199, 0, 57)
    TANGERINE = (255, 87, 51)
    MAGENTA = (204, 0, 204)
    PALE_GREEN = (218, 247, 166)

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
        self.dialogue_index += 1
        if self.dialogue_index >= len(self.dialogue):
            self.dialogue_index = 0

class Book01(InteractiveObject):
    book_dialogue = ["a brand-new book.", "the pages are stiff and sharp. they has seen very little use.",
                     "the pages of this closed book aren't sitting quite flush."]

    def __init__(self, dialogue, position, book_button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.book_button = book_button
        self.dialogue_instance = Dialogue()
        self.is_book_open = False
        self.open_dialogue_index = 0
        self.open_dialogue = ["The book opens with a crackle. You find a newly cut brass key inside and pocket it.",
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
                    color=self.MAGENTA,
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
    exam_dialogue = ["a substantial looking door.",
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
        if button == 1 and self.door_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.exam_dialogue
                if self.door_opened:
                    if self.dialogue_index < len(self.exam_dialogue) - 2:
                        self.advance_dialogue()
                        self.toggle_visibility()
                    else:
                        self.dialogue_index = 0
                        self.toggle_visibility()
                elif not self.door_opened:
                    if self.dialogue_index < len(self.exam_dialogue) - 1:
                        self.advance_dialogue()
                        self.toggle_visibility()
                    else:
                        self.dialogue_index = 0
                        self.toggle_visibility()
            else:
                self.toggle_visibility()
        print(f"door open: {self.door_opened}\nkey obtained  {self.game_state_manager.book01_key_obtained}")

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            # Ensure dialogue_index is within the correct range
            if 0 <= self.dialogue_index < len(self.dialogue):
                current_text = self.dialogue[self.dialogue_index]  # Access the current dialogue
                self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                    text=current_text,
                    color=self.RED,
                    pos=(500, 250))

    def open(self):
        self.is_visible = True
        if self.game_state_manager.book01_key_obtained and self.door_opened:
            self.dialogue = [self.open_dialogue[2]]
            self.dialogue_index = 0

        elif self.game_state_manager.book01_key_obtained and not self.door_opened:
            self.dialogue = [self.open_dialogue[1]]
            self.dialogue_index = 0
            self.door_opened = True
        else:
            self.dialogue = [self.open_dialogue[0]]
            self.dialogue_index = 0


    def close(self):
        print("close")

    def listen(self):
        print("listen")

    def push(self):
        print("push")

class WindowDude01(InteractiveObject):
    window_dude_dialogue = ["...", "you can barely make out a figure outside", "...you think."]

    def __init__(self, dialogue, position, window_dude_button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.dialogue_instance = Dialogue()
        self.window_dude_button = window_dude_button
        self.current_dialogue_rect = None

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.window_dude_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.window_dude_dialogue
                self.advance_dialogue()
                self.toggle_visibility()
            else:
                self.toggle_visibility()

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            # Ensure dialogue_index is within the correct range
            if 0 <= self.dialogue_index < len(self.dialogue):
                current_text = self.dialogue[self.dialogue_index]  # Access the current dialogue
                self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                    text=current_text,
                    color=self.TANGERINE,
                    pos=(450, 319))

class LibraryBooks01(InteractiveObject):
    library_books_dialogue = ["many books line the walls", 'unlike most book collections, most of these seem recently purchased.', 'not a speck of dust to be found.']

    def __init__(self, dialogue, position, library_books_button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.dialogue_instance = Dialogue()
        self.library_books_button = library_books_button
        self.current_dialogue_rect = None

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.library_books_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.library_books_dialogue
                self.advance_dialogue()
                self.toggle_visibility()
            else:
                self.toggle_visibility()

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            # Ensure dialogue_index is within the correct range
            if 0 <= self.dialogue_index < len(self.dialogue):
                current_text = self.dialogue[self.dialogue_index]  # Access the current dialogue
                self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                    text=current_text,
                    color=self.MUSTARD,
                    pos=(259, 412))

class LightSwitch01(InteractiveObject):
    light_switch_dialogue = ["you flick the lightswitch on. no response",
                             "after giving the lightswitch a few more toggles, you conclude it doesn't work",
                             "...",
                             "you give it one more for the road. no good"]

    def __init__(self, dialogue, position, light_switch_button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.dialogue_instance = Dialogue()
        self.light_switch_button = light_switch_button
        self.current_dialogue_rect = None

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.light_switch_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.light_switch_dialogue
                self.advance_dialogue()
                self.toggle_visibility()
            else:
                self.toggle_visibility()

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            # Ensure dialogue_index is within the correct range
            if 0 <= self.dialogue_index < len(self.dialogue):
                current_text = self.dialogue[self.dialogue_index]  # Access the current dialogue
                self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                    text=current_text,
                    color=self.PALE_GREEN,
                    pos=(550, 319))