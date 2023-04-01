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
        color: pygame.Vector2):

    square_entity = ecs_world.create_entity()
    # normalmente hay un componente por entidad
    ecs_world.add_component(
        square_entity, CSurface(size, color))

    # pero vamos a crear otro componente
    ecs_world.add_component(
        square_entity, CTransform(position))

    ecs_world.add_component(
        square_entity, CVelocity(velocity))

    # velocity_square = pygame.Vector2(
    #     100, 100)  # 100px vel en x y 100px en Y

    # self.square_position = pygame.Vector2(150, 100)
    # size_square = pygame.Vector2(50, 50)
    # color_square = pygame.Color(255, 255, 100)

    # creamos la superficie o textura y pide un tamaño de coordenada
    # self.surface_square = pygame.Surface(size_square)

    # es igual que lo que indicamos en draw
    # self.surface_square.fill(color_square)
