"""
Platformer Game
"""
import math
import os
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Platformer"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 1
COIN_SCALING = 1
SPRITE_PIXEL_SIZE = 64
GRID_PIXEL_SIZE = SPRITE_PIXEL_SIZE * TILE_SCALING

# Player constants
PLAYER_MOVEMENT_SPEED = 0
PLAYER_MOVEMENT_SPEED_MAX = 6.5
PLAYER_MOVEMENT_ACCELERATION = 0.25
PLAYER_MOVEMENT_SLOWDOWN = 1.5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


# Player starting position
PLAYER_START_X = 128
PLAYER_START_Y = 225

RIGHT_FACING = 0
LEFT_FACING = 1

# Layer Names from our TileMap
LAYER_NAME_PLATFORMS = "Platformy"
LAYER_NAME_COINS = "Monety"
LAYER_NAME_DONT_TOUCH = "Kolce"
LAYER_NAME_PLAYER = "Player"
LAYER_NAME_ENEMIES = "Przeciwnicy"


def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]

class Enemy(arcade.Sprite):
    """Enemy Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        self.licznik = 0

        # Default to face-right
        self.facing_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.delta = 0
        self.scale = CHARACTER_SCALING

        self.move_speed = -1

        # Track our state
        self.jumping = False

        # --- Load Textures ---
        main_path = "images/enemy1/enemy1"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}a8.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}a2.png")

        # Load textures for walking
        self.walk_textures = []
        texture = load_texture_pair(f"{main_path}a1.png")
        self.walk_textures.append(texture)
        texture = load_texture_pair(f"{main_path}a5.png")
        self.walk_textures.append(texture)
        texture = load_texture_pair(f"{main_path}a6.png")
        self.walk_textures.append(texture)
        texture = load_texture_pair(f"{main_path}a7.png")
        self.walk_textures.append(texture)


        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        self.hit_box = self.texture.hit_box_points

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.facing_direction == RIGHT_FACING:
            self.facing_direction = LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == LEFT_FACING:
            self.facing_direction = RIGHT_FACING

        # Jumping animation
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.facing_direction]
            return
        elif self.change_y < 0:
            self.texture = self.fall_texture_pair[self.facing_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.facing_direction]
            return

        # Walking animation
        self.delta += 1
        if self.cur_texture == 1 or self.cur_texture == 3:
            if self.delta == 10:
                self.cur_texture += 1
                self.delta = 0
        else:
            if self.delta == 10:
                self.cur_texture += 1
                self.delta = 0

        if self.cur_texture > 3:
            self.cur_texture = 0

        self.texture = self.walk_textures[self.cur_texture][
            self.facing_direction
        ]


class PlayerCharacter(arcade.Sprite):
    """Player Sprite"""

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.delta = 0
        self.scale = CHARACTER_SCALING

        # Track our state
        self.jumping = False

        # --- Load Textures ---
        main_path = "images/player1/character1"

        # Load textures for idle standing
        self.idle_texture_pair = load_texture_pair(f"{main_path}0.png")
        self.jump_texture_pair = load_texture_pair(f"{main_path}1.png")
        self.fall_texture_pair = load_texture_pair(f"{main_path}2.png")

        # Load textures for walking
        self.walk_textures = []
        texture = load_texture_pair(f"{main_path}6.png")
        self.walk_textures.append(texture)
        texture = load_texture_pair(f"{main_path}7.png")
        self.walk_textures.append(texture)
        texture = load_texture_pair(f"{main_path}8.png")
        self.walk_textures.append(texture)
        texture = load_texture_pair(f"{main_path}9.png")
        self.walk_textures.append(texture)


        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        self.hit_box = self.texture.hit_box_points

        # health
        self.health = 5

    def update_animation(self, delta_time: float = 1 / 60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        # Jumping animation
        if self.change_y > 0:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.delta += 1
        if self.cur_texture == 1 or self.cur_texture == 3:
            if self.delta == 5:
                self.cur_texture += 1
                self.delta = 0
        else:
            if self.delta == 10:
                self.cur_texture += 1
                self.delta = 0

        if self.cur_texture > 3:
            self.cur_texture = 0

        self.texture = self.walk_textures[self.cur_texture][
            self.character_face_direction
        ]

    def death(self):
        self.health -= 1

        if(self.health > 0):
            # don't reset game
            return 1
        else:
            # reset game
            self.health = 5
            return 0

class MyGame(arcade.Window):
    """
    Main application class.
    """

    def __init__(self):

        # Call the parent class and set up the window
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.player_speed = 0
        self.player_acc = 0

        self.camera = None
        self.gui_camera = None
        self.score = 0
        self.reset_score = True
        self.end_of_map = 0
        self.level = 3

        # sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover1.wav")

        self.new_enemy = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)


    def setup(self):

        """Set up the game here. Call this function to restart the game."""

        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)

        map_name = f"levels/Level{self.level}.json"

        # start level with timer equals 0
        self.new_enemy = 0

        # Layer Specific Options for the Tilemap
        layer_options = {
            LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(map_name, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        if self.reset_score:
            self.score = 0
        self.reset_score = True


        # Create the Sprite lists
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = PLAYER_START_X
        self.player_sprite.center_y = PLAYER_START_Y
        self.scene.add_sprite(LAYER_NAME_PLAYER, self.player_sprite)

        # koniec mapy
        self.end_of_map = (self.tile_map.width - 5) * GRID_PIXEL_SIZE

        # Enemies type 1.
        enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]

        for my_object in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            enemy = Enemy()

            enemy.center_x = math.floor(
                cartesian[0] * TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
            )

            enemy.physics_engine = arcade.PhysicsEnginePlatformer(
                enemy,
                gravity_constant=GRAVITY,
                walls=self.scene[LAYER_NAME_PLATFORMS],
            )
            self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)

        # --- Other stuff
        # Set the background color
        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the 'physics engine'
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=GRAVITY,
            walls=self.scene[LAYER_NAME_PLATFORMS],
        )

    def on_draw(self):
        """Render the screen."""
        # Clear the screen to the background color
        self.clear()

        self.camera.use()

        # Draw our Scene
        self.scene.draw()

        self.gui_camera.use()

        score_text = f"Score: {self.score}"
        arcade.draw_text(
            score_text,
            10,
            10,
            arcade.csscolor.WHITE,
            18,
        )

        life_text = f"Health: {self.player_sprite.health}"
        arcade.draw_text(
            life_text,
            10,
            630,
            arcade.csscolor.RED,
            18,
        )

    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_speed = -1
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_speed = 1
        elif (key == arcade.key.LEFT or key == arcade.key.A) and (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player_speed = 0

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key."""

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_speed = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_speed = 0

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )

        # Don't let camera travel past 0
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def players_death(self):
        if self.player_sprite.death() == 1:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = PLAYER_START_X
            self.player_sprite.center_y = PLAYER_START_Y
        else:
            self.level = 1
            self.setup()
        arcade.play_sound(self.game_over)


    def on_update(self, delta_time):
        """Movement and game logic"""

        # Enemies type 1.
        self.new_enemy += 1

        if self.new_enemy == 240:
            enemies_layer = self.tile_map.object_lists[LAYER_NAME_ENEMIES]

            for my_object in enemies_layer:
                cartesian = self.tile_map.get_cartesian(
                    my_object.shape[0], my_object.shape[1]
                )
                enemy = Enemy()

                enemy.center_x = math.floor(
                    cartesian[0] * TILE_SCALING * self.tile_map.tile_width
                )
                enemy.center_y = math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * TILE_SCALING)
                )

                enemy.physics_engine = arcade.PhysicsEnginePlatformer(
                    enemy,
                    gravity_constant=GRAVITY,
                    walls=self.scene[LAYER_NAME_PLATFORMS],
                )
                self.scene.add_sprite(LAYER_NAME_ENEMIES, enemy)

                self.new_enemy = 0



        # Move the player with the physics engine
        self.physics_engine.update()

        if self.physics_engine.can_jump():
            if self.player_speed > 0:
                if self.player_sprite.change_x < PLAYER_MOVEMENT_SPEED_MAX:
                    self.player_sprite.change_x += PLAYER_MOVEMENT_ACCELERATION * self.player_speed
            elif self.player_speed < 0:
                if self.player_sprite.change_x > -PLAYER_MOVEMENT_SPEED_MAX:
                    self.player_sprite.change_x += PLAYER_MOVEMENT_ACCELERATION * self.player_speed
            else:
                self.player_sprite.change_x = 0

        # animacje
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        self.scene.update_animation(
            delta_time, [LAYER_NAME_COINS, LAYER_NAME_PLAYER, "Znaki", LAYER_NAME_ENEMIES]
        )

        self.scene.update([LAYER_NAME_ENEMIES])

        # See if the enemy hit a boundary and needs to reverse direction.
        for enemy in self.scene[LAYER_NAME_ENEMIES]:
            enemy.physics_engine.update()

            #change of direction
            '''if enemy.change_x == 0:
                enemy.licznik += 1
                if enemy.licznik == 5:
                    enemy.move_speed *= -1
                    enemy.licznik = 0'''

            if enemy.physics_engine.can_jump():
                enemy.change_x = enemy.move_speed

            if arcade.check_for_collision_with_list(
                    enemy, self.scene[LAYER_NAME_DONT_TOUCH]
            ):
                enemy.remove_from_sprite_lists()

            if enemy.center_y < -100:
                enemy.remove_from_sprite_lists()


        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[LAYER_NAME_COINS],
                self.scene[LAYER_NAME_ENEMIES],
            ],
        )

        # Loop through each coin we hit (if any) and remove it
        for collision in player_collision_list:
            if self.scene[LAYER_NAME_ENEMIES] in collision.sprite_lists:
                self.players_death()
                return
            else:
                collision.remove_from_sprite_lists()
                # Play a sound
                arcade.play_sound(self.collect_coin_sound)
                self.score += 1

        if self.player_sprite.center_y < -100:
            self.players_death()

            # Did the player touch something they should not?
        if arcade.check_for_collision_with_list(
                self.player_sprite, self.scene[LAYER_NAME_DONT_TOUCH]
        ):
            self.players_death()

            # See if the user got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            # Advance to the next level
            self.level += 1

            # Make sure to keep the score from this level when setting up the next level
            self.reset_score = False

            # Load the next level
            self.setup()


        self.center_camera_to_player()



def main():
    """Main function"""
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()