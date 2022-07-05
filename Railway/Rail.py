import pygame
from pygame import gfxdraw


class Rail:
    def __init__(self, Stops, RailElements, ordered_elements, screen, color):
        self.stops = Stops
        self.railway_elements = RailElements
        self.ordered_elements = ordered_elements
        self.screen = screen
        self.color = color

    def draw(self):
        self.draw_railway()
        self.draw_stops()

    def draw_railway(self):
        for key, data in self.railway_elements.items():
            if key == 'arc':
                for value in data:
                    gfxdraw.arc(self.screen, value['x'], value['y'], value['radius'], value['start_angle'],
                                value['end_angle'], self.color)
            if key == 'line':
                for value in data:
                    pygame.draw.line(self.screen, self.color, value['start'], value['end'], 1)

    def draw_stops(self):
        for i in range(len(self.stops)):
            rect = pygame.Rect(self.stops[i].Rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect)