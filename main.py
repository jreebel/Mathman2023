import random
import arcade
# import arcade.gui
from gui_styles import *

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Mathman II"


# class QuitButton(arcade.gui.UIFlatButton):
#     def on_click(self, event: arcade.gui.UIOnClickEvent):
#         arcade.exit()
#
#
# class RestartButton(arcade.gui.UIFlatButton):
#     def on_click(self, event: arcade.gui.UIOnClickEvent):
#         pass


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

        # self.texture = arcade.load_texture("game_over.png")
        # arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # Create a vertical BoxGroup to align buttons
        # self.v_box = arcade.gui.UIBoxLayout()
        # quit_button = QuitButton(text="Quit", width=200, style=RED_STYLE)
        # self.v_box.add(quit_button)
        # restart_button = RestartButton(text="Restart", width=200, style=GREEN_STYLE)
        # self.v_box.add(restart_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        # self.manager.add(
        #     arcade.gui.UIAnchorWidget(
        #         anchor_x="center_x",
        #         anchor_y="center_y",
        #         child=self.v_box)
        # )

    def on_draw(self):
        self.clear()
        self.window.set_mouse_visible(True)
        self.texture.draw_sized(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                SCREEN_WIDTH, SCREEN_HEIGHT)
        self.manager.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class InstructionView(arcade.View):
    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport if we have a scrolling game.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Pick your practice set", self.window.width / 2, self.window.height / 2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """ When the user presses a mouse button start the game """
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class GameView(arcade.View):
    """ Our custom Window Class"""

    def __init__(self):
        """ Initializer """
        # Call the parent class initializer
        super().__init__()
        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        self.manager = arcade.gui.UIManager()
        self.manager.enable()

        # Variables that will hold sprite lists
        self.player_list = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        """ Set up the game and initialize the variables. """

        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        # Sprite lists
        self.player_list = arcade.SpriteList()

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        self.player_sprite = arcade.Sprite(":resources:images/animated_characters/female_person/femalePerson_idle.png",
                                           SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 50
        self.player_list.append(self.player_sprite)

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.player_list.draw()

        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_mouse_motion(self, x, y, dx, dy):
        """ Handle Mouse Motion """

        # Move the center of the player sprite to match the mouse x, y
        self.player_sprite.center_x = x
        self.player_sprite.center_y = y

    def on_update(self, delta_time):
        """ Movement and game logic """
        pass

        # Call update on all sprites (The sprites don't do much in this
        # example though.)
        # Generate a list of all sprites that collided with the player.
        # coins_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)

        # Loop through each colliding sprite, remove it, and add to the score.
        # for coin in coins_hit_list:
        #     coin.remove_from_sprite_lists()
        #     self.score += 1

        # If the coin list is empty, we are done, go to game over view
        # if len(self.coin_list) == 0:
        #     view = GameOverView()
        #     self.window.show_view(view)


def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
