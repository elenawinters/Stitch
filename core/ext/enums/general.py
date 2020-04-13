from enum import Enum, auto


class Sex(Enum):
    male = 1
    female = 2
    other = 3
    man = male
    boy = male
    m = male
    woman = female
    girl = female
    f = female
    default = other
