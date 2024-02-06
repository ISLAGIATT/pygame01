import pygame
from dialogue import Dialogue
from dropdown import DropdownMenu
from button import Button, TransparentButton
from game_objects import Book01, Door01

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
book_button = TransparentButton(None, 150, 70, (150, 624), 0, None,
                                (128, 128, 255, 0), (64, 64, 128, 0), (128, 128, 255, 0))
book01 = Book01(dialogue=Book01.book_dialogue,
                position=(150, 624), book_button=book_button)
book_dropdown = DropdownMenu(180, 700, ['open', 'close', 'push', 'listen'], {'open': book01.open, 'close': book01.close, 'push': book01.push, 'listen': book01.listen})

# Door
door_button = TransparentButton('DOOR', 150, 400, (793, 350), 0, None,
                                (128, 128, 255, 0), (64, 64, 128, 0), (128, 128, 255, 0))
door01 = Door01(dialogue=Door01.exam_dialogue, position=(793, 350), button=door_button)
door_dropdown = DropdownMenu(680, 563, ['open', 'close', 'push', 'listen'], {'open': door01.open, 'close': door01.close, 'push': door01.push, 'listen': door01.listen})


def handle_click(mouse_pos, button):
    # Book
    if book_button.is_over(mouse_pos):
        book01.handle_click(mouse_pos, button)
    elif door_button.is_over(mouse_pos):
        door01.handle_click(mouse_pos, button)

    print("Mouse clicked at position:", mouse_pos)


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
            # Get the position of the mouse click
            mouse_pos = pygame.mouse.get_pos()
            handle_click(mouse_pos, event.button)

            if event.button == 3:  # Right-click
                if book_button.is_over(mouse_pos):
                    book_dropdown.is_visible = not book_dropdown.is_visible
                if door_button.is_over(mouse_pos):
                    door_dropdown.is_visible = not door_dropdown.is_visible

            elif event.button == 1:  # Left-click
                if book_dropdown.is_visible:
                    # Check if the click is over one of the dropdown options
                    hovered_option_index = book_dropdown.is_over_option(mouse_pos)
                    if hovered_option_index is not None:
                        # Click is on a dropdown option
                        selected_option = book_dropdown.option_list[hovered_option_index]
                        # Execute the associated action
                        book_dropdown.execute_action(selected_option)
                        # Optionally hide the dropdown after an option is selected
                        book_dropdown.is_visible = False
                    else:
                        # Click is outside the dropdown menu, so hide it
                        book_dropdown.is_visible = False
                if door_dropdown.is_visible:
                    # Check if the click is over one of the dropdown options
                    hovered_option_index = door_dropdown.is_over_option(mouse_pos)
                    if hovered_option_index is not None:
                        # Click is on a dropdown option
                        selected_option = door_dropdown.option_list[hovered_option_index]
                        # Execute the associated action
                        door_dropdown.execute_action(selected_option)
                        # Optionally hide the dropdown after an option is selected
                        door_dropdown.is_visible = False
                    else:
                        # Click is outside the dropdown menu, so hide it
                        door_dropdown.is_visible = False

    pygame.display.update()
