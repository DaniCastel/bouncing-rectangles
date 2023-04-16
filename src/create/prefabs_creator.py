import random
import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
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
        player_level_config: dict):

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
    world.add_component(player_entity, CTagPlayer)


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
    world.add_component(enemy_entity, CTagEnemy)
