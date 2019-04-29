class Country:
    """
        This class contains basic country attributes:
        --> ID, name, asset, gold, population, solider, weapon,
            food_speed, wood_speed, steel_speed, stone_speed, food, wood, steel, stone

        Don't try to set above attributes be negative, or it will raise error.
    """

    # Constructor of Country object
    def __init__(self, ID, name, wonders, gold, population, weapon, defense,
                 food_speed, wood_speed, steel_speed, stone_speed, food, wood, steel, stone):
        self._ID = int(ID)
        self._name = name
        self._wonders = int(wonders)
        self._gold = int(gold)
        self._population = int(population)
        self._weapon = float(weapon)
        self._defense = int(defense)
        self._food_speed = float(food_speed)
        self._wood_speed = float(wood_speed)
        self._steel_speed = float(steel_speed)
        self._stone_speed = float(stone_speed)
        self._food = int(food)
        self._wood = int(wood)
        self._steel = int(steel)
        self._stone = int(stone)

    def __dict__(self):
        """ Return all of the variables in dictionary that Country has """
        return {"ID": self.ID, "name": self.name, "wonders": self.wonders, "gold": self.gold,
                "population": self.population, "weapon": self.weapon, "defense": self.defense,
                "food_speed": self.food_speed, "wood_speed": self.wood_speed,
                "steel_speed": self.steel_speed, "stone_speed": self.stone_speed,
                "food": self.food, "wood": self.wood, "steel": self.steel, "stone": self.stone}

    def __iter__(self):
        for attr, value in self.__dict__().items():
            yield attr, value

    def __str__(self):
        return f"{self._name} has {self.food} food & {self.wood} wood & {self.steel} steel & {self.stone} stone"

    def __lt__(self, other):
        """ When you try to sort Country object, it will compare their value of asset. """
        return self.asset < other.asset

    @classmethod
    def from_tuple(cls, data):
        """ construct Country with namedtuple """
        return cls(data.id, data.name, data.wonders, data.gold, data.population, data.weapon,
                   data.defense, data.food_speed, data.wood_speed, data.steel_speed,
                   data.stone_speed, data.food, data.wood, data.steel, data.stone)

    def to_list(self):
        """ Return all of the information in list """
        return list(self.__dict__().values())

    # set the "ID" and "name" are immutable
    @property
    def ID(self):
        return self._ID

    @ID.setter
    def ID(self, value):
        raise TypeError("ID is not mutable")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        raise TypeError("name is not mutable")

    # set the value of Country.wonders and avoid it becomes negtive
    @property
    def wonders(self):
        return self._wonders

    @wonders.setter
    def wonders(self, value):
        if value < 0:
            print(f"{self.name}的世界奇觀應該是正數而不是{value}")
            raise TypeError("wonders must be positive")

        self._wonders = int(round(value, -1))

    # set the value of Country.gold and avoid it becomes negtive
    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        if value < 0:
            print(f"{self.name}的黃金應該是正數而不是{value}")
            raise ValueError("gold must be positive")
        self._gold = int(round(value, -1))

    # set the value of Country.population and avoid it becomes negtive
    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        if value < 0:
            print(f"{self.name}的黃金應該是正數而不是{value}")
            raise ValueError("population must be positive")
        self._population = int(round(value, -1))

    # set the value of Country.weapon and avoid it becomes negtive
    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, value):
        if value < 0:
            print(f"{self.name}的武器倍率應該大於0而不是{value}")
            raise ValueError("weapon must be positive")
        self._weapon = value

    # set the value of Country.defense and avoid it becomes negtive
    @property
    def defense(self):
        return self._defense

    @defense.setter
    def defense(self, value):
        if value < 0:
            print(f"{self.name}的防禦力應該是正數而不是{value}")
            raise ValueError("defense must be positive")
        self._defense = int(round(value, -1))

    # set the value of Country.food_speed and avoid it becomes negtive
    @property
    def food_speed(self):
        return self._food_speed

    @food_speed.setter
    def food_speed(self, value):
        if value < 0:
            print(f"{self.name}的糧食生產速度應該是正數而不是{value}")
            raise ValueError("food_speed must be positive")
        self._food_speed = value

    # set the value of Country.wood_speed and avoid it becomes negtive
    @property
    def wood_speed(self):
        return self._wood_speed

    @wood_speed.setter
    def wood_speed(self, value):
        if value < 0:
            print(f"{self.name}的木頭生產速度應該是正數而不是{value}")
            raise ValueError("wood_speed must be positive")
        self._wood_speed = value

    # set the value of Country.steel_speed and avoid it becomes negtive
    @property
    def steel_speed(self):
        return self._steel_speed

    @steel_speed.setter
    def steel_speed(self, value):
        if value < 0:
            print(f"{self.name}的鐵礦生產速度應該是正數而不是{value}")
            raise ValueError("steel_speed must be positive")
        self._steel_speed = value

    # set the value of Country.stone_speed and avoid it becomes negtive
    @property
    def stone_speed(self):
        return self._stone_speed

    @stone_speed.setter
    def stone_speed(self, value):
        if value < 0:
            print(f"{self.name}的石頭生產速度應該是正數而不是{value}")
            raise ValueError("stone_speed must be positive")
        self._stone_speed = value

    # set the value of Country.food and avoid it becomes negtive
    @property
    def food(self):
        return self._food

    @food.setter
    def food(self, value):
        if value < 0:
            print(f"{self.name}的糧食應該是正數而不是{value}")
            raise ValueError("food must be positive")
        self._food = int(round(value, -1))

    # set the value of Country.wood and avoid it becomes negtive
    @property
    def wood(self):
        return self._wood

    @wood.setter
    def wood(self, value):
        if value < 0:
            print(f"{self.name}的木頭應該是正數而不是{value}")
            raise ValueError("wood must be positive")
        self._wood = int(round(value, -1))

    # set the value of Country.steel and avoid it becomes negtive
    @property
    def steel(self):
        return self._steel

    @steel.setter
    def steel(self, value):
        if value < 0:
            print(f"{self.name}的鐵礦應該是正數而不是{value}")
            raise ValueError("steel must be positive")
        self._steel = int(round(value, -1))

    # set the value of Country.stone and avoid it becomes negtive
    @property
    def stone(self):
        return self._stone

    @stone.setter
    def stone(self, value):
        if value < 0:
            print(f"{self.name}的石頭應該是正數而不是{value}")
            raise ValueError("stone must be positive")
        self._stone = int(round(value, -1))


class Atlantis(Country):
    """docstring for Atlantis"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class Asgard(Country):
    """docstring for Asgard"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class Olympus(Country):
    """docstring for Olympus"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class Wakanda(Country):
    """docstring for Wakanda"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class ShangriLa(Country):
    """docstring for ShangriLa"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class Varanasi(Country):
    """docstring for Varanasi"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class Maya(Country):
    """docstring for Maya"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class Tartarus(Country):
    """docstring for Tartarus"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class Teotihuacan(Country):
    """docstring for Teotihuacan"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class EasterIsland(Country):
    """docstring for EasterIsland"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)
