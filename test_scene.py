import pygame
from dialogue import Dialogue
from dropdown import DropdownMenu
from button import Button, TransparentButton
from game_objects import Book01, Door01, WindowDude01, LibraryBooks01, LightSwitch01
from game_state_manager import GameStateManager
from mouse_event import MouseEventHandler
from exits_window import ExitsWindow, ClickableBox

game_state_manager = GameStateManager()
dialogue = Dialogue()
pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.mixer.music.load("sounds/Lofi Beat 3.wav")
pygame.mixer.music.set_volume(0.50)
pygame.mixer.music.play(loops=-1)

bg_all_closed = pygame.image.load("images/test_scene/scene03.png")
bg_book_open = pygame.image.load("images/test_scene/scene03_book_open.png")
bg_all_open = pygame.image.load("images/test_scene/scene03_book_and_door_open.png")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (32, 32, 32)

# Instantiate game objects

# Draw Exits Window
# Exit window font
exit_window_font_name = pygame.font.get_default_font()
exit_window_font_size = 24
exit_window_font = pygame.font.Font(exit_window_font_name, exit_window_font_size)
exits_window = ExitsWindow(x=20, y=835, width=150, height=150, font=exit_window_font,
                           game_state_manager=game_state_manager, bg_color=GREY)

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
                             ['open', 'touch', 'listen', 'consider'],
                             {'open': book01.open, 'touch': book01.touch, 'listen': book01.listen,
                              'consider': book01.consider},
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
                             ['open', 'touch', 'listen', 'consider'],
                             {'open': door01.open, 'touch': door01.touch, 'listen': door01.listen,
                              'consider': door01.consider},
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
    # Background changes with game state
    screen.fill((0, 0, 0))
    if game_state_manager.door01_unlocked:
        screen.blit(bg_all_open, (0, 0))
    elif game_state_manager.book01_key_obtained:
        screen.blit(bg_book_open, (0, 0))
    else:
        screen.blit(bg_all_closed, (0, 0))
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

    # Exits Window
    exits_window.update_exits()
    exits_window.draw(screen)

    # Game Loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            run = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # exits_window.on_click_box()
            mouse_pos = event.pos
            button = event.button
            print(f"Mouse pos: {mouse_pos}")
            if not exits_window.handle_click(event.pos, event.button):
                mouse_event_handler.handle_click(event.pos, event.button)
            if exits_window.rect.collidepoint(mouse_pos):
                exits_window.handle_mouse_down(mouse_pos, screen)

        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos
            exits_window.handle_mouse_up(mouse_pos, screen)


    pygame.display.update()
