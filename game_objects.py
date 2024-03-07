import pygame.time
from dialogue import Dialogue

class InteractiveObject:
    MUSTARD = (199, 142, 0)
    RED = (199, 0, 57)
    TANGERINE = (255, 87, 51)
    MAGENTA = (204, 0, 204)
    PALE_GREEN = (218, 247, 166)
    AQUAMARINE = (0, 255, 255)

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
    listen_dialogue = ["you run your thumb across the unworn pages and it sounds like a deck of cards."]
    touch_dialogue = ["glossed in a cheap finish. the kind of book that is printed so someone can decorate a "
                      "room with it rather than read."]
    consider_dialogue = ["conspicuously placed. or maybe someone left it here in haste?"]

    def __init__(self, dialogue, position, book_button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.book_button = book_button
        self.dialogue_instance = Dialogue()
        self.is_book_open = False
        self.open_dialogue_index = 0
        self.last_show_time = 0
        self.open_dialogue = ["The book opens with a crackle. You find a newly cut brass key inside and pocket it.",
                              "The pages point skyward, waiting for a reader that will never come."]

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.book_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.book_dialogue
                if self.game_state_manager.book01_key_obtained:
                    # If has key will no longer allude to key hidden in book
                    if self.dialogue_index < len(self.book_dialogue) - 2:
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
                self.toggle_visibility()
        print(f"key obtained: {self.game_state_manager.book01_key_obtained}")
        self.last_show_time = pygame.time.get_ticks()

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            if pygame.time.get_ticks() - self.last_show_time > 3500:
                self.is_visible = False
                self.last_show_time = 0
            else:
                if self.is_visible and self.dialogue:
                    if 0 <= self.dialogue_index < len(self.dialogue):
                        current_text = self.dialogue[self.dialogue_index]
                        self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                            text=current_text, color=self.MAGENTA, pos=(200, 200))

    def open(self):
        self.is_visible = True
        if self.game_state_manager.book01_key_obtained: #dialogue for the book being open
            self.dialogue = [self.open_dialogue[1]]
            self.dialogue_index = 0
            self.last_show_time = pygame.time.get_ticks()
        else:
            self.dialogue = [self.open_dialogue[0]] #dialogue for the book being closed
            self.dialogue_index = 0
            self.game_state_manager.pick_up_key01()
            self.is_book_open = True
            self.last_show_time = pygame.time.get_ticks()

    def touch(self):  # touch
        self.last_show_time = pygame.time.get_ticks()
        self.is_visible = True
        self.dialogue = [self.touch_dialogue[0]]
        self.dialogue_index = 0

    def listen(self):
        self.last_show_time = pygame.time.get_ticks()
        self.is_visible = True
        self.dialogue = [self.listen_dialogue[0]]
        self.dialogue_index = 0

    def consider(self):  # consider
        self.last_show_time = pygame.time.get_ticks()
        self.is_visible = True
        self.dialogue = [self.consider_dialogue[0]]
        self.dialogue_index = 0


class Door01(InteractiveObject):
    open_dialogue = ["you reach for the doorknob, and just above it you find a deadbolt with the keyhole facing you.",
                     "the deadbolt disengages with a satisfying yet somewhat off-putting 'THUNK'",
                     "the door is ajar. cold, damp air creeps in through the opening."]
    exam_dialogue = ["a substantial looking door.",
                     "it looks like its been scratched at, but the marks aren't low enough to be from an animal.",
                     "you push your shoulder into it, but there is no give."]
    touch_dialogue = ["your fingers explore the deep crevices of the scratch marks. "
                      "they are of different widths and depths"]
    listen_dialogue = ["you rap lightly on the door. it sounds multitudes more dense than a typical interior door. "
                       "this is meant to keep something out... or in.",
                       "do you hear distant voices, or are you just disoriented?"]
    consider_dialogue = ["finding yourself in a room that locks from the outside bodes poorly."]

    def __init__(self, dialogue, position, button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.door_button = button
        self.dialogue_instance = Dialogue()
        self.game_state_manager = game_state_manager
        self.door_unlocked = False
        self.door_opened = False
        self.open_dialogue_index = 0
        self.last_show_time = 0

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.door_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.exam_dialogue
                if self.door_opened:
                    if self.dialogue_index < len(self.exam_dialogue) - 2: # if door is open, then you can't push with your shoulder
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
        self.last_show_time = pygame.time.get_ticks()

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            if pygame.time.get_ticks() - self.last_show_time > 3500:
                self.is_visible = False
                self.last_show_time = 0
            else:
                if self.is_visible and self.dialogue:
                    if 0 <= self.dialogue_index < len(self.dialogue):
                        current_text = self.dialogue[self.dialogue_index]
                        self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                            text=current_text,
                            color=self.RED,
                            pos=(500, 250))

    def open(self):
        self.is_visible = True
        if self.game_state_manager.book01_key_obtained and self.door_opened:
            self.dialogue = [self.open_dialogue[2]]
            self.dialogue_index = 0
            self.last_show_time = pygame.time.get_ticks()

        elif self.game_state_manager.book01_key_obtained and not self.door_opened:
            self.game_state_manager.door01_unlocked = True
            self.dialogue = [self.open_dialogue[1]]
            self.dialogue_index = 0
            self.game_state_manager.door01_open = True
            self.last_show_time = pygame.time.get_ticks()
            print(f'door open {self.game_state_manager.door01_open}')
        else:
            self.dialogue = [self.open_dialogue[0]]
            self.dialogue_index = 0
            self.last_show_time = pygame.time.get_ticks()

    def touch(self):
        self.is_visible = True
        self.dialogue = [self.touch_dialogue[0]]
        self.dialogue_index = 0
        self.last_show_time = pygame.time.get_ticks()

    def listen(self):
        self.is_visible = True
        if self.game_state_manager.door01_unlocked:
            self.dialogue = [self.listen_dialogue[1]]
            self.last_show_time = pygame.time.get_ticks()
        else:
            self.dialogue = [self.listen_dialogue[0]]
            self.last_show_time = pygame.time.get_ticks()


    def consider(self):
        self.is_visible = True
        self.dialogue = [self.consider_dialogue[0]]
        self.dialogue_index = 0
        self.last_show_time = pygame.time.get_ticks()


