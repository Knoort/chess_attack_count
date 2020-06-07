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

    def put_figure(self, Figure, place:str):
        '''Проверка попадания в поле. Возвращает абстрактные координаты'''
        y = int(place[1]) - 1
        if (
            (len(place) != 2) or
            (place[0] not in self.letter_idx) or
            y not in range(len(self.letter_idx))
        ):
            return [None, None]

        x = self.letter_idx.index(place[0])
        #    if max(x, y) >= self.BOARD_SIZE:
        #     return [None, None]

        self.board[y][x] = Figure.name[0] #symb()
        self.figures_card[Figure.name] = [x, y]
       
        return [x, y]

    def clear(self):
        self.figures_card.clear()
        self.board = [['0' for i in range(self.SIZE)] for j in range(self.SIZE)]

class ChessMan:
    '''Шахматная фигура'''
    SYMB_UCODE = 0
    BOARD_SIZE = 20
    letter_idx = (
        'A', 'B', 'C', 'D', 'F', 'E', 'G', 'H'
    )
    number_idx = (
        '1', '2', '3', '4', '5', '6', '7', '8'
    )

    def __init__(self, name:str):
        self.name = name
    def __str__(self):
        return self.name

    def symb(self):
        return chr(self.SYMB_UCODE)

    def field_verify(self, place:str):
        '''Проверка попадания в поле. Возвращает абстрактные координаты'''
        if (
            (len(place) != 2) or
            (place[0] not in self.letter_idx) or
            (place[1] not in self.number_idx)
        ):
            return [None, None]
        x = self.letter_idx.index(place[0])
        y = self.number_idx.index(place[1])
        if max(x, y) >= self.BOARD_SIZE:
            return [None, None]

        return [x, y]

    def _create_plus_list(self, x, y):
        '''Функция ладьи. Получает абстрактные координаты,
        возвращает список полей под атакой.'''

        fields_list = []
        # Суммируем строку
        for i in range(self.BOARD_SIZE):
            fields_list.append([i, y])
        # Суммируем стобец
        for j in range(self.BOARD_SIZE):
            fields_list.append([x, j])
        return fields_list

    
    def _create_cross_list(self, x, y):
        '''Функция слона. Получает абстрактные координаты,
        возвращает список полей под атакой. '''

        fields_list = []
        # Определяем диапазон, перебираем главную диагональ
        xmin = x - y
        xmax = x + (self.BOARD_SIZE - 1 - y)
        xmin = max(0, xmin)
        xmax = min(xmax, self.BOARD_SIZE - 1)
        if xmax < xmin:
            return fields_list

        for i in range(xmin, xmax +1):
            j = y + (i - x)
            fields_list.append([i, j])
        # Определяем диапазон, перебираем побочную диагональ
        xmin = x - (self.BOARD_SIZE - 1 - y)
        xmax = x + y
        xmin = max(0, xmin)
        xmax = min(xmax, self.BOARD_SIZE - 1)
        if xmax < xmin:
            return fields_list

        for i in range(xmin, xmax +1):
            j = y - (i - x)
            fields_list.append([i, j])
        return fields_list
    
    def _func_stack(self, place, *attack_func):
        '''Стек обработки фигуры.'''
  
        # Проверка, что попали в поле
        x, y = self.field_verify(place)
        if x is None:
            return []

        # Общий список полей
        fields_list = []
        for func in attack_func:
            fields_list.extend(func(x,y))

        # В лошади ничего не удаляем
        if attack_func is Horse._create_horse_list:
            return fields_list
        # В остальных удаление повторяющихся полей
        fields_list = dupl_rm(fields_list)
        # и собственного поля
        if [x, y] in fields_list:
            fields_list.remove([x, y])
        # fields_list = self._remove_self(fields_list, x, y)
        return fields_list
        

class Castle(ChessMan):
    '''Ладья'''

    SYMB_UCODE = 9820

    def under_attack(self, place:str):
        '''Список полей атаки ладьи'''
        fields_list = self._func_stack(place, self._create_plus_list)
        return fields_list


class Queen(ChessMan):
    '''Ферзь'''

    SYMB_UCODE = 9819

    def under_attack(self, place:str):
        '''Список полей атаки ферзя'''
        fields_list = self._func_stack(
            place,
            self._create_plus_list,
            self._create_cross_list
        )
        return fields_list


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

    input_places_sets = [
        # 'D1 D3 E5',
        # 'A1 H8 B6',
        # 'H7 F8 G6',
        'C5 B4 G2'
    ]

    Chessboard1 = Chessboard(10)

    Queen1 = Queen('Queen')
    Castle1 = Castle('Castle')
    Horse1 = Horse('Horse')

    figures_set = [Queen1, Castle1, Horse1]

    places_list = input_places_sets[0].split(' ')
    print(places_list)

    place_idx = [
        Chessboard1.put_figure(figures_set[i], places_list[i])
        for i in range(len(places_list))
    ]
    print(place_idx)
    print(Chessboard1.figures_card)

    print('    ',' '.join(Chessboard1.letter_idx))
    for i in range(Chessboard1.SIZE):
        print(f'{i+1:{0}{2}}  ',' '.join(Chessboard1.board[i]))
    print()
    Chessboard1.clear()
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

