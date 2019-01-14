from read_file import country_list, nameDict


class Country:
    """This class contains basic country attributes"""

    def __init__(self, ID, name, asset, gold, population, solider, weapon,
                 food_speed, wood_speed, mineral_speed, oil_speed, food, wood, mineral, oil):
        self.ID = int(ID)
        self._name = nameDict[name]
        self._asset = float(asset)
        self._gold = int(gold)
        self._population = int(population)
        self._solider = int(solider)
        self._food_speed = float(food_speed)
        self._wood_speed = float(wood_speed)
        self._mineral_speed = float(mineral_speed)
        self._oil_speed = float(oil_speed)
        self._food = int(food)
        self._wood = int(wood)
        self._mineral = int(mineral)
        self._oil = int(oil)

    def __str__(self):
        return f"This country is {self._name}, food:{self.food}, wood:{self.wood}, mineral:{self.mineral}, oil:{self.oil}"

    def __lt__(self, other):
        return self.asset < other.asset

    @property
    def asset(self):
        return self._asset

    @asset.setter
    def asset(self, value):
        if value < 0:
            raise ValueError("asset must be positive")
        self._asset = value

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        if value < 0:
            raise ValueError("gold must be positive")
        self._gold = value

    @property
    def population(self):
        return self._population

    @gold.setter
    def population(self, value):
        if value < 0:
            raise ValueError("population must be positive")
        self._population = value

    @property
    def solider(self):
        return self._solider

    @gold.setter
    def solider(self, value):
        if value < 0:
            raise ValueError("solider must be positive")
        self._solider = value

    @property
    def food_speed(self):
        return self._food_speed

    @food_speed.setter
    def food_speed(self, value):
        if value < 0:
            raise ValueError("food_speed must be positive")
        self._food_speed = value

    @property
    def wood_speed(self):
        return self._wood_speed

    @wood_speed.setter
    def food_speed(self, value):
        if value < 0:
            raise ValueError("wood_speed must be positive")
        self._wood_speed = value

    @property
    def mineral_speed(self):
        return self._mineral_speed

    @wood_speed.setter
    def mineral_speed(self, value):
        if value < 0:
            raise ValueError("mineral_speed must be positive")
        self._mineral_speed = value

    @property
    def oil_speed(self):
        return self._oil_speed

    @oil_speed.setter
    def oil_speed(self, value):
        if value < 0:
            raise ValueError("oil_speed must be positive")
        self._oil_speed = value

    @property
    def food(self):
        return self._food

    @food.setter
    def food(self, value):
        if value < 0:
            raise ValueError("food must be positive")
        self._food = value

    @property
    def wood(self):
        return self._wood

    @wood.setter
    def wood(self, value):
        if value < 0:
            raise ValueError("wood must be positive")
        self._wood = value

    @property
    def mineral(self):
        return self._mineral

    @mineral.setter
    def mineral(self, value):
        if value < 0:
            raise ValueError("mineral must be positive")
        self._mineral = value

    @property
    def oil(self):
        return self._oil

    @oil.setter
    def oil(self, value):
        if value < 0:
            raise ValueError("oil must be positive")
        self._oil = value

    @classmethod
    def from_tuple(cls, data):
        return cls(data.id, data.name, float(data.asset), int(data.gold), int(data.population), int(data.solider), float(data.weapon),
                   float(data.food_speed), float(data.wood_speed), float(data.mineral_speed), float(data.oil_speed),
                   int(data.food), int(data.wood), int(data.mineral), int(data.oil))


class Atlantis(Country):
    """docstring for Atlantis"""

    def __init__(self, *arg, **kwargs):
        super(Atlantis, self).__init__(*arg, **kwargs)


class Asgard(Country):
    """docstring for Asgard"""

    def __init__(self, *arg, **kwargs):
        super(Asgard, self).__init__(*arg, **kwargs)


class Olympus(Country):
    """docstring for Olympus"""

    def __init__(self, *arg, **kwargs):
        super(Olympus, self).__init__(*arg, **kwargs)


class Wakanda(Country):
    """docstring for Wakanda"""

    def __init__(self, *arg, **kwargs):
        super(Wakanda, self).__init__(*arg, **kwargs)


class ShangriLa(Country):
    """docstring for ShangriLa"""

    def __init__(self, *arg, **kwargs):
        super(ShangriLa, self).__init__(*arg, **kwargs)


class Varanasi(Country):
    """docstring for Varanasi"""

    def __init__(self, *arg, **kwargs):
        super(Varanasi, self).__init__(*arg, **kwargs)


class Maya(Country):
    """docstring for Maya"""

    def __init__(self, *arg, **kwargs):
        super(Maya, self).__init__(*arg, **kwargs)


class ElDorado(Country):
    """docstring for ElDorado"""

    def __init__(self, *arg, **kwargs):
        super(ElDorado, self).__init__(*arg, **kwargs)


class Mongolia(Country):
    """docstring for Mongolia"""

    def __init__(self, *arg, **kwargs):
        super(Mongolia, self).__init__(*arg, **kwargs)


class Australia(Country):
    """docstring for Australia"""

    def __init__(self, *arg, **kwargs):
        super(Australia, self).__init__(*arg, **kwargs)


a = Atlantis.from_tuple(country_list[0])
