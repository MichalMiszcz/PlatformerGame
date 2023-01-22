import arcade
import Consts


def load_texture_pair(filename):
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, flipped_horizontally=True),
    ]


class Enemy(arcade.Sprite):

    def __init__(self):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.facing_direction = Consts.RIGHT_FACING

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.delta = 0
        self.scale = Consts.CHARACTER_SCALING

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
        if self.change_x < 0 and self.facing_direction == Consts.RIGHT_FACING:
            self.facing_direction = Consts.LEFT_FACING
        elif self.change_x > 0 and self.facing_direction == Consts.LEFT_FACING:
            self.facing_direction = Consts.RIGHT_FACING

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

    def death(self):
        self.remove_from_sprite_lists()
