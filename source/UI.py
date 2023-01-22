import arcade
import arcade.gui
import Consts
import Main


class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()

        self.background = arcade.load_texture("levels/Background/background.png")

        self.start_button = arcade.gui.UIFlatButton(text="Play", width=200)
        self.quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        self.start_button.on_click = self.on_click_start
        self.quit_button.on_click = self.on_click_quit

        self.v_box = None
        self.manager = None

    def on_show_view(self):
        self.v_box = arcade.gui.UIBoxLayout()

        # Title
        title = arcade.gui.UILabel(text="Platformer Game", font_size=48)
        self.v_box.add(title.with_space_around(bottom=40))

        # Add the buttons to the v_box
        self.v_box.add(self.start_button.with_space_around(bottom=20))
        self.v_box.add(self.quit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        game_view = Main.MyGame()
        self.window.show_view(game_view)

    @staticmethod
    def on_click_quit(event):
        arcade.exit()

    def on_draw(self):
        self.clear()

        # Set background
        arcade.draw_lrwh_rectangle_textured(0, 0, Consts.SCREEN_WIDTH, Consts.SCREEN_HEIGHT, self.background)
        self.manager.draw()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton()
        self.v_box.add(start_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton()
        self.v_box.add(quit_button)


class GameOverView(arcade.View):
    def __init__(self):
        super().__init__()

        # Create the buttons
        self.restart_button = arcade.gui.UIFlatButton(text="Restart Game", width=200)
        self.quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        # Assign callbacks to button events
        self.restart_button.on_click = self.on_click_start
        self.quit_button.on_click = self.on_click_quit

        self.v_box = None
        self.manager = None

    def on_show_view(self):
        self.v_box = arcade.gui.UIBoxLayout()

        # title
        title = arcade.gui.UILabel(text="Game over", font_size=48)
        self.v_box.add(title.with_space_around(bottom=40))

        # Add the buttons to the v_box
        self.v_box.add(self.restart_button.with_space_around(bottom=20))
        self.v_box.add(self.quit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        game_view = Main.MyGame()
        self.window.show_view(game_view)

    @staticmethod
    def on_click_quit(event):
        arcade.exit()

    def on_draw(self):
        self.clear()
        self.manager.draw()

        # Set background color
        arcade.set_background_color(arcade.color.BLACK)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        restart_button = arcade.gui.UIFlatButton()
        self.v_box.add(restart_button.with_space_around(bottom=20))

        quit_button = arcade.gui.UIFlatButton()
        self.v_box.add(quit_button)


class GameWonView(arcade.View):
    def __init__(self):
        super().__init__()

        # Create the buttons
        self.start_button = arcade.gui.UIFlatButton(text="Main menu", width=200)
        self.quit_button = arcade.gui.UIFlatButton(text="Quit", width=200)

        # Assign callbacks to button events
        self.start_button.on_click = self.on_click_start
        self.quit_button.on_click = self.on_click_quit

        self.v_box = None
        self.manager = None

    def on_show_view(self):
        self.v_box = arcade.gui.UIBoxLayout()

        # title
        title = arcade.gui.UILabel(text="You won!!!", font_size=48)
        self.v_box.add(title.with_space_around(bottom=40))

        # Add the buttons to the v_box
        self.v_box.add(self.start_button.with_space_around(bottom=20))
        self.v_box.add(self.quit_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.manager = arcade.gui.UIManager()
        self.manager.enable()
        self.manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="center_x",
                anchor_y="center_y",
                child=self.v_box)
        )

    def on_click_start(self, event):
        """Use a mouse press to advance to the 'game' view."""
        game_view = MainMenu()
        self.window.show_view(game_view)

    @staticmethod
    def on_click_quit(event):
        arcade.exit()

    def on_draw(self):
        """Draw the menu"""
        self.clear()
        self.manager.draw()

        # Set background color
        arcade.set_background_color(arcade.color.LIGHT_BLUE)

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.UIBoxLayout()

        # Create the buttons
        start_button = arcade.gui.UIFlatButton()
        self.v_box.add(start_button.with_space_around(bottom=20))

        # Again, method 1. Use a child class to handle events.
        quit_button = arcade.gui.UIFlatButton()
        self.v_box.add(quit_button)
