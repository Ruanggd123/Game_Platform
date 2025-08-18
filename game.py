import pgzrun
from pgzero.builtins import Actor
from pygame import Rect
from characters import Player, Enemy
import random

#Constantes do Jogo 
WIDTH, HEIGHT = 800, 600
TITLE = "Forest Adventure"
GRAVITY = 0.5
MAX_ENEMIES_ON_SCREEN = 4
MIN_ENEMY_SPAWN_DISTANCE = 350
ENEMY_LIMITS_PER_PHASE = [10, 15, 20]

#Botões da interface
start_button = Rect(WIDTH//2 - 100, HEIGHT//2 - 60, 200, 50)
music_button = Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
exit_button = Rect(WIDTH//2 - 100, HEIGHT//2 + 60, 200, 50)
is_music_enabled = True

#Música e Sons
BACKGROUND_MUSIC = "music_track_1"
WIN_SOUND = "win_track"

#Variáveis Globais do Jogo
game_state = "menu"
GROUND_LEVEL = 0
player = None
enemies = []
ground_tiles = []
player_projectiles = []
enemies_killed_in_phase = 0
current_phase = 1

class Projectile: #criamos nosssa calsse de projetil
    def __init__(self, pos, direction):
        self.rect = Rect(pos, (20, 8))
        self.direction = direction
        self.speed = 10
        self.start_x = self.rect.x
        self.max_range = 400
        self.active = True

    def update(self):
        self.rect.x += self.speed * self.direction
        self.active = abs(self.rect.x - self.start_x) <= self.max_range

    def draw(self):
        screen.draw.filled_rect(self.rect, "yellow")

def spawn_new_enemy(player_to_avoid):
    global enemies_killed_in_phase
    if enemies_killed_in_phase >= ENEMY_LIMITS_PER_PHASE[current_phase - 1]:
        return

    side = random.choice([-1, 1])
    if player_to_avoid.x < WIDTH * 0.25:
        side = 1
    elif player_to_avoid.x > WIDTH * 0.75:
        side = -1
    
    spawn_x = player_to_avoid.x + (MIN_ENEMY_SPAWN_DISTANCE * side)
    spawn_x = max(50, min(spawn_x, WIDTH - 50))
    patrol_range = (spawn_x - 75, spawn_x + 75)
    
    enemies.append(Enemy((spawn_x, GROUND_LEVEL - 100), patrol_range, screen_bounds=(0, WIDTH)))

def reset_game():
    global player, enemies, ground_tiles, GROUND_LEVEL, player_projectiles, enemies_killed_in_phase
    enemies.clear(); ground_tiles.clear(); player_projectiles.clear()
    enemies_killed_in_phase = 0

    tile = Actor("ground_tile.png")
    GROUND_LEVEL = HEIGHT - tile.height
    tile_width = tile.width - 10
    for i in range((WIDTH // tile_width) + 3):
        ground_tiles.append(Actor("ground_tile.png", bottomleft=(i * tile_width, HEIGHT)))

    player = Player((100, GROUND_LEVEL - 100), subfolder="player")
    for _ in range(2):
        spawn_new_enemy(player)

    if is_music_enabled:
        music.play(BACKGROUND_MUSIC); music.set_volume(0.4)

def draw_world():
    screen.blit("background_far", (0, 0))
    for tile in ground_tiles: tile.draw()
    player.custom_draw()
    for e in enemies: e.custom_draw()
    
def draw():
    screen.clear()
    if game_state == "menu":
        screen.blit("background_far", (0, 0))
        screen.draw.filled_rect(start_button, "darkblue")
        screen.draw.text("Start", center=start_button.center, color="white")
        screen.draw.filled_rect(music_button, "darkblue")
        screen.draw.text(f"Music: {'ON' if is_music_enabled else 'OFF'}", center=music_button.center, color="white")
        screen.draw.filled_rect(exit_button, "darkred")
        screen.draw.text("Exit", center=exit_button.center, color="white")
        screen.draw.text("Press 'K' to shoot", center=(700,580 ), color="white", fontsize=30)
    else:
        draw_world()
        if game_state == "paused":
            screen.draw.text("PAUSED", center=(WIDTH/2, HEIGHT/2), fontsize=60, color="white")
        elif game_state == "phase_completed":
            screen.draw.text(f"PHASE {current_phase} COMPLETE!", center=(WIDTH/2, HEIGHT/2 - 40), fontsize=60, color="cyan")
            screen.draw.text("Press ENTER for the next phase", center=(WIDTH/2, HEIGHT/2 + 40), fontsize=30, color="white")
        elif game_state == "win":
            screen.draw.text("YOU WIN!", center=(WIDTH/2, HEIGHT/2 - 40), fontsize=80, color="gold")
            screen.draw.text("Press ENTER to return to the menu", center=(WIDTH/2, HEIGHT/2 + 40), fontsize=30, color="white")
        elif game_state == "playing":
            for p in player_projectiles: p.draw()
            screen.draw.text(f"HEALTH: {player.health}", (10, 10), fontsize=40, color="white")
            screen.draw.text(f"PHASE: {current_phase}/{len(ENEMY_LIMITS_PER_PHASE)}", (10, 50), fontsize=40, color="white")
        elif game_state == "game_over":
            screen.draw.text("GAME OVER", center=(WIDTH/2, HEIGHT/2 - 40), fontsize=80, color="red")
            screen.draw.text("Press ENTER to return to the menu", center=(WIDTH/2, HEIGHT/2 + 40), fontsize=30, color="white")

def update():
    global game_state, enemies_killed_in_phase
    if game_state != "playing": return

    player.handle_input(keyboard, sounds)
    player.update_physics(GROUND_LEVEL, GRAVITY)
    player.update_animation()
    player.wrap_x_with_hitbox(WIDTH)


    for p in player_projectiles[:]:
        p.update()
        for e in enemies:
            if e.hitbox.colliderect(p.rect) and e.take_damage(1, sounds):
                p.active = False
                break
        if not p.active: player_projectiles.remove(p)

    num_enemies_before = len(enemies)
    for e in enemies:
        e.update_behavior(player.hitbox.center)
        e.update_physics(GROUND_LEVEL, GRAVITY)
        e.update_animation()
        if player.hitbox.colliderect(e.hitbox):
            player.take_damage(1, sounds)
    
    enemies[:] = [e for e in enemies if e.health > 0]
    enemies_killed_in_phase += num_enemies_before - len(enemies)

    if enemies_killed_in_phase < ENEMY_LIMITS_PER_PHASE[current_phase - 1]:
        while len(enemies) < MAX_ENEMIES_ON_SCREEN and len(enemies) < enemies_killed_in_phase + 1:
            spawn_new_enemy(player)

    if not enemies and enemies_killed_in_phase >= ENEMY_LIMITS_PER_PHASE[current_phase - 1]:
        music.stop()
        if hasattr(sounds, WIN_SOUND): sounds.win_track.play()
        if current_phase < len(ENEMY_LIMITS_PER_PHASE):
            game_state = "phase_completed"
        else:
            game_state = "win"
    
    if player.health <= 0:
        game_state = "game_over"
        music.stop()

def on_mouse_down(pos, button):
    global game_state, is_music_enabled
    if game_state == "menu":
        if start_button.collidepoint(pos):
            reset_game()
            game_state = "playing"
        elif music_button.collidepoint(pos):
            is_music_enabled = not is_music_enabled
            music.play(BACKGROUND_MUSIC) if is_music_enabled else music.stop()
        elif exit_button.collidepoint(pos):
            exit()

def on_key_down(key):
    global game_state, current_phase
    if key == keys.ESCAPE:
        game_state = "paused" if game_state == "playing" else "playing"
        music.pause() if game_state == "paused" else (music.unpause() if is_music_enabled else None)
    elif game_state in ["game_over", "win"] and key == keys.RETURN:
        game_state = "menu"
        current_phase = 1
        if is_music_enabled: music.play(BACKGROUND_MUSIC)
    elif game_state == "phase_completed" and key == keys.RETURN:
        current_phase += 1
        reset_game()
        game_state = "playing"
    elif game_state == "playing" and key == keys.K:
        direction = 1 if not player.flip_x else -1
        player_projectiles.append(Projectile(player.hitbox.center, direction))
        if hasattr(sounds, "player_shoot"):
            sounds.player_shoot.stop()
            sounds.player_shoot.play()

reset_game()
pgzrun.go()