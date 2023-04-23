import pygame


class CSurface:
    def __init__(self, size: pygame.Vector2, color: pygame.color) -> None:
        self.surface = pygame.Surface(size)
        self.surface.fill(color)

    @classmethod
    def from_surface(cls, surface: pygame.Surface):
        c_surf = cls(pygame.Vector2(0, 0), pygame.Color(0, 0, 0))
        c_surf.surf = surface
        return c_surf
