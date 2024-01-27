import pygame

pygame.init()

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 1024
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.mixer.music.load("Lofi Beat 3.wav")
pygame.mixer.music.set_volume(0.50)
pygame.mixer.music.play(loops=-1)

BLACK = (0, 0, 0)

background_image = pygame.image.load("bg1.png")

run = True

def handle_click(mouse_pos):
    # Handle the mouse click event here
    print("Mouse clicked at position:", mouse_pos)


dialogue_1 = ["Hello i am in a cabin",
              "Still in a cabin",
              "finally, I am in a cabin"]

dialogue_index_1 = 0

dialogue_2 = ["Yes we are in a cabin",
              "I agree we are in a cabin",
              "Finally, we are in a cabin together"]

dialogue_index_2 = 0

def draw_wrapped_text(text, max_characters_per_line, font, color, pos):
    words = text.split()
    lines = []
    current_line = ''
    for word in words:
        if font.size(current_line + word)[0] <= max_characters_per_line * font.size('A')[0]:
            current_line += ' ' + word
        else:
            lines.append(current_line.lstrip())
            current_line = word
    lines.append(current_line.lstrip())

    # Calculate the size of the dialogue bubble
    max_width = max(font.size(line)[0] for line in lines)
    total_height = sum(font.size(line)[1] for line in lines)
    bubble_rect = pygame.Rect(pos[0] - 10, pos[1] - 10, max_width + 20, total_height + 20)
    pygame.draw.rect(screen, BLACK, bubble_rect, border_radius=10)  # Draw the rounded rectangle

    y = pos[1]
    for line in lines:
        text_surface = font.render(line, True, color)
        screen.blit(text_surface, (pos[0], y))
        y += font.size(line)[1]  # Move to the next line

def draw_dialogue(text, color, pos):
    font = pygame.font.Font(None, 36)
    max_characters_per_line = 25

    if text:
        draw_wrapped_text(text, max_characters_per_line, font, color, pos)

while run:
    screen.fill((0, 0, 0))
    screen.blit(background_image, (0, 0))

    # Draw dialogue for character 1 only if there's dialogue available
    if dialogue_index_1 < len(dialogue_1):
        draw_dialogue(dialogue_1[dialogue_index_1], (255, 0, 144), (200, 200))  # Character 1

    # If speaker 1's dialogue is complete, start speaker 2's dialogue
    if dialogue_index_1 >= len(dialogue_1):
        if dialogue_index_2 < len(dialogue_2):
            draw_dialogue(dialogue_2[dialogue_index_2], (0, 255, 255), (600, 200))  # Character 2

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.mixer.music.stop()
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the mouse click
            mouse_pos = pygame.mouse.get_pos()
            handle_click(mouse_pos)

            # Advance to speaker 2's dialogue after speaker 1 is finished
            if dialogue_index_1 >= len(dialogue_1):
                # Increment dialogue index for speaker 2 if there's more dialogue
                if dialogue_index_2 < len(dialogue_2):
                    dialogue_index_2 += 1

            # Increment dialogue index for speaker 1 if there's more dialogue
            elif dialogue_index_1 < len(dialogue_1):
                dialogue_index_1 += 1

    pygame.display.update()

pygame.quit()
