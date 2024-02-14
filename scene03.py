import pygame
from dialogue import Dialogue
from dropdown import DropdownMenu
from button import Button, TransparentButton
from game_objects import Book01, Door01, WindowDude01, LibraryBooks01, LightSwitch01
from game_state_manager import GameStateManager
from mouse_event import MouseEventHandler

game_state_manager = GameStateManager()
dialogue = Dialogue()
pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.mixer.music.load("Lofi Beat 3.wav")
pygame.mixer.music.set_volume(0.50)
pygame.mixer.music.play(loops=-1)

background_image = pygame.image.load("images/scene03.png")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Instantiate game objects

# Book
book_button = TransparentButton(text=None,
                                width=150,
                                height=70,
                                pos=(150, 624),
                                elevation=0,
                                action=lambda: book01.handle_click(mouse_pos, button),
                                color=(128, 128, 255, 0),
                                shadow=(64, 64, 128, 0),
                                hover=(128, 128, 255, 0),
                                image=None)
book01 = Book01(dialogue=Book01.book_dialogue,
                position=(150, 624),
                book_button=book_button,
                game_state_manager=game_state_manager)
book_dropdown = DropdownMenu(180,
                             700,
                             ['open', 'close', 'push', 'listen'],
                             {'open': book01.open, 'close': book01.close, 'push': book01.push,
                              'listen': book01.listen},
                             game_state_manager,
                             button=book_button)

# Door
door_button = TransparentButton(text=None,
                                width=150,
                                height=400,
                                pos=(793, 350),
                                elevation=0,
                                action=lambda: door01.handle_click(mouse_pos, button),
                                image=None,
                                color=(128, 128, 255, 0),
                                shadow=(64, 64, 128, 0),
                                hover=(128, 128, 255, 0))
door01 = Door01(dialogue=Door01.exam_dialogue,
                position=(793, 350),
                button=door_button,
                game_state_manager=game_state_manager)
door_dropdown = DropdownMenu(680,
                             563,
                             ['open', 'close', 'push', 'listen'],
                             {'open': door01.open, 'close': door01.close, 'push': door01.push,
                              'listen': door01.listen},
                             game_state_manager,
                             button=door_button)

# Window Dude
window_dude = WindowDude01(dialogue=WindowDude01.window_dude_dialogue,
                           position=(440, 435),
                           window_dude_button=None,
                           game_state_manager=game_state_manager)
window_dude_button = TransparentButton(text=None,
                                       width=120,
                                       height=170,
                                       pos=(440, 435),
                                       elevation=0,
                                       action=lambda: window_dude.handle_click(mouse_pos, button),
                                       image=None,
                                       color=(128, 128, 255, 0),
                                       shadow=(64, 64, 128, 0),
                                       hover=(128, 128, 255, 0))
window_dude.window_dude_button = window_dude_button

# Library Books

library_books = LibraryBooks01(dialogue=LibraryBooks01.library_books_dialogue,
                               position=(440, 435),
                               library_books_button=None,
                               game_state_manager=game_state_manager)
library_books_button = TransparentButton(text=None,
                                         width=110,
                                         height=240,
                                         pos=(90, 380),
                                         elevation=0,
                                         action=lambda: library_books.handle_click(mouse_pos, button),
                                         image=None,
                                         color=(128, 128, 255, 0),
                                         shadow=(64, 64, 128, 0),
                                         hover=(128, 128, 255, 0))
library_books.library_books_button = library_books_button

# Light Switch

light_switch = LightSwitch01(dialogue=LightSwitch01.light_switch_dialogue,
                             position=(500, 500),
                             light_switch_button=None,
                             game_state_manager=game_state_manager)
light_switch_button = TransparentButton(text=None,
                                        width=30,
                                        height=40,
                                        pos=(678, 475),
                                        elevation=0,
                                        action=lambda: light_switch.handle_click(mouse_pos, button),
                                        image=None,
                                        color=(128, 128, 255, 0),
                                        shadow=(64, 64, 128, 0),
                                        hover=(128, 128, 255, 0))
light_switch.light_switch_button = light_switch_button

# Mouse event handler
mouse_event_handler = MouseEventHandler(
    clickable_objects=[book_button, door_button, window_dude_button, library_books_button, light_switch_button],  # Add other clickable objects here
    interactive_objects=[book01, door01, window_dude, library_books, light_switch],
    dropdown_menus=[book_dropdown, door_dropdown]  # Add other dropdown menus here
)

run = True

while run:
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # book button
    book_button.draw(screen)
    book_dropdown.draw(screen)
    # door button
    door_button.draw(screen)
    door_dropdown.draw(screen)
    # window dude
    window_dude_button.draw(screen)
    # library books
    library_books_button.draw(screen)
    # light switch
    light_switch_button.draw(screen)

    # dialogue enablers
    if book01.is_visible:
        book01.show_current_dialogue(screen)
    if door01.is_visible:
        door01.show_current_dialogue(screen)
    if window_dude.is_visible:
        window_dude.show_current_dialogue(screen)
    if library_books.is_visible:
        library_books.show_current_dialogue(screen)
    if light_switch.is_visible:
        light_switch.show_current_dialogue(screen)

    # Game Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            print(f"Mouse pos: {mouse_pos}")
            button = event.button
            mouse_event_handler.handle_click(mouse_pos, event.button)

    pygame.display.update()
