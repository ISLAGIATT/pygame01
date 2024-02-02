import pygame
from dialogue import Dialogue
from button import Button

dialogue = Dialogue()
pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.mixer.music.load("Lofi Beat 3.wav")
pygame.mixer.music.set_volume(0.50)
pygame.mixer.music.play(loops=-1)

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

button = (Button(GREEN, 800, 800, 100, 50, 'next button'))

background_image = pygame.image.load("images/bg1.png")

run = True

def handle_click(mouse_pos):
    # Handle the mouse click event here
    print("Mouse clicked at position:", mouse_pos)
    if button.is_over(mouse_pos):
        import scene02
        scene02.run()


while run:
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    dialogue.two_speaker_logic()
    if dialogue.dialogue_index_2 == len(dialogue.dialogue_2):
        button.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            mouse_pos = pygame.mouse.get_pos()
            handle_click(mouse_pos)
            if button.is_over(mouse_pos):
                print(f"Clicked {button.text}")

            dialogue.advance_dialogue()

    pygame.display.update()

pygame.quit()
