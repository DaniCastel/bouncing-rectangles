import json
import pygame

import esper
from src.create.prefabs_creator import create_bullet_square, create_enemy_spawner, create_input_player, create_player_square, create_square
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_bounce import system_screen_bounce
from src.ecs.systems.s_collision_player_enemy import system_collision_player_enemy
from src.ecs.systems.s_input_player import system_input_player
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_player_limits import system_player_limits
from src.ecs.systems.s_rendering import system_rendering
from src.ecs.systems.s_system_enemy_spawner import system_enemy_spawner


class GameEngine:
    def __init__(self) -> None:
        self._load_config_files()

        pygame.init()
        pygame.display.set_caption(self.window_config["title"])
        self.screen = pygame.display.set_mode(
            (self.window_config["size"]["w"], self.window_config["size"]["h"]), pygame.SCALED)
        self.clock = pygame.time.Clock()
        self.is_running = False
        self.framerate = self.window_config["framerate"]
        self.delta_time = 0
        # # mundo que maneja los componentes y estructuras, agregar y borrar entidades etc
        self.ecs_world = esper.World()

    def _load_config_files(self):
        with open('assets/cfg/window.json', encoding="utf-8") as window_file:
            self.window_config = json.load(window_file)
        with open('assets/cfg/enemies.json', encoding="utf-8") as enemies_file:
            self.enemies_config = json.load(enemies_file)
        with open('assets/cfg/level_01.json', encoding="utf-8") as level_file:
            self.level_config = json.load(level_file)
        with open('assets/cfg/player.json', encoding="utf-8") as player_file:
            self.player_config = json.load(player_file)
        with open('assets/cfg/bullet.json', encoding="utf-8") as bullet_file:
            self.bullet_config = json.load(bullet_file)

    def run(self) -> None:
        self._create()
        self.is_running = True
        self.start_time = pygame.time.get_ticks()
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        self._player_entity = create_player_square(self.ecs_world, self.player_config,
                                                   self.level_config["player_spawn"])
        self._player_component_velocity = self.ecs_world.component_for_entity(
            self._player_entity, CVelocity)
        self._player_component_transform = self.ecs_world.component_for_entity(
            self._player_entity, CTransform)
        self._player_component_size = self.ecs_world.component_for_entity(
            self._player_entity, CSurface)
        create_enemy_spawner(self.ecs_world, self.level_config)
        create_input_player(self.ecs_world)

    def _calculate_time(self):
        # previamente creamos el reloj en el init

        self.clock.tick(self.framerate)  # movemos el reloj con el frame rate

        # si la velocidad es 0 va a ir lo mas rapido que pueda
        # en este caso seleccionamos 60 cuadros por segundo

        # Dividimos en 1000 para contar en segundos
        self.delta_time = self.clock.get_time()/1000.0

    def _process_events(self):
        for event in pygame.event.get():  # get retorna una lista de eventos
            system_input_player(self.ecs_world, event, self._do_action)
            if event.type == pygame.QUIT:  # cuando cierran la ventana
                self.is_running = False

    def _update(self):
        system_enemy_spawner(
            self.ecs_world,
            self.enemies_config,
            self.delta_time,
        )
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)
        system_player_limits(self.ecs_world, self.screen,
                             self._player_component_velocity, self.player_config)
        system_collision_player_enemy(
            self.ecs_world, self._player_entity, self.level_config)
        self.ecs_world._clear_dead_entities()

    def _draw(self):
        color = self.window_config["bg_color"]
        self.screen.fill((color["r"], color["g"], color["b"])
                         )  # se indica un color
        # sistema de dibujo
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()  # presenta la pantalla

    def _clean(self):
        self.ecs_world.clear_database()
        pygame.quit()  # limpia todo

    def _do_action(self, c_input: CInputCommand):
        if c_input.name == "PLAYER_LEFT":
            if c_input.phase == CommandPhase.START:
                self._player_component_velocity.velocity.x -= self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_component_velocity.velocity.x = 0

        if c_input.name == "PLAYER_RIGHT":
            if c_input.phase == CommandPhase.START:
                self._player_component_velocity.velocity.x += self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_component_velocity.velocity.x = 0

        if c_input.name == "PLAYER_UP":
            if c_input.phase == CommandPhase.START:
                self._player_component_velocity.velocity.y -= self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_component_velocity.velocity.y = 0

        if c_input.name == "PLAYER_DOWN":
            if c_input.phase == CommandPhase.START:
                self._player_component_velocity.velocity.y += self.player_config["input_velocity"]
            elif c_input.phase == CommandPhase.END:
                self._player_component_velocity.velocity.y = 0

        if c_input.name == "PLAYER_FIRE":
            print(self._player_component_transform.position.x)
            print(self._player_component_transform.position.y)

            size = self._player_component_size.surface.get_size()

            print(size)

            create_bullet_square(
                self.ecs_world,
                pygame.Vector2(
                    self._player_component_transform.position.x -
                    (size[0] / 2),
                    self._player_component_transform.position.x - (size[1] / 2)),
                self.bullet_config)
