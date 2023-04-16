from typing import Callable
import pygame
import esper
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity


def system_input_player(
        world: esper.World,
        event: pygame.event.Event,
        do_action: Callable[[CInputCommand], None]):

    # solo necesitamos un componente por ello es get_component en singular
    components = world.get_component(CInputCommand)

    for _, c_input in components:
        if event.type == pygame.KEYDOWN and c_input.key == event.key:
            c_input.phase = CommandPhase.START
            do_action(c_input)
        if event.type == pygame.KEYUP and c_input.key == event.key:
            c_input.phase = CommandPhase.END
            do_action(c_input)
