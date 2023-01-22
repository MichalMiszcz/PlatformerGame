import math
import arcade
import arcade.gui

import Player
import Enemy
import UI
import Consts


class MyGame(arcade.View):

    def __init__(self):

        super().__init__()

        self.tile_map = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.player_speed = 0
        self.player_acc = 0
        self.down_pressed = False
        self.bought = False
        self.health = 5

        # Shooting mechanics
        self.can_shoot = False
        self.shoot_timer = 0
        self.shoot_pressed = False
        self.bullets = 0

        # UI and camera
        self.camera = None
        self.gui_camera = None
        self.score = 0
        self.reset_score = True
        self.end_of_map = 0
        self.end_of_map1 = 0
        self.level = 1

        # Sounds
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.lose = arcade.load_sound(":resources:sounds/lose5.wav")
        self.game_over = arcade.load_sound(":resources:sounds/gameover4.wav")
        self.shoot_sound = arcade.load_sound(":resources:sounds/hurt5.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hit5.wav")
        self.upgrade = arcade.load_sound(":resources:sounds/upgrade1.wav")

        self.new_enemy = 0

        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

    def setup(self):

        self.camera = arcade.Camera(self.window.width, self.window.height)
        self.gui_camera = arcade.Camera(self.window.width, self.window.height)

        if self.level <= Consts.NUMBER_OF_LEVELS:
            map_name = f"levels/Level{self.level}.json"
        else:
            game_won = UI.GameWonView()
            self.window.show_view(game_won)
            return

        self.new_enemy = 0

        # Layer Specific Options for the Tilemap
        layer_options = {
            Consts.LAYER_NAME_PLATFORMS: {
                "use_spatial_hash": True,
            },
            Consts.LAYER_NAME_COINS: {
                "use_spatial_hash": True,
            },
            Consts.LAYER_NAME_DONT_TOUCH: {
                "use_spatial_hash": True,
            },
            "Sklep": {
                "use_spatial_hash": True,
            },
        }

        self.tile_map = arcade.load_tilemap(map_name, Consts.TILE_SCALING, layer_options)
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        if self.reset_score:
            self.score = 0
        self.reset_score = True

        # Shooting mechanics
        self.can_shoot = True
        self.shoot_timer = 0

        self.player_sprite = Player.PlayerCharacter()
        self.player_sprite.center_x = Consts.PLAYER_START_X
        self.player_sprite.center_y = Consts.PLAYER_START_Y
        self.scene.add_sprite(Consts.LAYER_NAME_PLAYER, self.player_sprite)

        # variable for detecting if player ended the level
        self.end_of_map = (self.tile_map.width - 5) * Consts.GRID_PIXEL_SIZE
        # variable for detecting right edge of tilemap
        self.end_of_map1 = (self.tile_map.width - 16) * Consts.GRID_PIXEL_SIZE

        # Enemies
        enemies_layer = self.tile_map.object_lists[Consts.LAYER_NAME_ENEMIES]

        for my_object in enemies_layer:
            cartesian = self.tile_map.get_cartesian(
                my_object.shape[0], my_object.shape[1]
            )
            enemy = Enemy.Enemy()

            enemy.center_x = math.floor(
                cartesian[0] * Consts.TILE_SCALING * self.tile_map.tile_width
            )
            enemy.center_y = math.floor(
                (cartesian[1] + 1) * (self.tile_map.tile_height * Consts.TILE_SCALING)
            )

            enemy.physics_engine = arcade.PhysicsEnginePlatformer(
                enemy,
                gravity_constant=Consts.GRAVITY,
                walls=self.scene[Consts.LAYER_NAME_PLATFORMS],
            )
            self.scene.add_sprite(Consts.LAYER_NAME_ENEMIES, enemy)

        self.scene.add_sprite_list(Consts.LAYER_NAME_BULLETS)

        if self.tile_map.background_color:
            arcade.set_background_color(self.tile_map.background_color)

        # Create the physics engine
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite,
            gravity_constant=Consts.GRAVITY,
            walls=self.scene[Consts.LAYER_NAME_PLATFORMS],
        )

    def death(self):
        self.health -= 1

        if self.health > 0:
            # don't reset game
            return 1
        else:
            # reset game
            self.health = 5
            return 0

    def on_show_view(self):
        self.setup()

    def on_draw(self):
        # Clear the screen to the background color
        self.clear()

        self.camera.use()

        # Draw scene
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

        life_text = f"Health: {self.health}"
        arcade.draw_text(
            life_text,
            10,
            630,
            arcade.csscolor.RED,
            18,
        )

        bullet_text = f"Bullets: {self.bullets}"
        arcade.draw_text(
            bullet_text,
            870,
            10,
            arcade.csscolor.WHITE,
            18,
        )

    def on_key_press(self, key, modifiers):

        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = Consts.PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_speed = -1
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_speed = 1
        elif (key == arcade.key.LEFT or key == arcade.key.A) and (key == arcade.key.RIGHT or key == arcade.key.D):
            self.player_speed = 0

        if key == arcade.key.SPACE:
            self.shoot_pressed = True

        if key == arcade.key.DOWN:
            self.down_pressed = True

        if key == arcade.key.ESCAPE:
            game_view = UI.MainMenu()
            self.window.show_view(game_view)

    def on_key_release(self, key, modifiers):

        if key == arcade.key.LEFT or key == arcade.key.A:
            self.player_speed = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_speed = 0

        if key == arcade.key.SPACE:
            self.shoot_pressed = False

        if key == arcade.key.DOWN:
            self.down_pressed = False
            self.bought = False

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
                self.camera.viewport_height / 2
        )

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        if screen_center_x > self.end_of_map1:
            screen_center_x = self.end_of_map1
        player_centered = screen_center_x, screen_center_y

        self.camera.move_to(player_centered)

    def players_death(self):
        if self.death() == 1:
            self.player_sprite.change_x = 0
            self.player_sprite.change_y = 0
            self.player_sprite.center_x = Consts.PLAYER_START_X
            self.player_sprite.center_y = Consts.PLAYER_START_Y
            arcade.play_sound(self.lose)
        else:
            self.level = 1
            game_over = UI.GameOverView()
            self.window.show_view(game_over)
            arcade.play_sound(self.game_over)

    def on_update(self, delta_time):

        # Enemies
        self.new_enemy += 1

        if self.new_enemy == 240:
            enemies_layer = self.tile_map.object_lists[Consts.LAYER_NAME_ENEMIES]

            for my_object in enemies_layer:
                cartesian = self.tile_map.get_cartesian(
                    my_object.shape[0], my_object.shape[1]
                )
                enemy = Enemy.Enemy()

                enemy.center_x = math.floor(
                    cartesian[0] * Consts.TILE_SCALING * self.tile_map.tile_width
                )
                enemy.center_y = math.floor(
                    (cartesian[1] + 1) * (self.tile_map.tile_height * Consts.TILE_SCALING)
                )

                enemy.physics_engine = arcade.PhysicsEnginePlatformer(
                    enemy,
                    gravity_constant=Consts.GRAVITY,
                    walls=self.scene[Consts.LAYER_NAME_PLATFORMS],
                )
                self.scene.add_sprite(Consts.LAYER_NAME_ENEMIES, enemy)

                self.new_enemy = 0

        # Move the player with the physics engine
        self.physics_engine.update()

        if self.physics_engine.can_jump():
            if self.player_speed > 0:
                if self.player_sprite.change_x < Consts.PLAYER_MOVEMENT_SPEED_MAX:
                    self.player_sprite.change_x += Consts.PLAYER_MOVEMENT_ACCELERATION * self.player_speed
            elif self.player_speed < 0:
                if self.player_sprite.change_x > -Consts.PLAYER_MOVEMENT_SPEED_MAX:
                    self.player_sprite.change_x += Consts.PLAYER_MOVEMENT_ACCELERATION * self.player_speed
            else:
                self.player_sprite.change_x = 0

        if self.bullets == 0:
            self.can_shoot = False

        if self.can_shoot:
            if self.shoot_pressed:
                arcade.play_sound(self.shoot_sound)
                bullet = arcade.Sprite("levels/Sprites/pocisk.png", 1)

                if self.player_sprite.character_face_direction == Consts.RIGHT_FACING:
                    bullet.change_x = Consts.BULLET_SPEED
                else:
                    bullet.change_x = -Consts.BULLET_SPEED

                bullet.center_x = self.player_sprite.center_x
                bullet.center_y = self.player_sprite.center_y

                self.scene.add_sprite(Consts.LAYER_NAME_BULLETS, bullet)
                self.bullets -= 1
                self.can_shoot = False
        else:
            self.shoot_timer += 1
            if self.shoot_timer == Consts.SHOOT_SPEED:
                self.can_shoot = True
                self.shoot_timer = 0

        # Animations
        if self.physics_engine.can_jump():
            self.player_sprite.can_jump = False
        else:
            self.player_sprite.can_jump = True

        if self.level == 1:
            self.scene.update_animation(
                delta_time, [Consts.LAYER_NAME_COINS, Consts.LAYER_NAME_PLAYER, "Znaki", Consts.LAYER_NAME_ENEMIES]
            )
        else:
            self.scene.update_animation(
                delta_time, [Consts.LAYER_NAME_COINS, Consts.LAYER_NAME_PLAYER, "Znaki",
                             Consts.LAYER_NAME_ENEMIES, "Sklep"]
            )

        self.scene.update([Consts.LAYER_NAME_ENEMIES, Consts.LAYER_NAME_BULLETS])

        for enemy in self.scene[Consts.LAYER_NAME_ENEMIES]:
            enemy.physics_engine.update()

            if enemy.physics_engine.can_jump():
                enemy.change_x = enemy.move_speed

            if arcade.check_for_collision_with_list(
                    enemy, self.scene[Consts.LAYER_NAME_DONT_TOUCH]
            ):
                enemy.remove_from_sprite_lists()

            if enemy.center_y < -100:
                enemy.remove_from_sprite_lists()

        for bullet in self.scene[Consts.LAYER_NAME_BULLETS]:
            hit_list = arcade.check_for_collision_with_lists(
                bullet,
                [
                    self.scene[Consts.LAYER_NAME_ENEMIES],
                    self.scene[Consts.LAYER_NAME_PLATFORMS],
                ],
            )

            if hit_list:
                bullet.remove_from_sprite_lists()

                for collision in hit_list:
                    if (
                            self.scene[Consts.LAYER_NAME_ENEMIES]
                            in collision.sprite_lists
                    ):
                        collision.death()
                        arcade.play_sound(self.hit_sound)

                return

            if (bullet.right < 0) or (
                    bullet.left
                    > (self.tile_map.width * self.tile_map.tile_width) * Consts.TILE_SCALING
            ):
                bullet.remove_from_sprite_lists()

        player_collision_list = arcade.check_for_collision_with_lists(
            self.player_sprite,
            [
                self.scene[Consts.LAYER_NAME_COINS],
                self.scene[Consts.LAYER_NAME_ENEMIES],
            ],
        )

        # Loop through each coin we hit (if any) and remove it
        for collision in player_collision_list:
            if self.scene[Consts.LAYER_NAME_ENEMIES] in collision.sprite_lists:
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
                self.player_sprite, self.scene[Consts.LAYER_NAME_DONT_TOUCH]
        ):
            self.players_death()

        # Checking if player touched shop
        if self.level > 1:
            if arcade.check_for_collision_with_list(
                    self.player_sprite, self.scene["Sklep"]
            ):
                if self.down_pressed and not self.bought:
                    if self.score >= 2:
                        self.bullets += 1
                        self.score -= 2
                        self.bought = True
                        arcade.play_sound(self.upgrade)

        # See if the player got to the end of the level
        if self.player_sprite.center_x >= self.end_of_map:
            self.level += 1

            # Make sure to keep the score from this level when setting up the next level
            self.reset_score = False

            self.setup()

        self.center_camera_to_player()


def main():
    window = arcade.Window(Consts.SCREEN_WIDTH, Consts.SCREEN_HEIGHT, Consts.SCREEN_TITLE)
    menu_view = UI.MainMenu()
    window.show_view(menu_view)
    arcade.run()


if __name__ == "__main__":
    main()
