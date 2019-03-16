from read_file import country_list, nameDict


class Country:
    """
    This class contains basic country attributes:
    --> ID, name, asset, gold, population, solider, weapon,
        food_speed, wood_speed, steel_speed, stone_speed, food, wood, steel, stone

    Don't try to set above attributes be negative, or it will raise error.
    """

    # constructor of Country object
    def __init__(self, ID, name, asset, gold, population, solider, weapon, air,
                 food_speed, wood_speed, steel_speed, stone_speed, food, wood, steel, stone):
        self._ID = int(ID)
        self._name = nameDict[name]
        self._asset = int(asset)
        self._gold = int(gold)
        self._population = int(population)
        self._solider = int(solider)
        self._weapon = float(weapon)
        self._air = float(air)
        self._food_speed = float(food_speed)
        self._wood_speed = float(wood_speed)
        self._steel_speed = float(steel_speed)
        self._stone_speed = float(stone_speed)
        self._food = int(food)
        self._wood = int(wood)
        self._steel = int(steel)
        self._stone = int(stone)

    def __dict__(self):
        """return all of the variables in dictionary that Country has"""
        return {"ID": self.ID, "name": self.name, "asset": self.asset, "gold": self.gold,
                "population": self.population, "solider": self.solider, "food_speed": self.food_speed,
                "wood_speed": self.wood_speed, "steel_speed": self.wood_speed, "stone_speed": self.stone_speed,
                "food": self.food, "wood": self.wood, "stone": self.stone}

    def __iter__(self):
        for attr, value in self.__dict__().items():
            yield attr, value

    def __str__(self):
        return f"{self._name} has food: {self.food} & wood: {self.wood} & steel: {self.steel} & stone: {self.stone}"

    def __lt__(self, other):
        """When you try to sort Country object, it will compare their value of asset."""
        return self.asset < other.asset

    @classmethod
    def from_tuple(cls, data):
        """construct Country with namedtuple"""
        return cls(data.id, data.name, data.asset, data.gold, data.population, data.solider,
                   data.weapon, data.food_speed, data.wood_speed, data.steel_speed,
                   data.stone_speed, data.food, data.wood, data.steel, data.stone)

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

    # set the value of Country.asset and avoid it becomes negtive
    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, value):
        if value < 0:
            raise ValueError("asset must be positive")
        self._asset = value

    # set the value of Country.gold and avoid it becomes negtive
    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        if value < 0:
            raise ValueError("gold must be positive")
        self._gold = value

    # set the value of Country.population and avoid it becomes negtive
    @property
    def population(self):
        return self._population

    @population.setter
    def population(self, value):
        if value < 0:
            raise ValueError("population must be positive")
        self._population = value

    # set the value of Country.solider and avoid it becomes negtive
    @property
    def solider(self):
        return self._solider

    @solider.setter
    def solider(self, value):
        if value < 0:
            raise ValueError("solider must be positive")
        self._solider = value

    # set the value of Country.weapon and avoid it becomes negtive
    @property
    def weapon(self):
        return self._weapon

    @weapon.setter
    def weapon(self, value):
        if value < 0:
            raise ValueError("weapon must be positive")
        self._weapon = value

    # set the value of Country.air and avoid it becomes negtive
    @property
    def air(self):
        return self._air

    @air.setter
    def air(self, value):
        if value < 0:
            raise ValueError("air must be positive")
        self._air = value

    # set the value of Country.food_speed and avoid it becomes negtive
    @property
    def food_speed(self):
        return self._food_speed

    @food_speed.setter
    def food_speed(self, value):
        if value < 0:
            raise ValueError("food_speed must be positive")
        self._food_speed = value

    # set the value of Country.wood_speed and avoid it becomes negtive
    @property
    def wood_speed(self):
        return self._wood_speed

    @wood_speed.setter
    def wood_speed(self, value):
        if value < 0:
            raise ValueError("wood_speed must be positive")
        self._wood_speed = value

    # set the value of Country.steel_speed and avoid it becomes negtive
    @property
    def steel_speed(self):
        return self._steel_speed

    @steel_speed.setter
    def steel_speed(self, value):
        if value < 0:
            raise ValueError("steel_speed must be positive")
        self._steel_speed = value

    # set the value of Country.stone_speed and avoid it becomes negtive
    @property
    def stone_speed(self):
        return self._stone_speed

    @stone_speed.setter
    def stone_speed(self, value):
        if value < 0:
            raise ValueError("stone_speed must be positive")
        self._stone_speed = value

    # set the value of Country.food and avoid it becomes negtive
    @property
    def food(self):
        return self._food

    @food.setter
    def food(self, value):
        if value < 0:
            raise ValueError("food must be positive")
        self._food = value

    # set the value of Country.wood and avoid it becomes negtive
    @property
    def wood(self):
        return self._wood

    @wood.setter
    def wood(self, value):
        if value < 0:
            raise ValueError("wood must be positive")
        self._wood = value

    # set the value of Country.steel and avoid it becomes negtive
    @property
    def steel(self):
        return self._steel

    @steel.setter
    def steel(self, value):
        if value < 0:
            raise ValueError("steel must be positive")
        self._steel = value

    # set the value of Country.stone and avoid it becomes negtive
    @property
    def stone(self):
        return self._stone

    @stone.setter
    def stone(self, value):
        if value < 0:
            raise ValueError("stone must be positive")
        self._stone = value


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


class ElDorado(Country):
    """docstring for ElDorado"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class Mongolia(Country):
    """docstring for Mongolia"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


class Australia(Country):
    """docstring for Australia"""

    def __init__(self, *arg, **kwargs):
        super().__init__(*arg, **kwargs)


a = Atlantis.from_tuple(country_list[0])
print(dict(a))
