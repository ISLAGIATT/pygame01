import pygame
from dialogue import Dialogue
from dropdown import DropdownMenu
from button import Button, TransparentButton
from game_objects import Book01, Door01
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

# Mouse event handler
mouse_event_handler = MouseEventHandler(
    clickable_objects=[book_button, door_button],  # Add other clickable objects here
    interactive_objects=[book01, door01],
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
    # dialogue enablers
    if book01.is_visible:
        book01.show_current_dialogue(screen)
    if door01.is_visible:
        door01.show_current_dialogue(screen)

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