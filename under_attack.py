class Chessboard():

    FIRST_LETTER_CODE = ord('A')
    LETTERS_CNT = 26

    def __init__(self, size = 8):
        self.SIZE = min(size, self.LETTERS_CNT)
        self.letter_idx = [
            chr(ucode + self.FIRST_LETTER_CODE)
            for ucode in range(self.SIZE)
        ]
        self._board_clear()
        self.figures_card = dict()

    def _board_clear(self):
         self.board = [['0' for i in range(self.SIZE)] for j in range(self.SIZE)]

    def clear(self):
        self.figures_card.clear()
        self._board_clear()

    def field_verify(self, place:str):
        '''Проверка попадания в поле. Возвращает абстрактные координаты'''

        if len(place) not in (2, 3):
            return [None, None]
        # if len(place) == 2:
        #     y = int(place[1]) - 1
        # elif len(place) == 3:

        y = int(place[1:]) - 1           
        if (
            (place[0] not in self.letter_idx) or
            y not in range(len(self.letter_idx))
        ):
            return [None, None]
        x = self.letter_idx.index(place[0])
        return [x, y]

    def put_figure(self, Figure, place:str):
        '''Функция установки фигур на доске. Размещает полученную фигуру
        в поле и в списке фигур'''

        x, y = self.field_verify(place)
        if x is not None:
            self.board[y][x] = Figure.name[0] #symb()
            self.figures_card[Figure] = [x, y]

        return [x, y]

    def figures_attack(self):
        attack_field_cnt = 0
        for fig in self.figures_card:
            # Перебор фигур на доске

            for attack_dir in fig.under_attack(self.SIZE):
                # Перебор направлений атаки для фигуры

                for idx in range(len(attack_dir)):
                    #Проверка направления
                    x = self.figures_card[fig][0] + attack_dir[idx][0]

                    if x not in range(self.SIZE):
                        break
                    y = self.figures_card[fig][1]+ attack_dir[idx][1]
                    if y not in range(self.SIZE):
                        break
                    if self.board[y][x] == '1':
                        continue
                    elif self.board[y][x] == '0':
                        self.board[y][x] = '1'
                        attack_field_cnt += 1
                        continue
                    break
        return attack_field_cnt


class ChessMan:
    '''Шахматная фигура'''
    SYMB_UCODE_BLACK = 0
    SYMB_UCODE_WHITE = 0

    def __init__(self, name:str):
        self.name = name
    def __str__(self):
        return self.name

    def symb(self):
        return chr(self.SYMB_UCODE_WHITE)
        

class Castle(ChessMan):
    '''Ладья'''

    SYMB_UCODE_BLACK = 9814
    SYMB_UCODE_WHITE = 9820

    def under_attack(self, b_size):
        '''Список полей атаки ладьи'''

        attack_list = []
        attack_dir = [[i, 0] for i in range(1, b_size)]
        attack_list.append(attack_dir)
        attack_dir = [[-i, 0] for i in range(1, b_size)]
        attack_list.append(attack_dir)
        attack_dir = [[0, i] for i in range(1, b_size)]
        attack_list.append(attack_dir)
        attack_dir = [[0, -i] for i in range(1, b_size)]
        attack_list.append(attack_dir)
        return attack_list

 
class Elephant(ChessMan):
    '''Слон'''

    SYMB_UCODE_BLACK = 9815
    SYMB_UCODE_WHITE = 9821

    def under_attack(self, b_size):
        '''Список полей атаки слона'''

        attack_list = []
        attack_dir = [[i, i] for i in range(1, b_size)]
        attack_list.append(attack_dir)
        attack_dir = [[-i, i] for i in range(1, b_size)]
        attack_list.append(attack_dir)
        attack_dir = [[i, -i] for i in range(1, b_size)]
        attack_list.append(attack_dir)
        attack_dir = [[-i, -i] for i in range(1, b_size)]
        attack_list.append(attack_dir)
        return attack_list


class Queen(Elephant, Castle):
    '''Ферзь'''

    SYMB_UCODE_WHITE = 9819
    SYMB_UCODE_BLACK = 9813

    def under_attack(self, b_size):
        '''Список полей атаки ферзя'''
        
        attack_list = Elephant.under_attack(self, b_size)
        attack_list.extend(Castle.under_attack(self, b_size))

        return attack_list


class Horse(ChessMan):
    '''Лошадь'''

    SYMB_UCODE_BLACK = 9816
    SYMB_UCODE_WHITE = 9822

    # Куда ходит:
    horse_step = (
        ((1, 2),), ((1, -2),), ((2, 1),), ((2, -1),), ((-1, 2),), ((-1, -2),), ((-2, 1),), ((-2, -1),)
    )

    def under_attack(self, b_size):
        '''Список полей атаки коня'''

        return self.horse_step


class King(ChessMan):
    '''Лошадь'''

    SYMB_UCODE_BLACK = 9816
    SYMB_UCODE_WHITE = 9822

    # Куда ходит:
    king_step = (
        ((0, 1),), ((0, -1),), ((1, 1),), ((1, 0),), ((1, -1),), ((-1, 1),), ((-1, 0),), ((-1, -1),)
    )

    def under_attack(self, b_size):
        '''Список полей атаки короля'''

        return self.king_step


def runner():

    Chessboard1 = Chessboard(8)
    Queen1 = Queen('Queen')
    Castle1 = Castle('Castle')
    Horse1 = Horse('Horse')
    Elephant1 = Elephant('Elephant')
    King1 = King('King')

    figures_set = [Queen1, Castle1, Horse1]

    input_places_sets = [
        'D1 D3 E5',
        'A1 H8 B6',
        'H7 F8 G6',
        'F6 E4 H1',
        # 'F2 D4 E6'
    ]

    for input_set in input_places_sets:
        places_list = input_set.split(' ')

        Chessboard1.clear()
        print()

        figures_names_set = []
        for i in range(min(len(places_list), len(figures_set))):
            # Ставим фигуры на поле
            Chessboard1.put_figure(figures_set[i], places_list[i])
            figures_names_set.append(figures_set[i].name)
        print('Фигуры в игре: ',' '.join(figures_names_set))
        print('Поля фигур: ', ' '.join(places_list[:i+1]))

        # Включаем атаку фигур
        attack_cnt = Chessboard1.figures_attack()

        # Вывод доски с полями атаки
        print('    ',' '.join(Chessboard1.letter_idx))
        for i in range(Chessboard1.SIZE):
            print(f'{i+1:{0}{2}}  ',' '.join(Chessboard1.board[i]))
        print('Число полей атаки: ', attack_cnt)


if __name__ == '__main__':
    runner()

