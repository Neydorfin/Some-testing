class Cell:
    # Класс, представляющий отдельную ячейку на игровой доске
    def __init__(self, id_cell):
        self.id_cell = id_cell  # Номер ячейки
        self.value = None  # Значение в ячейке (крестик, нолик или None)

    def is_busy(self):
        # Проверка, занята ли ячейка
        return self.value is not None

    def __str__(self):
        # Строковое представление ячейки
        return "Cell {} is {}".format(self.id_cell, self.value)


class Board:
    # Класс, представляющий игровое поле (доску)
    def __init__(self):
        self.cells = []  # Список ячеек на доске
        for id_cell in range(1, 10):
            cell = Cell(id_cell)
            id_cell += 1
            self.cells.append(cell)

    # Очистка поля (заполняет все ячейки None)
    def clear(self):
        for cell in self.cells:
            cell.value = None

    # Проверка, заполнено ли поле
    def is_full(self):
        for cell in self.cells:
            if cell.value is None:
                return False
        else:
            return True

    def __str__(self):  # Визуализация игрового поля в виде строк
        border = "—" * 19
        first = "|{: ^5}|{: ^5}|{: ^5}|".format(*(cell.value
                                                  if cell.value is not None
                                                  else cell.id_cell
                                                  for cell in self.cells[:3]))
        second = "|{: ^5}|{: ^5}|{: ^5}|".format(*(cell.value
                                                   if cell.value is not None
                                                   else cell.id_cell
                                                   for cell in self.cells[3:6]))
        third = "|{: ^5}|{: ^5}|{: ^5}|".format(*(cell.value
                                                  if cell.value is not None
                                                  else cell.id_cell
                                                  for cell in self.cells[6:9]))

        return '\n'.join((border, first, border, second, border, third, border))


class Player:
    # Класс, представляющий игрока
    def __init__(self, mark):
        name = input("Введите имя игрока: ")
        self.name = name
        self.mark = mark  # Знак игрока (X или O)
        self.score = 0  # Счет игрока

    # Метод запроса номера ячейки, куда игрок хочет походить
    def move_were(self):
        try:
            id_cell = int(input(f"{self.name} введите на какое место вводить \"{self.mark}\":\n>>>"))
            return id_cell - 1
        except ValueError:
            print("Ввели неверное значение!")
            return self.move_were()

    # Метод совершения хода игрока
    def move(self, cell):
        if cell.is_busy():
            print("Клетка занята!")
            return False
        else:
            cell.value = self.mark
            return True


class Game:
    # Класс, представляющий игру
    def __init__(self):
        self.player1 = Player("X")  # Создание первого игрока с знаком X
        self.player2 = Player("O")  # Создание второго игрока с знаком O
        self.board = Board()  # Создание игровой доски

    # Метод проверки победы игрока с определенным знаком (mark) на текущей доске
    def check_win(self, mark):
        cells = tuple(self.board.cells)
        # for row1
        if cells[0].value == mark and cells[1].value == mark and cells[2].value == mark:
            return True
        # for row2
        elif cells[3].value == mark and cells[4].value == mark and cells[5].value == mark:
            return True
        # for row3
        elif cells[6].value == mark and cells[7].value == mark and cells[8].value == mark:
            return True
        # for Colm1
        elif cells[0].value == mark and cells[3].value == mark and cells[6].value == mark:
            return True
        # for Colm 2
        elif cells[1].value == mark and cells[4].value == mark and cells[7].value == mark:
            return True
        # for colm 3
        elif cells[2].value == mark and cells[5].value == mark and cells[8].value == mark:
            return True
        # daignole 1
        elif cells[0].value == mark and cells[4].value == mark and cells[8].value == mark:
            return True
        # daignole 2
        elif cells[2].value == mark and cells[4].value == mark and cells[6].value == mark:
            return True
        else:
            return False

    # Метод запроса продолжения игры у игроков
    def ask_next(self):
        ans = input("Хотите продолжить y\\n:\n>>>")
        if ans.lower() == 'y':
            self.play()
        elif ans.lower() == 'n':
            print("Игра закончилась!")
        else:
            print("Вы вели неверную команду!")
            self.ask_next()

    # Метод запуска одного хода игры. Получает одного из игроков, запрашивает у игрока номер клетки,
    # изменяет поле, проверяет, выиграл ли игрок. Если игрок победил, возвращает True, иначе False.
    def next_move(self, player):
        print(self.board)
        try:
            id_cell = player.move_were()
            move = player.move(self.board.cells[id_cell])

            if not move:
                self.next_move(player)

        except IndexError:
            print("Вы ввели неверный диапазон")
            self.next_move(player)
        if self.check_win(player.mark):
            return True
        else:
            return False

    # Метод запуска одной игры. Очищает поле, запускает цикл с игрой, который завершается победой
    # одного из игроков или ничьей. Если игра завершена, метод возвращает True, иначе False.
    def game(self):
        players = (self.player1, self.player2)
        print("Игра начинается!")
        self.board.clear()
        while True:
            for player in players:
                if self.next_move(player):
                    print("Победил {}".format(player.name))
                    player.score += 1
                    return True

                if self.board.is_full():
                    print("Ничья!")
                    return True

    # Основной метод запуска игр. В цикле запускает игры, запрашивая после каждой игры, хотят ли
    # игроки продолжать играть. После каждой игры выводится текущий счёт игроков.
    def play(self):
        if self.game():
            print("Счет: \n{: ^5} | {: ^5}".format(self.player1.name, self.player2.name))
            print("{: ^5} | {: ^5}".format(self.player1.score, self.player2.score))
        else:
            print("Что то пошло не так!")
        self.ask_next()
