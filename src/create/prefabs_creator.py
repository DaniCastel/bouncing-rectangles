import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


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
    create_square(world, size, position, velocity, color)
