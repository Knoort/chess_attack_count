class ChessMan():
    '''Общий класс для фигур'''

    BOARD_SIZE = 8
    letter_idx = (
        'A', 'B', 'C', 'D', 'F', 'E', 'G', 'H'
    )
    number_idx = (
        '1', '2', '3', '4', '5', '6', '7', '8'
    )

    
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

    def _remove_dups(self, fields_list = [], x = None, y = None):
        '''Функция удаления повторяющихся полей, и собственного поля.'''

        if fields_list == []:
            return fields_list
        uniq_list = []
        for i in range(len(fields_list)):
            if fields_list[i] not in uniq_list:
                uniq_list.append(fields_list[i])

        return uniq_list

    # def _remove_self(self, fields_list, x = None, y = None):
    #     if (
    #         (x is not None) and
    #         (y is not None) and
    #         ([x, y] in fields_list)
    #     ):
    #         fields_list.remove([x, y])
    #     return fields_list

    def _create_plus_list(self, x, y):
        '''Функция ладьи. Получает абстрактные координаты,
        возвращает список координат полей под атакой.'''

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
        возвращает список координат полей под атакой. '''

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
        fields_list = self._remove_dups(fields_list)
        # и собственного поля
        if [x, y] in fields_list:
            fields_list.remove([x, y])
        # fields_list = self._remove_self(fields_list, x, y)
        return fields_list
        

class Castle(ChessMan):
    '''Ладья'''

    def under_attack(self, place:str):
        # Передаем список функций атаки
        fields_list = self._func_stack(place, self._create_plus_list)
        return fields_list


class Elephant(ChessMan):
    '''Слон'''

    def under_attack(self, place:str):
        # Передаем список функций атаки
        fields_list = self._func_stack(place, self._create_cross_list)
        return fields_list


class Queen(ChessMan):
    '''Ферзь'''

    def under_attack(self, place:str):
        # Передаем список функций атаки
        fields_list = self._func_stack(
            place,
            self._create_plus_list,
            self._create_cross_list
        )
        return fields_list


class Horse(ChessMan):
    '''Лошадь'''

    horse_code = (
        +1, +2, -2, -1
    )

    def _create_horse_list(self, x, y):
        '''Функция коня. Получает абстрактные координаты,
         возвращает список координат полей под атакой.'''

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
        # Передаем список функций атаки
        fields_list = self._func_stack(place, self._create_horse_list)
        return fields_list


def attack_set_calc(places_set:str, *figures):
    places_list = places_set.split(' ')
    if len(places_list) != len(figures):
        return []
    print(places_list)
    fields_list = []
    for idx in range(len(places_list)):
        fields_list.extend(figures[idx].under_attack(places_list[idx]))
        print(fields_list)
        print(idx)
        fields_list = figures[idx]._remove_dups(fields_list)
    
    for idx in range(len(places_list)):
        x, y = figures[idx].field_verify(places_list[idx])
        if [x, y] in fields_list:
            fields_list.remove([x, y])

    return fields_list


def runner():

    queen_place = 'D1'
    castle_place = 'D3'
    horse_place = 'E5'
    input_places_set = f'{queen_place} {castle_place} {horse_place}'
    input_places_set = 'D1 D3 E5'

 
    Queen1 = Queen()
    Castle1 = Castle()
    Horse1 = Horse()
    
    attack_set = attack_set_calc(
        input_places_set,
        Queen1,
        Castle1,
        Horse1
    )
    print('Итоговый сет:')
    print(attack_set)
    print(len(attack_set))
    print('Ферзь:')
    queen_attack = Queen1.under_attack(queen_place)
    print(queen_attack)
    print('Ладья:')
    attack = Castle1.under_attack(castle_place)
    print(attack)
    print('Конь:')
    attack = Horse1.under_attack(horse_place)
    print(attack)


if __name__ == '__main__':
    runner()

