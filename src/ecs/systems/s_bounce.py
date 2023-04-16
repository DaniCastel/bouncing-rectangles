import pygame
import esper
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_enemy import CTagEnemy


def system_screen_bounce(world: esper.World, screen: pygame.Surface):

    screen_rect = screen.get_rect()  # rectangulo de la pantalla

    # buscamos los componentes que tengan las caracteristicas que indicamos dentro de los parametros
    components = world.get_components(
        CTransform, CVelocity, CSurface, CTagEnemy)

    square_transform: CTransform
    square_velocity: CVelocity
    square_surface: CSurface

    for _, (square_transform, square_velocity, square_surface, square_enemy) in components:
        square_rect = square_surface.surface.get_rect(
            topleft=square_transform.position)  # topleft pra obtener la posición exacta del rectangulo

        # si la parte izq del cuadrado es menor a cero en la pantalla o si la parte derecha del cuadrado es mayor a lo que mide la antalla
        if square_rect.left < 0 or square_rect.right > screen_rect.width:
            square_velocity.velocity.x *= -1
            square_rect.clamp_ip(screen_rect)
            square_transform.position.x = square_rect.x

        if square_rect.top < 0 or square_rect.bottom > screen_rect.height:
            square_velocity.velocity.y *= -1
            square_rect.clamp_ip(screen_rect)
            square_transform.position.y = square_rect.y
