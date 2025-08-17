import random
from pgzero.builtins import Actor
from pygame import Rect

class Character(Actor):
    def __init__(self, image_prefix, pos, subfolder=None, default_animation="idle", health=3):
        self.image_prefix = image_prefix
        self.subfolder = subfolder
        path_prefix = f"{self.subfolder}/" if self.subfolder else ""
        super().__init__(f"{path_prefix}{image_prefix}_{default_animation}_0", pos=pos)
        self.vy, self.is_on_ground, self.health = 0, True, health
        self.invulnerability_timer = 0
        self.animations = {}
        self.current_animation_name = default_animation
        self.current_frame = 0
        self.animation_speed = 0.2
        self.flip_x = False
        self.hitbox = None

    def _load_animation_frames(self, prefix, max_frames=12):
        frames = []
        for i in range(max_frames):
            frame_name = f"{self.subfolder}/{prefix}_{i}" if self.subfolder else f"{prefix}_{i}"
            try: Actor(frame_name); frames.append(frame_name)
            except Exception: break
        return frames

    def update_physics(self, ground_level, gravity):
        self.vy += gravity
        self.y += self.vy
        if self.hitbox and self.hitbox.bottom > ground_level:
            self.y -= self.hitbox.bottom - ground_level
            self.vy = 0
            self.is_on_ground = True
        if self.invulnerability_timer > 0: self.invulnerability_timer -= 1
        self.update_hitbox_position()

    def update_hitbox_position(self): pass

    def update_animation(self):
        frames = self.animations.get(self.current_animation_name)
        if not frames: return
        self.current_frame = (self.current_frame + self.animation_speed) % len(frames)
        self.image = frames[int(self.current_frame)]

    def custom_draw(self):
        self._flip_x = self.flip_x
        if self.invulnerability_timer > 0 and (self.invulnerability_timer // 6) % 2 == 0: return
        super().draw()

    def take_damage(self, amount, sounds=None):
        if self.invulnerability_timer <= 0:
            self.health -= amount
            self.invulnerability_timer = 120
            if sounds and hasattr(sounds, "damage"): sounds.damage.play()
            return True
        return False

class Player(Character):
    def __init__(self, pos, subfolder=None):
        super().__init__("player", pos, subfolder=subfolder, health=5)
        self.jump_strength = -16
        self.animations = {
            "idle": self._load_animation_frames("player_idle"),
            "run": self._load_animation_frames("player_run"),
            "jump": self._load_animation_frames("player_jump")
        }
        self.hitbox = Rect(0, 0, self.width - 240, self.height - 165)
        self.hitbox_margins = {"top": 100, "left": 120}
        self.update_hitbox_position()

    def update_hitbox_position(self):
        self.hitbox.topleft = (self.left + self.hitbox_margins["left"], self.top + self.hitbox_margins["top"])

    def handle_input(self, keyboard, sounds=None):
        moving = False

        #Define a velocidade de movimento. Um pouco maior no ar para um pulo mais longo.
        move_speed = 5 if not self.is_on_ground else 4

        if keyboard.a:
            self.x -= move_speed
            self.flip_x = True
            moving = True
        if keyboard.d:
            self.x += move_speed
            self.flip_x = False
            moving = True
        if keyboard.space and self.is_on_ground:
            self.vy = self.jump_strength
            self.is_on_ground = False
            if sounds and hasattr(sounds, "jump"):
                sounds.jump.play()
        self.current_animation_name = "jump" if not self.is_on_ground else "run" if moving else "idle"

class Enemy(Character):
    def __init__(self, pos, patrol_range=(100, 300), screen_bounds=(0, 800)):
        super().__init__("enemy", pos, subfolder="enemy", default_animation="run", health=2)
        self.patrol_range_start, self.patrol_range_end = patrol_range
        self.screen_bounds_start, self.screen_bounds_end = screen_bounds
        self.speed = 1.8
        self.direction = 1
        self.detection_range = 500
        self.animations = { "idle": self._load_animation_frames("enemy_idle"), "run": self._load_animation_frames("enemy_run") }
        self.current_animation_name = "idle"
        self.patrol_timer, self.wait_timer = 0, random.randint(90, 150)
        self.hitbox = Rect(0, 0, self.width - 75, self.height - 27)
        self.hitbox_margins = {"top": 12, "left": 40}
        self.update_hitbox_position()

    def update_hitbox_position(self):
        self.hitbox.topleft = (self.left + self.hitbox_margins["left"], self.top + self.hitbox_margins["top"])

    def update_behavior(self, player_pos):
        player_x = player_pos[0]
        if abs(self.x - player_x) < self.detection_range:
            self.current_animation_name = "run"
            if self.x < player_x:
                self.x += self.speed
                self.flip_x = False
            else:
                self.x -= self.speed
                self.flip_x = True
        else:
            self.patrol()
        self.left = max(self.screen_bounds_start, min(self.left, self.screen_bounds_end - self.width))

    def patrol(self):
        if self.patrol_timer > 0:
            self.current_animation_name = "run"
            self.x += self.speed * self.direction
            self.flip_x = self.direction < 0
            if (self.right > self.patrol_range_end and self.direction > 0) or \
               (self.left < self.patrol_range_start and self.direction < 0):
                self.direction *= -1
                self.patrol_timer, self.wait_timer = 0, random.randint(90, 150)
        elif self.wait_timer > 0:
            self.current_animation_name = "idle"
            self.wait_timer -= 1
            if self.wait_timer <= 0:
                self.patrol_timer = random.randint(180, 300)

    def take_damage(self, amount, sounds=None):
        if self.health > 0:
            self.health -= amount
            if sounds and hasattr(sounds, "damage"):
                sounds.damage.play()
            return True
        return False