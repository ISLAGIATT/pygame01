import pygame

class Dialogue:
    def __init__(self):
        SCREEN_WIDTH = 1024
        SCREEN_HEIGHT = 1024
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.BLACK = (0, 0, 0)

        self.dialogue_1 = ["Hello i am in a cabin",
                      "Still in a cabin",
                      "finally, I am in a cabin"]

        self.dialogue_index_1 = 0

        self.dialogue_2 = ["Yes we are in a cabin",
                      "I agree we are in a cabin",
                      "Finally, we are in a cabin together"]

        self.dialogue_index_2 = 0

    def draw_wrapped_text(self, text, max_characters_per_line, font, color, pos):
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
        pygame.draw.rect(self.screen, self.BLACK, bubble_rect, border_radius=10)  # Draw the rounded rectangle

        y = pos[1]
        for line in lines:
            text_surface = font.render(line, True, color)
            self.screen.blit(text_surface, (pos[0], y))
            y += font.size(line)[1]  # Move to the next line

    def draw_dialogue(self, text, color, pos):
        font = pygame.font.Font(None, 36)
        max_characters_per_line = 25

        if text:
            self.draw_wrapped_text(text, max_characters_per_line, font, color, pos)

    def one_speaker_logic(self, dialogue_list):
        if self.dialogue_index_1 < len(dialogue_list):
            self.draw_dialogue(dialogue_list[self.dialogue_index_1], (255, 0, 144), (200, 200))
        elif self.dialogue_index_1 >= len(dialogue_list):
            self.dialogue_index_1 = 0

    def two_speaker_logic(self):
        # Draw dialogue for character 1 only if there's dialogue available
        if self.dialogue_index_1 < len(self.dialogue_1):
            self.draw_dialogue(self.dialogue_1[self.dialogue_index_1],
                                   (255, 0, 144), (200, 200))  # Character 1

        # If speaker 1's dialogue is complete, start speaker 2's dialogue
        if self.dialogue_index_1 >= len(self.dialogue_1):
            if self.dialogue_index_2 < len(self.dialogue_2):
                self.draw_dialogue(self.dialogue_2[self.dialogue_index_2],
                                       (0, 255, 255), (600, 200))  # Character 2

    def advance_dialogue(self, dialogue_list, dialogue_list02):
        # Assume dialogue_1 is currently active and dialogue_2 is meant to follow.
        if self.dialogue_index_1 < len(dialogue_list) - 1:
            # Advance in dialogue_1
            self.dialogue_index_1 += 1
        elif self.dialogue_index_1 == len(dialogue_list):
            # Last dialogue of dialogue_1 shown, check for dialogue_2
            if self.dialogue_index_2 < len(dialogue_list02):
                # Still more dialogue in dialogue_2 to show
                self.dialogue_index_2 += 1
            elif self.dialogue_index_2 == len(dialogue_list02):
                # Last dialogue of dialogue_2 shown, prepare for reset
                self.dialogue_index_2 += 1  # Increment to signify the end of dialogue_2
            else:
                # Reset after the last dialogue of dialogue_2 has been shown
                self.dialogue_index_1 = 0
                self.dialogue_index_2 = 0  # Reset to start or handle according to your design
        else:
            # If dialogue_1 is finished and dialogue_2 hasn't started or finished, reset or advance logic
            self.dialogue_index_1 = 0  # Consider if you want an immediate reset or other handling