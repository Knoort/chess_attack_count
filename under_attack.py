class ChessMan():
    '''Общий класс для фигур'''

    BOARD_SIZE = 4
    letter_idx = (
        'A', 'B', 'C', 'D', 'F', 'E', 'G', 'H'
    )
    number_idx = (
        '1', '2', '3', '4', '5', '6', '7', '8'
    )

    # def __init__(self):
    #     pass
    
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

    def _remove_dups(self, fields_list, x, y):
        '''Функция удаления повторяющихся полей, и собственного поля.'''

        uniq_list = []
        for i in range(len(fields_list)):
            if fields_list[i] not in uniq_list:
                uniq_list.append(fields_list[i])

        if [x, y] in uniq_list:
            uniq_list.remove([x, y])
        return uniq_list

    def _create_plus_list(self, x, y):
        '''Функция ладьи. Получает абстрактные координаты,
        возвращает список координат полей под атакой.'''

        attack_fields = []
        # Суммируем строку
        for i in range(self.BOARD_SIZE):
            attack_fields.append([i, y])
        # Суммируем строку
        for j in range(self.BOARD_SIZE):
            attack_fields.append([x, j])

        return attack_fields

    
    def _create_cross_list(self, x, y):
        '''Функция слона. Получает абстрактные координаты,
        возвращает список координат полей под атакой. '''

        attack_fields = []

        # Определяем диапазон, перебираем главную диагональ
        xmin = x - y
        xmax = x + (self.BOARD_SIZE - 1 - y)
        xmin = max(0, xmin)
        xmax = min(xmax, self.BOARD_SIZE - 1)
        if xmax < xmin:
            return attack_fields

        for i in range(xmin, xmax +1):
            j = y + (i - x)
            attack_fields.append([i, j])

        # Определяем диапазон, перебираем побочную диагональ
        xmin = x - (self.BOARD_SIZE - 1 - y)
        xmax = x + y
        xmin = max(0, xmin)
        xmax = min(xmax, self.BOARD_SIZE - 1)
        if xmax < xmin:
            return attack_fields

        for i in range(xmin, xmax +1):
            j = y - (i - x)
            attack_fields.append([i, j])

        return attack_fields
    
    def _func_stack(self, place, *attack_func):
        '''Стек обработки фигуры.'''
  
        # Проверка, что попали в поле
        x, y = self.field_verify(place)
        if x is None:
            return []

        # Общий список полей
        attack_list = []
        for func in attack_func:
            attack_list.extend(func(x,y))

        # Удаление повторяющихся полей, и собственного поля
        if attack_func is Horse._create_horse_list:
            return attack_list
        attack_uniq_list = self._remove_dups(attack_list, x, y)
        return attack_uniq_list
        

class Castle(ChessMan):
    '''Ладья'''

    def under_attack(self, place:str):
        # Передаем список функций атаки
        attack_list = self._func_stack(place, self._create_plus_list)
        return attack_list


class Elephant(ChessMan):
    '''Слон'''

    def under_attack(self, place:str):
        # Передаем список функций атаки
        attack_list = self._func_stack(place, self._create_cross_list)

        return attack_list


class Queen(ChessMan):
    '''Ферзь'''

    def under_attack(self, place:str):
        # Передаем список функций атаки
        attack_list = self._func_stack(
            place,
            self._create_plus_list,
            self._create_cross_list
        )

        return attack_list


class Horse(ChessMan):
    '''Лошадь'''
    horse_code = (
        +1, +2, -2, -1
    )

    def _create_horse_list(self, x, y):
        '''Функция коня. Получает абстрактные координаты,
         возвращает список координат полей под атакой.'''
        # horse_idx = []
        attack_fields = []
        for bin_code in range(2 ** 4):
            i = (bin_code >> 2) & 0b11
            j = bin_code & 0b11

            if (
                (i == j) or
                (i == (~j) & 0b11)
            ):
                continue
            # horse_idx.append([i, j])
            dx = x + self.horse_code[i]
            dy = y + self.horse_code[j]
            if (
                dx in range(self.BOARD_SIZE) and
                dy in range(self.BOARD_SIZE)
            ):
                attack_fields.append([dx, dy])
        
        return attack_fields

    def under_attack(self, place:str):
        # Передаем список функций атаки
        attack_list = self._func_stack(place, self._create_horse_list)

        return attack_list


def runner():

    place1 = 'C4'

    # Castle1 = Castle()
    # castle_list = Castle1._create_plus_list(1, 2)
    # print(castle_list)

    # attack = Castle1.under_attack(place1)
    # print(attack)

    # Elephant1 = Elephant()
    # attack = Elephant1.under_attack(place1)
    # print(attack)

    # Queen1 = Queen()
    # attack = Queen1.under_attack(place1)
    # print(attack)

    Horse1 = Horse()
    attack = Horse1.under_attack(place1)
    print(attack)



if __name__ == '__main__':
    runner()

