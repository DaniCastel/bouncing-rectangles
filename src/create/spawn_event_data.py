import pygame


class SpawnEventData:
    def __init__(self, time, enemy_type, position) -> None:
        self.position = position
        self.enemy_type = enemy_type
        self.time = time
        self.already_created = False
