from typing import Callable
import pygame
import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_collision_player_enemy(
        world: esper.World,
        player_entity: int,
        level_config: dict) -> None:

    components = world.get_components(CSurface, CTransform, CTagEnemy)
    player_transform = world.component_for_entity(player_entity, CTransform)
    player_surface = world.component_for_entity(player_entity, CSurface)

    player_square = player_surface.surface.get_rect(
        topleft=player_transform.position)

    for enemy_entity, (component_surface, component_transform, _) in components:
        enemy_square = component_surface.surface.get_rect(
            topleft=component_transform.position)

        if enemy_square.colliderect(player_square):
            world.delete_entity(enemy_entity)
            player_transform.position.x = level_config["player_spawn"]["position"]["x"] - \
                player_surface.surface.get_width()/2
            player_transform.position.y = level_config["player_spawn"]["position"]["y"] - \
                player_surface.surface.get_height()/2
