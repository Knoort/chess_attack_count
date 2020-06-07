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
        y = int(place[1]) - 1
        if (
            (len(place) != 2) or
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
        if x is None:
            return

        self.board[y][x] = Figure.name[0] #symb()
        self.figures_card[Figure] = [x, y]

    def figures_attack(self):
        for fig in self.figures_card:
            print()
            for attack_dir in fig.under_attack(self.SIZE):
                # print(attack_dir)
                for idx in range(len(attack_dir)):
                    x = self.figures_card[fig][0] + attack_dir[idx][0]
                    if x not in range(self.SIZE):
                        break
                    y = self.figures_card[fig][1]+ attack_dir[idx][1]
                    if y not in range(self.SIZE):
                        break
                    if self.board[y][x] == '1':
                        print('continue')
                        continue
                    elif self.board[y][x] == '0':
                        self.board[y][x] = '1'
                        print('set 1')
                        continue
                    break


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


class Queen(Elephant):
    '''Ферзь'''

    SYMB_UCODE_WHITE = 9819
    SYMB_UCODE_BLACK = 9813

    def under_attack(self, b_size):
        '''Список полей атаки ферзя'''
        print(b_size)
        attack_list = []
        # attack_list.append(Castle.under_attack(b_size))
        attack_list = super().under_attack(b_size)
        return attack_list


class Horse(ChessMan):
    '''Лошадь'''

    SYMB_UCODE = 9822

    # Куда ходит:
    horse_code = (
        +1, +2, -2, -1
    )

    def _create_horse_list(self, x, y):
        '''Функция коня. Получает абстрактные координаты,
         возвращает список полей под атакой.'''

        fields_list = []
        for bin_code in range(2 ** 4):
            i = (bin_code >> 2) & 0b11
            j = bin_code & 0b11

            if (
                (i == j) or
                (i == (~j) & 0b11)
            ):
                continue
            dx = x + self.horse_code[i]
            dy = y + self.horse_code[j]
            if (
                dx in range(self.BOARD_SIZE) and
                dy in range(self.BOARD_SIZE)
            ):
                fields_list.append([dx, dy])

        return fields_list

    def under_attack(self, place:str):
        # Передаем список функций атаки фигуры
        fields_list = self._func_stack(place, self._create_horse_list)
        return fields_list

def dupl_rm(fields_list):
    '''Функция удаления дубликатов.'''
    uniq_list = []
    for i in range(len(fields_list)):
        if fields_list[i] not in uniq_list:
            uniq_list.append(fields_list[i])

    return uniq_list

def attack_set_calc(places_set:str, *figures):

    places_list = places_set.split(' ')
    if len(places_list) != len(figures):
        return []
    # Собираем список
    fields_list = []
    for idx in range(len(places_list)):
        fields_list.extend(figures[idx].under_attack(places_list[idx]))
        fields_list = dupl_rm(fields_list)
    # Удаляем поля фигур
    for idx in range(len(places_list)):
        x, y = figures[idx].field_verify(places_list[idx])
        if [x, y] in fields_list:
            fields_list.remove([x, y])

    return fields_list


def runner():

    Chessboard1 = Chessboard(8)
    Queen1 = Queen('Queen')
    Castle1 = Castle('Castle')
    # Castle2 = Castle('Castle')
    Elephant1 = Elephant('Elephant')
    # Horse1 = Horse('Horse')

    figures_set = [Queen1, Elephant1]

    input_places_sets = [
        # 'D1 D3 E5',
        # 'A1 H8 B6',
        # 'H7 F8 G6',
        'C5 F5 G2'
    ]

    places_list = input_places_sets[0].split(' ')
    print(places_list)

    place_idx = [
        Chessboard1.put_figure(figures_set[i], places_list[i])
        for i in range(min(len(places_list), len(figures_set)))
    ]
    print(place_idx)
    print(Chessboard1.figures_card)

    print('    ',' '.join(Chessboard1.letter_idx))
    for i in range(Chessboard1.SIZE):
        print(f'{i+1:{0}{2}}  ',' '.join(Chessboard1.board[i]))
    print()


    Chessboard1.figures_attack()
    print(Chessboard1.figures_card)

    print('    ',' '.join(Chessboard1.letter_idx))
    for i in range(Chessboard1.SIZE):
        print(f'{i+1:{0}{2}}  ',' '.join(Chessboard1.board[i]))


    # for inp_pset in input_places_sets:
    #     places_list = inp_pset.split(' ')
    #     print(places_list)
    #     place_ind = []
    #     for place in places_list[inp_pset]:
    #         place_ind.append(Chessboard.put_figure(figures_set[place], place))
 




if __name__ == '__main__':
    runner()

