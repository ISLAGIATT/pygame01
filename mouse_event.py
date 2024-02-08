class MouseEventHandler:
    def __init__(self, clickable_objects):
        self.clickable_objects = clickable_objects

    def handle_mouse_click(self, mouse_pos, button):
        for obj in self.clickable_objects:
            if obj.is_clickable() and obj.is_over(mouse_pos):
                obj.handle_click(mouse_pos, button)
                break