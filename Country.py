from read_file import country_list, nameDict


class Country:
    """This class contains basic country attributes"""

    def __init__(self, ID, name, asset, gold, population, solider, weapon,
                 food_speed, wood_speed, mineral_speed, oil_speed, food, wood, mineral, oil):
        self._id = int(ID)
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
        return f"This country is {self.name}, food:{self.food}, wood:{self.wood}, mineral:{self.mineral}, oil:{self.oil}"

    def __lt__(self, other):
        return self.asset < other.asset

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not 1 <= value <= 10:
            raise ValueError("name must between 1 to 10")
        self._id = value

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
