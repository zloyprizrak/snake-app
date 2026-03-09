import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.label import Label

GRID_SIZE = 20
GRID_WIDTH = 30
GRID_HEIGHT = 30


class SnakeGame(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        Window.bind(on_key_down=self.key_control)

        self.label = Label(
            text="Score: 0",
            size_hint=(1, None),
            height=40,
            pos=(0, Window.height - 40)
        )
        self.add_widget(self.label)

        self.restart()

    def restart(self):

        self.snake = [(10, 10), (9, 10), (8, 10)]
        self.direction = (1, 0)

        self.score = 0
        self.label.text = "Score: 0"

        self.food = self.spawn_food()

        self.game_speed = 0.15

        Clock.unschedule(self.update)
        Clock.schedule_interval(self.update, self.game_speed)

    def spawn_food(self):

        while True:
            food = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )

            if food not in self.snake:
                return food

    def update(self, dt):

        head = self.snake[0]

        new_head = (
            head[0] + self.direction[0],
            head[1] + self.direction[1]
        )

        # столкновение со стеной
        if (
            new_head[0] < 0
            or new_head[1] < 0
            or new_head[0] >= GRID_WIDTH
            or new_head[1] >= GRID_HEIGHT
        ):
            self.game_over()
            return

        # столкновение с собой
        if new_head in self.snake:
            self.game_over()
            return

        self.snake.insert(0, new_head)

        if new_head == self.food:

            self.score += 1
            self.label.text = f"Score: {self.score}"

            self.food = self.spawn_food()

            # ускорение игры
            self.game_speed = max(0.05, self.game_speed - 0.005)

            Clock.unschedule(self.update)
            Clock.schedule_interval(self.update, self.game_speed)

        else:
            self.snake.pop()

        self.draw()

    def draw(self):

        self.canvas.clear()

        with self.canvas:

            # змейка
            Color(0, 1, 0)

            for segment in self.snake:
                Rectangle(
                    pos=(segment[0] * GRID_SIZE, segment[1] * GRID_SIZE),
                    size=(GRID_SIZE, GRID_SIZE)
                )

            # еда
            Color(1, 0, 0)

            Rectangle(
                pos=(self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE),
                size=(GRID_SIZE, GRID_SIZE)
            )

    def key_control(self, window, key, *args):

        if key == 273 and self.direction != (0, -1):  # вверх
            self.direction = (0, 1)

        elif key == 274 and self.direction != (0, 1):  # вниз
            self.direction = (0, -1)

        elif key == 276 and self.direction != (1, 0):  # влево
            self.direction = (-1, 0)

        elif key == 275 and self.direction != (-1, 0):  # вправо
            self.direction = (1, 0)

    def on_touch_down(self, touch):

        # если игра закончена — перезапуск
        if "Game Over" in self.label.text:
            self.restart()
            return

        x = touch.x - Window.width / 2
        y = touch.y - Window.height / 2

        if abs(x) > abs(y):

            if x > 0 and self.direction != (-1, 0):
                self.direction = (1, 0)

            elif x < 0 and self.direction != (1, 0):
                self.direction = (-1, 0)

        else:

            if y > 0 and self.direction != (0, -1):
                self.direction = (0, 1)

            elif y < 0 and self.direction != (0, 1):
                self.direction = (0, -1)

    def game_over(self):

        self.label.text = f"Game Over | Score: {self.score} | Tap to restart"
        Clock.unschedule(self.update)


class SnakeApp(App):

    def build(self):
        Window.size = (600, 600)
        return SnakeGame()


SnakeApp().run()