class WindowDude01(InteractiveObject):
    window_dude_dialogue = ["...", "you can barely make out a figure outside", "...you think."]

    def __init__(self, dialogue, position, window_dude_button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.dialogue_instance = Dialogue()
        self.window_dude_button = window_dude_button
        self.current_dialogue_rect = None
        self.last_show_time = 0

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.window_dude_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.window_dude_dialogue
                self.advance_dialogue()
                self.toggle_visibility()
            else:
                self.toggle_visibility()
        self.last_show_time = pygame.time.get_ticks()
    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            if pygame.time.get_ticks() - self.last_show_time > 3500:
                self.is_visible = False
                self.last_show_time = 0
            else:
                if self.is_visible and self.dialogue:
                    if 0 <= self.dialogue_index < len(self.dialogue):
                        current_text = self.dialogue[self.dialogue_index]
                        self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                            text=current_text,
                            color=self.TANGERINE,
                            pos=(450, 319))


class LibraryBooks01(InteractiveObject):
    library_books_dialogue = ["many books line the walls", 'unlike most book collections,'
                                                           ' most of these seem recently purchased.',
                              'not a speck of dust to be found.']

    def __init__(self, dialogue, position, library_books_button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.dialogue_instance = Dialogue()
        self.library_books_button = library_books_button
        self.current_dialogue_rect = None
        self.last_show_time = 0

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.library_books_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.library_books_dialogue
                self.advance_dialogue()
                self.toggle_visibility()
            else:
                self.toggle_visibility()
        self.last_show_time = pygame.time.get_ticks()


    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            if pygame.time.get_ticks() - self.last_show_time > 3500:
                self.is_visible = False
                self.last_show_time = 0
            else:
                if self.is_visible and self.dialogue:
                    if 0 <= self.dialogue_index < len(self.dialogue):
                        current_text = self.dialogue[self.dialogue_index]
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
        self.last_show_time = 0

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.light_switch_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.light_switch_dialogue
                self.advance_dialogue()
                self.toggle_visibility()
            else:
                self.toggle_visibility()
        self.last_show_time = pygame.time.get_ticks()

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            if pygame.time.get_ticks() - self.last_show_time > 3500:
                self.is_visible = False
                self.last_show_time = 0
            else:
                if self.is_visible and self.dialogue:
                    if 0 <= self.dialogue_index < len(self.dialogue):
                        current_text = self.dialogue[self.dialogue_index]
                        self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                            text=current_text,
                            color=self.PALE_GREEN,
                            pos=(550, 319))
class Painting01(InteractiveObject):
    painting01_dialogue = ["you should have paid more attention in history class",
                           "... actually you could swear you've seen this man before",
                           "he may be a stock photo model"]

    def __init__(self, dialogue, position, painting01_button, game_state_manager):
        super().__init__(dialogue, position, game_state_manager)
        self.dialogue_instance = Dialogue()
        self.painting01_button = painting01_button
        self.current_dialogue_rect = None
        self.last_show_time = 0

    def handle_click(self, mouse_pos, button):
        if button == 1 and self.painting01_button.is_over(mouse_pos):
            if self.is_visible:
                self.dialogue = self.painting01_dialogue
                self.advance_dialogue()
                self.toggle_visibility()
            else:
                self.toggle_visibility()
        self.last_show_time = pygame.time.get_ticks()

    def show_current_dialogue(self, screen):
        if self.is_visible and self.dialogue:
            if pygame.time.get_ticks() - self.last_show_time > 3500:
                self.is_visible = False
                self.last_show_time = 0
            else:
                if self.is_visible and self.dialogue:
                    if 0 <= self.dialogue_index < len(self.dialogue):
                        current_text = self.dialogue[self.dialogue_index]
                        self.current_dialogue_rect = self.dialogue_instance.draw_dialogue(
                            text=current_text,
                            color=self.AQUAMARINE,
                            pos=(207, 279))
