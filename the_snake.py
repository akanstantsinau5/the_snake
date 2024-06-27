"""
This module provides functionality for generating random grid
positions using randint and pygame intitialization and display setup.
"""
from random import randint
import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 10

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption("Змейка")

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Initialize the parent class."""

    def __init__(self) -> None:
        """Initializes instance of a class."""
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Method draws an object of a class on grid."""


class Apple(GameObject):
    """Class Apple, parent class GameObject."""

    def __init__(self, snake=None):
        if snake is None:
            snake = Snake()
        """Initialize class Apple."""
        self.snake = snake
        self.position = self.randomize_position()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Method draws an Apple object."""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_position(self):
        """Method randomized position of the Apple object on the grid."""
        while True:
            position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
            )
            if not self.snake.position_check(position):
                return position


class Snake(GameObject):
    """Class Snake, parent class GameObject."""

    def __init__(self):
        """Initialize class Snake."""
        return self.reset()

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Method updates objects direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Method responsible for objects position on the grid."""
        head_dx, head_dy = self.get_head_position()
        direction_dx, direction_dy = self.direction
        self.position = (
            (head_dx + direction_dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_dy + direction_dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, self.position)
        if len(self.positions) - 1 > self.length:
            self.positions.pop()

    # Метод draw класса Snake
    def draw(self):
        """Method draws a Snake object."""
        for position in self.positions[:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.get_head_position(), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Methods returns Snakes position."""
        return self.positions[0]

    def position_check(self, position):
        """This method checks if position is occupied by snake"""
        return position in self.positions

    def reset(self):
        """Method resets the game to initial settings."""
        self.position = (randint(0, SCREEN_WIDTH - 1) * GRID_SIZE,
                         randint(0, SCREEN_HEIGHT - 1) * GRID_SIZE)
        self.positions = [self.position]
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Function handles keyboard activity."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Main game function."""
    # Инициализация PyGame:
    pg.init()
    snake = Snake()
    apple = Apple(snake)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.position = apple.randomize_position()
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.position = apple.randomize_position()

        apple.draw()
        snake.draw()
        pg.display.update()


if __name__ == "__main__":
    main()
