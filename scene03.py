import pygame
from dialogue import Dialogue
from dropdown import DropdownMenu
from button import Button, TransparentButton
from game_objects import Book01

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

book_button = TransparentButton(None, 150, 70, (150, 624), 0, None,
                                (128, 128, 255, 0), (64, 64, 128, 0), (128, 128, 255, 0))
book01 = Book01(dialogue=Book01.book_dialogue, options=None,
                position=(150, 624), book_button=book_button)
book_dropdown = DropdownMenu(180, 700, ['open', 'close', 'push', 'listen'], {'open': book01.open, 'close': book01.close, 'push': book01.push, 'listen': book01.listen})
book01.options = book01_dropdown_actions = {
    "open": book01.open,
    "close": book01.close,
    "push": book01.push,
    "listen": book01.listen
}
book01.options = book01_dropdown_actions
show_book = False


def handle_click(mouse_pos, button):
    # Book
    if book_button.is_over(mouse_pos):
        book01.handle_click(mouse_pos, button)
    print("Mouse clicked at position:", mouse_pos)


run = True

while run:
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    # book button
    book_button.draw(screen)
    book_dropdown.draw(screen)

    if book01.is_visible:
        book01.dialogue_instance.one_speaker_logic(book01.book_dialogue)
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            handle_click(mouse_pos, event.button)
            mouse_pos = pygame.mouse.get_pos()
            if event.button == 3:  # Right-click
                if book_button.is_over(mouse_pos):
                    book_dropdown.is_visible = not book_dropdown.is_visible
            elif event.button == 1:  # Left-click
                if book_dropdown.is_visible:  # Ensure dropdown is visible before checking for option hover
                    hovered_option_index = book_dropdown.is_over_option(mouse_pos)
                    if hovered_option_index is not None:
                        selected_option = book_dropdown.option_list[hovered_option_index]
                        # Execute the action associated with the selected option
                        if selected_option in book_dropdown.action_map:
                            book_dropdown.action_map[selected_option]()

    pygame.display.update()



