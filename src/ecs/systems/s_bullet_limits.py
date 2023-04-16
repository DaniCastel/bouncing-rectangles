import pygame
import esper
from src.ecs.components.c_input_command import CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet


def system_bullet_limits(world: esper.World, screen: pygame.Surface):

    screen_rect = screen.get_rect()  # rectangulo de la pantalla

    # buscamos los componentes que tengan las caracteristicas que indicamos dentro de los parametros
    components = world.get_components(
        CTransform, CSurface, CTagBullet)

    square_transform: CTransform
    square_surface: CSurface

    for bullet_entity, (square_transform, square_surface, square_bullet) in components:
        square_rect = square_surface.surface.get_rect(
            topleft=square_transform.position)  # topleft pra obtener la posición exacta del rectangulo

        if square_rect.left < 0 or square_rect.right > screen_rect.width or square_rect.top < 0 or square_rect.bottom > screen_rect.height:
            world.delete_entity(bullet_entity)
