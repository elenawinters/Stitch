from enum import Enum, auto


class NameURLs(Enum):
    male = 'https://www.randomlists.com/data/names-male.json'
    female = 'https://www.randomlists.com/data/names-female.json'
    first = 'https://www.randomlists.com/data/names-first.json'
    middle = 'https://www.randomlists.com/data/middle-names.json'
    last = 'https://www.randomlists.com/data/names-surnames.json'
    nicknames = 'https://www.randomlists.com/data/nicknames.json'
    cat = 'https://www.randomlists.com/data/cat-names.json'
    dog = 'https://www.randomlists.com/data/dog-names.json'
    pet = 'https://www.randomlists.com/data/pet-names.json'

    class Spanish(Enum):
        first = 'https://www.randomlists.com/data/names-first-spanish.json'
        last = 'https://www.randomlists.com/data/names-last-spanish.json'

    default = first

