import random
import pygame
import esper
from src.ecs.components.c_enemy_spawner import CEnemySpawner
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemy import CTagEnemy
from src.ecs.components.tags.c_tag_player import CTagPlayer


def create_square(
        ecs_world: esper.World,
        size: pygame.Vector2,
        position: pygame.Vector2,
        velocity: pygame.Vector2,
        color: pygame.Color):

    square_entity = ecs_world.create_entity()

    ecs_world.add_component(square_entity, CSurface(size, color))
    ecs_world.add_component(square_entity, CTransform(position))
    ecs_world.add_component(square_entity, CVelocity(velocity))

    return square_entity


def create_player_square(
        world: esper.World,
        player_config: dict,
        player_level_config: dict) -> int:

    size = pygame.Vector2(
        player_config["size"]["x"],
        player_config["size"]["y"])
    color = pygame.Color(
        player_config["color"]["r"],
        player_config["color"]["g"],
        player_config["color"]["b"])
    position = pygame.Vector2(
        player_level_config["position"]["x"] - (size.x / 2),
        player_level_config["position"]["y"] - (size.y / 2))
    velocity = pygame.Vector2(0, 0)
    player_entity = create_square(world, size, position, velocity, color)
    world.add_component(player_entity, CTagPlayer())
    return player_entity


def create_enemy_square(
        world: esper.World,
        position: pygame.Vector2,
        enemy_config: dict):

    size = pygame.Vector2(
        enemy_config["size"]["x"],
        enemy_config["size"]["y"])
    color = pygame.Color(
        enemy_config["color"]["r"],
        enemy_config["color"]["g"],
        enemy_config["color"]["b"])

    velocity_max = enemy_config["velocity_max"]
    velocity_min = enemy_config["velocity_min"]
    velocity_range = random.randrange(velocity_min, velocity_max)
    velocity = pygame.Vector2(
        random.choice([-velocity_range, velocity_range]),
        random.choice([-velocity_range, velocity_range]))
    enemy_entity = create_square(world, size, position, velocity, color)
    world.add_component(enemy_entity, CTagEnemy())


def create_enemy_spawner(
        world: esper.World,
        level_config: dict):
    spawner_entity = world.create_entity()
    world.add_component(
        spawner_entity,
        CEnemySpawner(level_config["enemy_spawn_events"]))


def create_input_player(
        world: esper.World):
    input_left = world.create_entity()
    input_right = world.create_entity()
    input_up = world.create_entity()
    input_down = world.create_entity()
    input_fire = world.create_entity()

    world.add_component(
        input_left,
        CInputCommand("PLAYER_LEFT", pygame.K_LEFT)
    )

    world.add_component(
        input_right,
        CInputCommand("PLAYER_RIGHT", pygame.K_RIGHT)
    )

    world.add_component(
        input_up,
        CInputCommand("PLAYER_UP", pygame.K_UP)
    )

    world.add_component(
        input_down,
        CInputCommand("PLAYER_DOWN", pygame.K_DOWN)
    )

    world.add_component(
        input_fire,
        CInputCommand("PLAYER_FIRE", pygame.BUTTON_LEFT)
    )


def create_bullet_square(
        world: esper.World,
        position: pygame.Vector2,
        bullet_config: dict):

    size = pygame.Vector2(
        bullet_config["size"]["x"],
        bullet_config["size"]["y"])
    color = pygame.Color(
        bullet_config["color"]["r"],
        bullet_config["color"]["g"],
        bullet_config["color"]["b"])

    velocity = pygame.Vector2(bullet_config["velocity"])
    bullet_entity = create_square(world, size, position, velocity, color)
    world.add_component(bullet_entity, CTagBullet())
