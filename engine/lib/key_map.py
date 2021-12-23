import pygame
from pygame import event

class KeyMap:
    def __init__(self, key_kent: event.Event) -> None:
        self._key_event = key_kent

    # key states
    def _key_press(self) -> bool:
        return self._key_event.type == pygame.KEYDOWN
    def _key_release(self) -> bool:
        return self._key_event.type == pygame.KEYUP
    # key states eng

    # direction keys
    def _key_left(self) -> bool:
        return self._key_event.key in [pygame.K_a, pygame.K_LEFT]
    def _key_right(self) -> bool:
        return self._key_event.key in [pygame.K_d, pygame.K_RIGHT]
    def _key_up(self) -> bool:
        return self._key_event.key in [pygame.K_w, pygame.K_UP]
    def _key_down(self) -> bool:
        return self._key_event.key in [pygame.K_s, pygame.K_DOWN]
    def key_right_press(self) -> bool:
        return self._key_press() and self._key_right()
    def key_right_release(self) -> bool:
        return self._key_release() and self._key_right()
    def key_left_press(self) -> bool:
        return self._key_press() and self._key_left()
    def key_left_release(self) -> bool:
        return self._key_release() and self._key_left()
    def key_up_press(self) -> bool:
        return self._key_press() and self._key_up()
    def key_down_press(self) -> bool:
        return self._key_press() and self._key_down()
    # direction keys end

    # action keys
    def key_attack_press(self) -> bool:
        return self._key_press() and self._key_event.key == pygame.K_j
    def key_attack_release(self) -> bool:
        return self._key_release() and self._key_event.key == pygame.K_j
    def key_jump_press(self) -> bool:
        return self._key_press() and self._key_event.key == pygame.K_k
    # action keys eng

    # other function key
    def key_back_press(self) -> bool:
        return self._key_press() and self._key_event.key == pygame.K_ESCAPE
    def key_enter_press(self) -> bool:
        return self._key_press() and self._key_event.key == pygame.K_RETURN
    def key_g_press(self) -> bool:
        return self._key_press() and self._key_event.key == pygame.K_g
    def key_q_press(self) -> bool:
        return self._key_press() and self._key_event.key == pygame.K_q
    def key_s_press(self) -> bool:
        return self._key_press() and self._key_event.key == pygame.K_s
    def key_c_press(self) -> bool:
        return self._key_press() and self._key_event.key == pygame.K_c
    # other function key end
