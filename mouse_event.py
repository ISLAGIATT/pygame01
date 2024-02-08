class MouseEventHandler:
    def __init__(self, clickable_objects, dropdown_menus):
        # Objects that respond directly to clicks (e.g., buttons)
        self.clickable_objects = clickable_objects
        # Dropdown menus which have specific visibility toggling and option selection
        self.dropdown_menus = dropdown_menus

    def handle_click(self, mouse_pos, button):
        # Right-click: Toggle dropdown visibility
        if button == 3:
            self.handle_right_click(mouse_pos)
        # Left-click: General click handling (objects and dropdown options)
        elif button == 1:
            self.handle_left_click(mouse_pos)

    def handle_right_click(self, mouse_pos):
        for dropdown in self.dropdown_menus:
            if dropdown.button.is_over(mouse_pos):  # Assuming each dropdown is associated with a button
                dropdown.toggle_visibility()
                return  # Assuming only one dropdown can be toggled at a time

    def handle_left_click(self, mouse_pos):
        # Check for clicks on dropdown options first
        for dropdown in self.dropdown_menus:
            if dropdown.is_visible:
                hovered_option_index = dropdown.is_over_option(mouse_pos)
                if hovered_option_index is not None:
                    # Execute the associated action for the clicked dropdown option
                    selected_option = dropdown.option_list[hovered_option_index]
                    dropdown.execute_action(selected_option)
                    dropdown.is_visible = False  # Hide after selection
                    return  # Exit to avoid further action if dropdown was interacted with

                # If clicked outside any visible dropdown, hide them
                dropdown.is_visible = False

        # Check for clicks on other clickable objects (e.g., buttons)
        for obj in self.clickable_objects:
            if obj.is_over(mouse_pos):
                obj.handle_click(mouse_pos)
                break  # Assuming only one object can be clicked at a time
