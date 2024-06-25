from random import randint

import pygame

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption("Змейка")

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Class GameObject initializes Game Objects"""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        """Draw method 'draws' an object"""
        pass


class Apple(GameObject):
    """Object Apple, initialized on grid at random."""

    def __init__(self):
        self.position = self.randomize_postion()
        self.body_color = APPLE_COLOR

    def draw(self):
        """Draw method 'draws' an apple"""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def randomize_postion(self):
        """Method randomize_position randomizes apples position on the grid"""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE,
        )
        return self.position


class Snake(GameObject):
    """Object Snake, initialized on grid at random."""

    def __init__(self):
        self.positions = [
            (
                randint(0, SCREEN_WIDTH - 1) * GRID_SIZE,
                randint(0, SCREEN_HEIGHT - 1) * GRID_SIZE,
            )
        ]
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Update method updates snakes direction"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move method is responsible for snakes position on the grid"""
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
        """Draw method 'draws' a snake"""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    def get_head_position(self):
        """Get_head_positon method returns snake head's position"""
        return self.positions[0]

    def reset(self):
        """Reset method resets the game to initial settings"""
        return self.__init__()


# Функция обработки действий пользователя
def handle_keys(game_object):
    """Function handle keys handles keyboard activity"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Function main is the main game function"""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        snake.update_direction()
        snake.move()

        pygame.display.update()

        # Тут опишите основную логику игры
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_postion()
        elif snake.get_head_position() in snake.positions[1:]:
            snake.reset()


if __name__ == "__main__":
    main()
