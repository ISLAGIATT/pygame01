import pygame

class ClickableBox:
    def __init__(self, rect, color, callback, visible=True):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.callback = callback
        self.visible = visible

    def update(self, rect, color, callback, visible):
        self.rect = pygame.Rect(rect)
        self.color = color
        self.callback = callback
        self.visible = visible

    def draw(self, surface):
        if self.visible:
            pygame.draw.rect(surface, self.color, self.rect)

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
        # Define a clickable box inside the window. Adjust the position as needed.
        self.clickable_box = ClickableBox((x + 10, y + 30, 80, 30), (255, 0, 0), self.on_click_box)

    def on_click_box(self):
        print("Clickable box was clicked!")

    def update_exits(self):
        current_room_id = self.game_state_manager.get_current_room_id()
        self.exits = self.game_state_manager.get_exits_for_current_room()
        # Update the clickable box based on the current scene
        box_data = self.game_state_manager.get_clickable_box_data_for_room(current_room_id)
        self.clickable_box.update(**box_data)

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

    def draw(self, surface):
        # Set the transparency for the surface: RGBA where A is alpha
        alpha_color = self.bg_color + (200,)  # Adjust the alpha value as needed

        # Fill the window surface with a fully transparent color first
        self.surface.fill((0, 0, 0, 0))  # Clear with full transparency

        # Then draw the rounded rectangle on it
        self.draw_rounded_rect(alpha_color, 10)  # 10 is the corner radius

        # Render the title text
        title_surface = self.font.render(self.title, True, pygame.Color('white'))
        title_rect = title_surface.get_rect(center=(self.rect.width // 2, 20))
        self.surface.blit(title_surface, title_rect)

        # Draw the exits text below the title
        for i, exit_name in enumerate(self.exits):
            text_surface = self.font.render(exit_name, True, pygame.Color('white'))
            self.surface.blit(text_surface, (10, 50 + i * 20))

        # Blit the separate exits window surface onto the main surface
        surface.blit(self.surface, self.rect.topleft)

    def handle_click(self, mouse_pos):
        if self.clickable_box.is_over(mouse_pos):
            self.clickable_box.click()
