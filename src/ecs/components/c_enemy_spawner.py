import json
import pygame

from src.create.spawn_event_data import SpawnEventData


class CEnemySpawner:
    def __init__(self) -> None:
        self.events = []

        spawns_file = open('level_01.json')
        spawns = json.load(spawns_file)["enemy_spawn_events"]

        for spawn in spawns:
            self.events.append(SpawnEventData(
                spawn["time"], spawn["enemy_type"], spawn["position"]))
