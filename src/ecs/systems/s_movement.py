import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_movement(world: esper.World, delta_time: float):
    components = world.get_components(CTransform, CVelocity)

    square_transform: CTransform
    square_velocity: CVelocity

    for entity, (square_transform, square_velocity) in components:
        # lo unico que podemos cambiar para que el objeto se mueva es su posicion
        # avanzamos en x a 100px por segundo (delta_time)
        square_transform.position.x += square_velocity.velocity.x * delta_time
        square_transform.position.y += square_velocity.velocity.y * delta_time
