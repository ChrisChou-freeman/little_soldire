#! /usr/bin/env python
from engine import game


def main() -> None:
    _game = game.MainGame()
    _game.run()

if __name__ == '__main__':
    main()
