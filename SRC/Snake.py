import tkinter as tk# Импорт библиотеки tkinter для создания графического интерфейса с псевдонимом tk
from tkinter import simpledialog# Импорт дополнительных модулей из tkinter
import random
WIDTH = 600  # Ширина игрового окна
HEIGHT = 400  # Высота игрового окна
SNAKE_SIZE = 10  # Размер сегмента змейки
#  Используемые цвета
BLUE = "#3299D5"
SNAKE_COLOR = "#00FF00"
EAT_COLOR = "#D53250"
SNAKE_COLOR_OUTLINE = "#00FFF0"
EAT_COLOR_OUTLINE = "#D5325F"
GROUND_COLOR = "#000000"
TXT_COLOR = "#FFFF66"
MENU_BG = "#2E8B57"
MENU_TEXT = "#FFFFFF"
# Глобальные переменные
difficulty = 5  # Сложность изначальная
player_name = ''  # Имя игрока
default_player_name = True  # Имя не установлено
# Определение основного класса игры "Змейка"
class SnakeGame:
    def __init__(self, root):# Инициализация объектов
        self.root = root# Сохранение ссылки на корневое окно tkinter
        self.root.title("ИГРА ЗМЕЙКА")# Установка заголовка окна
        self.root.geometry(f"{WIDTH}x{HEIGHT}")# Установка размеров окна
        self.root.resizable(False, False)# Запрет изменения размеров окна пользователем
        self.snake = []# Создание пустого списка для хранения координат сегментов змейки
        self.food = [0, 0]# 34. Координаты еды как списка [x, y]
        self.score = 0# Инициализация счета игры нулем
        self.length = 1# Инициализация начальной длины змейки
        self.game_running = False# Флаг, указывающий то что игра не запущена
        self.game_over = False# Флаг, указывающий то что игра не завершена
        self.create_widgets()# Вызов метода для создания виджетов интерфейса
        self.show_start_screen()# Вызов метода для отображения стартового экрана
    def create_widgets(self):# Метод для создания всех виджетов игры
        self.canvas = tk.Canvas(# Создание холста (Canvas) для рисования игровых объектов
            self.root,  # Родительский виджет
            width=WIDTH,
            height=HEIGHT,
            bg=GROUND_COLOR,
            highlightthickness=0  # Убираем обводку холста
        )
        self.canvas.pack()# Размещение холста в окне с помощью менеджера компоновки pack
        self.root.bind("<KeyPress>", self.on_key_press)# Привязка обработчика нажатий клавиш к корневому окну
    def show_start_screen(self):# Метод для отображения стартового меню
        self.clear_canvas()# Очистка холста от всех предыдущих элементов
        self.canvas.create_text(# Создание текстового элемента с названием игры
            WIDTH // 2, 50,  # Позиция по центру сверху
            text="ИГРА ЗМЕЙКА НА PYTHON <3",
            fill=SNAKE_COLOR,
            font=("Arial", 24, "bold")
        )
        self.start_button = tk.Button(# Создание кнопки "ИГРАТЬ"
            self.root,
            text="ИГРАТЬ",
            command=self.start_game_dialog,  # Функция при нажатии
            bg=MENU_BG,
            fg=MENU_TEXT,
            font=("Arial", 14),
            width=15,
            height=2
        )
        self.start_button_window = self.canvas.create_window(# Размещение кнопки на холсте в определенной позиции
            WIDTH // 2, 150,
            window=self.start_button  # Виджет для размещения
        )
        self.exit_button = tk.Button(# Создание кнопки "ВЫХОД"
            self.root,
            text="ВЫХОД",
            command=self.root.quit,  # Закрытие приложения
            bg=MENU_BG,
            fg=MENU_TEXT,
            font=("Arial", 14),
            width=15,
            height=2
        )
        self.exit_button_window = self.canvas.create_window(# Размещение кнопки выхода на холсте
            WIDTH // 2, 220,
            window=self.exit_button
        )
    def start_game_dialog(self):# Метод для отображения диалогов начала игры
        global player_name, default_player_name# Объявление глобальных переменных для их изменения
        name = simpledialog.askstring(# Отображение диалогового окна для ввода имени игрока
            "Имя игрока",
            "Введите ваше имя:",
            initialvalue="Змеёнышь" if default_player_name else player_name# Начальное значение: "Змеёнышь" если имя не установлено, иначе текущее имя
        )
        if name:# Проверка: ввел ли пользователь имя (не нажал Cancel)
            player_name = name# Сохранение введенного имени
            default_player_name = False# Сброс флага - имя теперь установлено
            difficulty_dialog = tk.Toplevel(self.root)# Создание нового диалогового окна для выбора сложности
            difficulty_dialog.title("Выбор сложности")
            difficulty_dialog.geometry("500x300")
            difficulty_dialog.resizable(False, False)
            difficulty_dialog.transient(self.root)# Связывание окна с родительским (будет поверх)!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            difficulty_dialog.grab_set()# Захват фокуса
            tk.Label(# Создание текстовой метки в диалоге сложности
                difficulty_dialog,  # Родительское окно
                text="Выберите сложность:",
                font=("Arial", 14)
            ).pack(pady=20)
            diff_var = tk.StringVar(value="Средняя")  # Значение по умолчанию
            difficulties = {# Словарь соответствия названий сложности и значений скорости
                "Лёгкая": 5,
                "Средняя": 15,
                "Тяжёлая": 30
            }
            for diff_text in difficulties:# Цикл для создания радиокнопок для каждого уровня сложности
                tk.Radiobutton(# Создание радиокнопки
                    difficulty_dialog,  # Родительское окно
                    text=diff_text,  # Текст рядом с кнопкой
                    variable=diff_var,  # Переменная для хранения выбора
                    value=diff_text,
                    font=("Arial", 12)
                ).pack(anchor='w', padx=50)
            def start_with_difficulty():# Вложенная функция для начала игры с выбранной сложностью
                global difficulty
                difficulty = difficulties[diff_var.get()]# Получение значения скорости по выбранному названию сложности
                difficulty_dialog.destroy()
                self.start_game()# Запуск игры
            tk.Button(# Создание кнопки для запуска игры
                difficulty_dialog,  # Родительское окно
                text="Начать игру",
                command=start_with_difficulty,
                bg=MENU_BG,
                fg=MENU_TEXT,
                font=("Arial", 12)
            ).pack(pady=20)
    def start_game(self):# Метод для начала новой игры
        self.clear_canvas()# Очистка холста от элементов меню
        self.snake = [[WIDTH // 2, HEIGHT // 2]]#Размещение змейки по центру
        self.food = self.generate_food()# Генерация первой еды
        self.direction = "Right"# Направления движения
        self.next_direction = "Left"
        self.score = 0# Сброс счета
        self.length = 1# Сброс длины змейки
        self.game_running = True# Установка флага то что игра запущена
        self.game_over = False# Сброс флага завершения игры
        self.canvas.focus_set()# Установка фокуса на холст для обработки клавиатуры
        self.game_loop()# Запуск основного игрового цикла
    def generate_food(self):# Метод для генерации случайной позиции еды
        x = round(random.randrange(0, WIDTH - SNAKE_SIZE) / 10.0) * 10.0# Генерация случайной координаты X
        y = round(random.randrange(0, HEIGHT - SNAKE_SIZE) / 10.0) * 10.0# Генерация случайной координаты Y
        return [x, y]# Возврат координат в виде списка [x, y]
    def draw_snake(self):# Метод для отрисовки змейки на холсте
        for segment in self.snake:# Цикл по всем сегментам змейки
            x, y = segment# Получение координат текущего сегмента
            self.canvas.create_oval(# Рисование прямоугольника для сегмента змейки
                x, y,  # Левый верхний угол
                x + SNAKE_SIZE, y + SNAKE_SIZE,  # Правый нижний угол
                fill=SNAKE_COLOR,
                outline=SNAKE_COLOR_OUTLINE#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            )
    def draw_food(self):# Метод для отрисовки еды на холсте
        x, y = self.food# Получение координат еды
        self.canvas.create_oval(# Рисование прямоугольника для еды
            x, y,  # Левый верхний угол
            x + SNAKE_SIZE, y + SNAKE_SIZE,  # Правый нижний угол
            fill=EAT_COLOR,
            outline=EAT_COLOR_OUTLINE
        )
    def draw_ui(self):# Метод для отрисовки пользовательского интерфейса
        self.canvas.create_text(# Отрисовка текста с текущим счетом
            60, 20,  # Позиция слева сверху
            text=f"Счёт: {self.score}",  # Текст со счетом
            fill=TXT_COLOR,
            font=("Arial", 12, "bold"),
            anchor="w"
        )
        self.canvas.create_text(# Отрисовка текста с именем игрока
            60, 40,
            text=f"Игрок: {player_name}",
            fill=TXT_COLOR,
            font=("Arial", 12),
            anchor="w"
        )
        self.canvas.create_text( # Отрисовка текста с текущей скоростью
            60, 60,
            text=f"Скорость: {difficulty}",
            fill=TXT_COLOR,
            font=("Arial", 12),
            anchor="w"
        )
        self.canvas.create_text(# Отрисовка подсказок по управлению внизу экрана
            WIDTH // 2, HEIGHT - 20,
            text="Управление: WASD/Стрелки, ESC-меню",
            fill=TXT_COLOR,
            font=("Arial", 10)
        )
    def on_key_press(self, event):# Метод-обработчик нажатий клавиш
        if not self.game_running:# Если игра не запущена - игнорировать нажатия
            return
        key = event.keysym# Получение символа нажатой клавиши из события
        if key in ("Left", "a", "A") and self.direction != "Right":
            self.next_direction = "Left"
        elif key in ("Right", "d", "D") and self.direction != "Left":
            self.next_direction = "Right"
        elif key in ("Up", "w", "W") and self.direction != "Down":
            self.next_direction = "Up"
        elif key in ("Down", "s", "S") and self.direction != "Up":
            self.next_direction = "Down"
        elif key == "Escape":
            self.game_over = True
            self.show_game_over_screen()
    def update_snake_position(self):# Метод для обновления позиции змейки
        head_x, head_y = self.snake[-1]# Получение координат головы змейки
        self.direction = self.next_direction# Обновление текущего направления движения
        # Изменение координат головы змейки при изменении движения
        if self.direction == "Left":
            head_x -= SNAKE_SIZE
        elif self.direction == "Right":
            head_x += SNAKE_SIZE
        elif self.direction == "Up":
            head_y -= SNAKE_SIZE
        elif self.direction == "Down":
            head_y += SNAKE_SIZE
        # Проверка столкновения с границами игрового поля
        if (head_x < 0 or head_x >= WIDTH or
                head_y < 0 or head_y >= HEIGHT):
            self.game_over = True
            self.show_game_over_screen()
            return False
        # Создание новой головы змейки
        new_head = [head_x, head_y]
        # Проверка столкновения головы с телом змейки
        if new_head in self.snake:
            self.game_over = True
            self.show_game_over_screen()
            return False
        self.snake.append(new_head)# Добавление новой головы в конец списка змейки
        # Проверка поедания еды
        if (abs(head_x - self.food[0]) < SNAKE_SIZE and
                abs(head_y - self.food[1]) < SNAKE_SIZE):
            self.score += 1
            self.length += 1
            self.food = self.generate_food()
        else:
            if len(self.snake) > self.length:
                self.snake.pop(0)
        return True
    # Основной игровой цикл
    def game_loop(self):
        if not self.game_running or self.game_over:
            return
        self.canvas.delete("all")# Очистка холста для перерисовки кадра
        if not self.update_snake_position():
            return
        # Отрисовка всех игровых объектов
        self.draw_food()
        self.draw_snake()
        self.draw_ui()
        if self.game_running and not self.game_over:# Планирование следующего кадра игры
            self.root.after(1000 // difficulty, self.game_loop)
    def show_game_over_screen(self):# Метод для отображения экрана завершения игры
        self.game_running = False
        self.clear_canvas()
        self.canvas.create_text(
            WIDTH // 2, HEIGHT // 3,
            text=f"ИГРА ЗАВЕРШЕНА! ВАШ СЧЁТ: {self.score}",
            fill=EAT_COLOR,  # Цвет
            font=("Arial", 20, "bold")
        )
        self.canvas.create_text(
            WIDTH // 2, HEIGHT // 3 + 40,
            text=f"Игрок: {player_name}",
            fill=BLUE,
            font=("Arial", 16)
        )

        # Создание кнопки "ИГРАТЬ СНОВА"
        self.restart_button = tk.Button(
            self.root,
            text="ИГРАТЬ СНОВА (C)",
            command=self.start_game,
            bg=MENU_BG,
            fg=MENU_TEXT,
            font=("Arial", 12),
            width=20
        )
        self.canvas.create_window(
            WIDTH // 2, HEIGHT // 2 + 40,
            window=self.restart_button
        )
        # Создание кнопки "В МЕНЮ"
        self.menu_button = tk.Button(
            self.root,
            text="В МЕНЮ (Q)",
            command=self.show_start_screen,
            bg=MENU_BG,
            fg=MENU_TEXT,
            font=("Arial", 12),
            width=20
        )
        self.canvas.create_window(
            WIDTH // 2, HEIGHT // 2 + 90,
            window=self.menu_button
        )
        # Привязка клавиши C для перезапуска игры
        self.root.bind("<KeyPress-c>", lambda e: self.start_game())
        self.root.bind("<KeyPress-C>", lambda e: self.start_game())
        # Привязка клавиши Q для возврата в меню
        self.root.bind("<KeyPress-q>", lambda e: self.show_start_screen())
        self.root.bind("<KeyPress-Q>", lambda e: self.show_start_screen())
    def clear_canvas(self):# Метод для полной очистки холста
        self.canvas.delete("all")# Удаление всех графических объектов с холста
        for widget in self.root.winfo_children():# Удаление всех кнопок из окна
            if isinstance(widget, tk.Button):# Проверка: является ли виджет кнопкой
                widget.destroy()  # Уничтожение кнопки
def main():# Основная функция программы
    root = tk.Tk()# Создание корневого окна tkinter
    game = SnakeGame(root)# Создание экземпляра игры SnakeGame
    root.eval('tk::PlaceWindow . center')# Центрирование окна на экране с помощью Tcl команды
    root.mainloop()# Запуск главного цикла обработки событий tkinter
if __name__ == "__main__":# Проверка: запущен ли этот файл как основной
    main()# Если да - вызываем основную функцию