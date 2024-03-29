import random
import arcade
import problem_sets_defined as psd
from gui_styles import *

# --- Constants ---
SPRITE_SCALING_PLAYER = 0.5
SPRITE_SCALING_PROBLEM = 0.5

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 900
SCREEN_TITLE = "Mathman 2023"
PLAYER_MOVEMENT_SPEED = 2
PROB_SET_ROW_SCALE = 50


# class QuitButton(arcade.gui.UIFlatButton):
#     def on_click(self, event: arcade.gui.UIOnClickEvent):
#         arcade.exit()
#
#
# class RestartButton(arcade.gui.UIFlatButton):
#     def on_click(self, event: arcade.gui.UIOnClickEvent):
#         pass
#
#
class ProbSetButton0(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        psd.cur_problem_set = psd.problem_sets[0]


class ProbSetButton1(arcade.gui.UIFlatButton):
    def on_click(self, event: arcade.gui.UIOnClickEvent):
        psd.cur_problem_set = psd.problem_sets[1]


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

        self.texture = arcade.load_texture("game_over.png")
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        # --- Required for all code that uses UI element,
        # a UIManager to handle the UI.
        # self.manager = arcade.gui.UIManager()
        # self.manager.enable()
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
        # self.manager.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)


class InstructionView(arcade.View):

    def __init__(self):
        super().__init__()
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        ps0 = ProbSetButton0(text=psd.problem_sets[0]['name'], width=200, style=RED_STYLE)
        self.v_box.add(ps0)
        ps1 = ProbSetButton1(text=psd.problem_sets[1]['name'], width=200, style=RED_STYLE)
        self.v_box.add(ps1)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

        self.cur_problem_set = None

    def on_show_view(self):
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport if we have a scrolling game.
        arcade.set_viewport(0, self.window.width, 0, self.window.height)

    def on_draw(self):
        self.clear()
        arcade.draw_text("Click on your practice set", self.window.width / 2,
                         self.window.height - PROB_SET_ROW_SCALE,
                         arcade.color.YELLOW, font_size=40, anchor_x="center")
        arcade.draw_text("then press any key to begin", self.window.width / 2,
                         self.window.height - PROB_SET_ROW_SCALE * 2,
                         arcade.color.GREEN, font_size=30, anchor_x="center")
        self.manager.draw()

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        """ When the user presses a mouse button start the game """
        self.cur_problem_set = psd.cur_problem_set

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if psd.cur_problem_set is None:
            print('must choose')
        else:
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

        self.scene = None
        self.physics_engine = None

        # Set up the player info
        self.player_sprite = None
        self.score = 0

        # Track the current state of what key is pressed
        self.left_pressed = False
        self.right_pressed = False
        self.up_pressed = False
        self.down_pressed = False

        arcade.set_background_color(arcade.color.AMAZON)
        self.cps = psd.cur_problem_set

    def setup(self):
        """ Set up the game and initialize the variables. """
        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)

        self.scene = arcade.Scene()
        # Sprite lists
        self.scene.add_sprite_list("Player")
        self.problem_sprite_list = arcade.SpriteList()
        self.scene.add_sprite_list("Walls", use_spatial_hash=True)

        # Score
        self.score = 0

        # Set up the player
        # Character image from kenney.nl
        image_source = ":resources:images/animated_characters/female_person/femalePerson_idle.png"
        self.player_sprite = arcade.Sprite(image_source, SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = SCREEN_WIDTH / 2
        self.player_sprite.center_y = SCREEN_HEIGHT / 2
        self.scene.add_sprite("Player", self.player_sprite)

        # Set up the border walls
        # left side
        wall = arcade.Sprite("objects/vertical_wall.png")
        wall.top = 899
        wall.left = 0
        self.scene.add_sprite("Walls", wall)
        # right side
        wall = arcade.Sprite("objects/vertical_wall.png")
        wall.top = 899
        wall.right = 1199
        self.scene.add_sprite("Walls", wall)
        # top
        wall = arcade.Sprite("objects/horizontal_wall.png")
        wall.top = 899
        wall.right = 1199
        self.scene.add_sprite("Walls", wall)
        # bottom
        wall = arcade.Sprite("objects/horizontal_wall.png")
        wall.bottom = 35
        wall.right = 1199
        self.scene.add_sprite("Walls", wall)

        # Set up the problem sprites
        i = 0
        cnt = len(psd.cur_problem_set['answers'])

        while i < cnt:
            problem = arcade.Sprite(psd.cur_problem_set['file_name'][i],
                                    center_x=psd.cur_problem_set['xcoords'][i],
                                    center_y=psd.cur_problem_set['ycoords'][i],
                                    scale=SPRITE_SCALING_PROBLEM)
            problem.ix = i
            problem.answer = psd.cur_problem_set['answers'][i]
            self.problem_sprite_list.append(problem)
            i = i + 1

        self.physics_engine = arcade.PhysicsEngineSimple(self.player_sprite, self.scene.get_sprite_list("Walls"))

    def on_draw(self):
        """ Draw everything """
        self.clear()
        self.scene.draw()
        self.problem_sprite_list.draw()


        # Put the text on the screen.
        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    def on_update(self, delta_time):
        """ Movement and game logic """
        self.player_sprite.center_x += self.player_sprite.change_x
        self.player_sprite.center_y += self.player_sprite.change_y
        self.physics_engine.update()
        self.scene.update()

        # Generate a list of all sprites that collided with the player.
        hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                        self.problem_sprite_list)
        for hit in hit_list:
            print(hit.ix)

        # Loop through each colliding sprite, remove it, and add to the score.

        # If the problem list is empty, we are done, go to game over view
        # if len(self.problem_list) == 0:
        #     view = GameOverView()
        #     self.window.show_view(view)

    def process_keychange(self):
        """
        Called when we change a key up/down
        """
        # Process up/down
        if self.up_pressed and not self.down_pressed:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif self.down_pressed and not self.up_pressed:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_y = 0

        # Process left/right
        if self.right_pressed and not self.left_pressed:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED
        elif self.left_pressed and not self.right_pressed:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        else:
            self.player_sprite.change_x = 0

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = True
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = True
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = True
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = True

        self.process_keychange()

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.UP or key == arcade.key.W:
            self.up_pressed = False
            self.jump_needs_reset = False
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.down_pressed = False
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.left_pressed = False
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.right_pressed = False

        self.process_keychange()


def main():
    """ Main function """
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = InstructionView()
    window.show_view(start_view)
    arcade.run()


if __name__ == "__main__":
    main()
