
# entidad
# adquirir lista
# iterar sobre la lista

import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform


def system_rendering(world: esper.World, screen: pygame.Surface):
    # solicita una tupla de los componentes que necesitamos
    components = world.get_components(CTransform, CSurface)

    square_transform: CTransform
    square_surface: CSurface

    for entity, (square_transform, square_surface) in components:
        screen.blit(square_surface.surface, square_transform.position)
