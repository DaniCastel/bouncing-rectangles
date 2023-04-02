from random import randrange
import random
import pygame
import esper
from src.create.prefabs_creator import create_square
from src.ecs.components.c_enemy_spawner import CEnemySpawner


def system_enemy_spawner(ecs_world: esper.World, delta_time, enemies, start_time):
    components = ecs_world.get_components(CEnemySpawner)

    enemy_spawner: CEnemySpawner
    enemy_spawner = components[0][1][0]

    current_seconds = pygame.time.get_ticks()/1000

    for event in enemy_spawner.events:
        if (current_seconds >= event.time and event.already_created == False):
            enemy = enemies[event.enemy_type]
            color = enemy["color"]

            velocity_x = random.randint(
                enemy["velocity_min"], enemy["velocity_max"])*positive_or_negative()
            velocity_y = random.randint(
                enemy["velocity_min"], enemy["velocity_max"])*positive_or_negative()

            create_square(ecs_world, pygame.Vector2(enemy["size"]["x"], enemy["size"]["y"]), pygame.Vector2(
                event.position["x"], event.position["y"]), pygame.Vector2(velocity_x, velocity_y), pygame.Color(color["r"], color["g"], color["b"]))
            event.already_created = True


def positive_or_negative():
    if random.random() < 0.5:
        return 1
    else:
        return -1
