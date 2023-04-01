import json
import pygame

import esper
from src.create.prefabs_creator import create_square
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_bounce import system_screen_bounce
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_rendering import system_rendering


class GameEngine:
    def __init__(self) -> None:

        window_file = open('window.json')

        # returns JSON object as
        # a dictionary
        window_config = json.load(window_file)
        self.window_config = window_config

        pygame.init()
        pygame.display.set_caption(window_config["title"])
        self.screen = pygame.display.set_mode(
            (window_config["size"]["x"], window_config["size"]["y"]), pygame.SCALED)
        self.clock = pygame.time.Clock()

        self.is_running = False
        self.framerate = window_config["framerate"]
        self.delta_time = 0
        # # mundo que maneja los componentes y estructuras, agregar y borrar entidades etc
        self.ecs_world = esper.World()

    def run(self) -> None:
        self._create()
        self.is_running = True
        while self.is_running:
            self._calculate_time()
            self._process_events()
            self._update()
            self._draw()
        self._clean()

    def _create(self):
        create_square(self.ecs_world, pygame.Vector2(50, 50), pygame.Vector2(
            150, 100), pygame.Vector2(100, 100), pygame.Color(255, 255, 100))

        # self.velocity_square = pygame.Vector2(
        #     100, 100)  # 100px vel en x y 100px en Y

        # self.square_position = pygame.Vector2(150, 100)
        # size_square = pygame.Vector2(50, 50)
        # color_square = pygame.Color(255, 255, 100)

        # creamos la superficie o textura y pide un tamaño de coordenada
        # self.surface_square = pygame.Surface(size_square)

        # es igual que lo que indicamos en draw
        # self.surface_square.fill(color_square)

    def _calculate_time(self):
        # previamente creamos el reloj en el init

        self.clock.tick(self.framerate)  # movemos el reloj con el frame rate

        # si la velocidad es 0 va a ir lo mas rapido que pueda
        # en este caso seleccionamos 60 cuadros por segundo

        # Dividimos en 1000 para contar en segundos
        self.delta_time = self.clock.get_time()/1000.0

    def _process_events(self):
        for event in pygame.event.get():  # get retorna una lista de eventos
            if event.type == pygame.QUIT:  # cuando cierran la ventana
                self.is_running = False

    def _update(self):
        # modificamos la velocidad
        system_movement(self.ecs_world, self.delta_time)
        system_screen_bounce(self.ecs_world, self.screen)

    def _draw(self):
        color = self.window_config["color"]
        self.screen.fill((color["r"], color["g"], color["b"])
                         )  # se indica un color
        # sistema de dibujo
        system_rendering(self.ecs_world, self.screen)
        pygame.display.flip()  # presenta la pantalla

    def _clean(self):
        pygame.quit()  # limpia todo
