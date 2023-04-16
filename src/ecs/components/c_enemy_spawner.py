import json


class CEnemySpawner:
    def __init__(self, spawns_config: dict) -> None:
        self.events = []

        for spawn in spawns_config:
            self.events.append(SpawnEventData(
                spawn["time"], spawn["enemy_type"], spawn["position"]))


class SpawnEventData:
    def __init__(self, time, enemy_type, position) -> None:
        self.position = position
        self.enemy_type = enemy_type
        self.time = time
        self.already_created = False
