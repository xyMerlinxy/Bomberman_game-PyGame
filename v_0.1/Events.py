import pygame

PLAYER_0_INSENSITIVITY_OFF = pygame.USEREVENT + 1
PLAYER_1_INSENSITIVITY_OFF = pygame.USEREVENT + 2
PLAYER_2_INSENSITIVITY_OFF = pygame.USEREVENT + 3
PLAYER_3_INSENSITIVITY_OFF = pygame.USEREVENT + 4


def creat_event(event_id: int, _dict: dict = None):
    return pygame.event.Event(event_id, _dict)


def rise_event(event_id: int, delay: int = 0):
    pygame.time.set_timer(pygame.event.Event(event_id), delay)
