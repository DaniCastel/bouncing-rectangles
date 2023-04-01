import pygame


class SpawnEventData:
    def __init__(self, time, enemy_type, position) -> None:
        self.time = time
        self.enemy_type = enemy_type
        self.position = position
