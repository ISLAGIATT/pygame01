import pygame
import time
class ClickableBox:
    def __init__(self, rect, primary_color, secondary_color, callback, visible=True):
        self.rect = pygame.Rect(rect)
        self.primary_color = (255, 0, 0)  # Original color
        self.secondary_color = (0, 255, 0)  # Color when clicked
        self.current_color = primary_color  # Current color
        self.callback = callback
        self.visible = False
        self.last_click_time = 0

    def handle_mouse_down(self, pos, surface):
        # Change to secondary color on mouse down if over the box
        if self.visible and self.rect.collidepoint(pos):
            self.current_color = self.secondary_color
            self.draw(surface)

    def handle_mouse_up(self, pos, screen):
        # Revert to primary color on mouse up and check for double click
        if self.visible and self.rect.collidepoint(pos):
            self.current_color = self.primary_color
            current_time = pygame.time.get_ticks()
            if current_time - self.last_click_time <= 500:
                self.click()
            self.last_click_time = current_time

    def update(self, rect, color, callback, visible):
        self.rect = pygame.Rect(rect)
        self.current_color = color
        self.callback = callback
        self.visible = visible

    def draw(self, surface):
        if self.visible:
            offset_rect = self.rect.copy()
            offset_rect.x -= surface.get_rect().x
            offset_rect.y -= surface.get_rect().y
            pygame.draw.rect(surface, self.current_color, offset_rect)

    def is_over(self, pos):
        return self.rect.collidepoint(pos)

    def click(self):
        if self.callback:
            self.callback()

class ExitsWindow:
    def __init__(self, x, y, width, height, font, game_state_manager, bg_color=(0, 0, 0), title="Exits"):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.game_state_manager = game_state_manager
        self.bg_color = bg_color
        self.title = title
        self.exits = []
        self.surface = pygame.Surface((width, height), pygame.SRCALPHA)
        self.clickable_box = ClickableBox((10, 30, 30, 30), (255, 0, 0), (0, 255, 0), self.on_click_box)

    def draw(self, surface):
        alpha_color = self.bg_color + (200,)
        self.surface.fill((0, 0, 0, 0))  # Clear with full transparency
        self.draw_rounded_rect(alpha_color, 10)
        # Render the title text
        title_surface = self.font.render(self.title, True, pygame.Color('white'))
        title_rect = title_surface.get_rect(center=(self.rect.width // 2, 20))
        self.surface.blit(title_surface, title_rect)

        # Draw the clickable box if it is visible
        if self.clickable_box.visible:
            self.clickable_box.draw(self.surface)

        # Draw the exits text below the title
        for i, exit_name in enumerate(self.exits):
            text_surface = self.font.render(exit_name, True, pygame.Color('white'))
            self.surface.blit(text_surface, (10, 50 + i * 20))

        surface.blit(self.surface, self.rect.topleft)

    def handle_mouse_down(self, mouse_pos, screen):
        if self.rect.collidepoint(mouse_pos):
            relative_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
            self.clickable_box.handle_mouse_down(relative_pos, self.surface)

    def handle_mouse_up(self, mouse_pos, screen):
        if self.rect.collidepoint(mouse_pos):
            relative_pos = (mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y)
            self.clickable_box.handle_mouse_up(relative_pos, screen)

    def handle_click(self, mouse_pos, button):
        if self.rect.collidepoint(mouse_pos) and not self.clickable_box.is_over(mouse_pos):
            if self.clickable_box.visible and self.clickable_box.rect.collidepoint(mouse_pos[0] - self.rect.x, mouse_pos[1] - self.rect.y):
                self.clickable_box.click()
                return True
        return False

    def on_click_box(self):
        print("Clickable box was clicked!")

    def update_exits(self):
        current_room_id = self.game_state_manager.get_current_room_id()
        self.exits = self.game_state_manager.get_exits_for_current_room()
        self.update_clickable_box(self.game_state_manager.door01_open)

    def update_clickable_box(self, door_open):
        """Updates the ClickableBox properties based on the door open state."""
        if door_open:
            new_rect = pygame.Rect(100, 55, 15, 15)  # Define new properties
            new_callback = self.on_click_box_open_door  # Define new callback
            self.clickable_box.update(new_rect, self.clickable_box.current_color, new_callback, True)  # Update ClickableBox
        else:
            # Reset ClickableBox properties (optional)
            self.clickable_box.current_color = self.clickable_box.primary_color
            self.clickable_box.secondary_color = (0, 255, 0)

    def on_click_box_open_door(self):
        # Define what happens when the clickable box is clicked and the door is open
        print("Clickable box was clicked when the door is open!")

    def draw_rounded_rect(self, color, corner_radius):
        """Draws a rectangle with rounded corners on the window's surface."""
        rect = self.surface.get_rect()
        if rect.width < 2 * corner_radius or rect.height < 2 * corner_radius:
            raise ValueError("The rectangle dimensions are too small for the specified corner radius")

        # Inflate the rectangle for the sides, then draw the sides without the corners
        pygame.draw.rect(self.surface, color, rect.inflate(-2 * corner_radius, 0))
        pygame.draw.rect(self.surface, color, rect.inflate(0, -2 * corner_radius))

        # Corner positions
        corner_positions = [
            rect.topleft,
            rect.topright,
            rect.bottomleft,
            rect.bottomright
        ]

        # Adjusted center positions for the circles based on corner radius
        for position in corner_positions:
            # Manually calculate the offset for the circle's center
            if position in [rect.topleft, rect.bottomleft]:
                center_x = position[0] + corner_radius
            else:
                center_x = position[0] - corner_radius

            if position in [rect.topleft, rect.topright]:
                center_y = position[1] + corner_radius
            else:
                center_y = position[1] - corner_radius

            pygame.draw.circle(self.surface, color, (center_x, center_y), corner_radius)




