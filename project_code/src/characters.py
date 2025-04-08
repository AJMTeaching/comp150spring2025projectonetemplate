from .entities import Character, Ability

class WizardCat(Character):
    def __init__(self):
        super().__init__(name="Wizard Cat", health=12)
        self.intelligence.value = 8
        self.add_ability(Ability("Fireball", damage_range=(4, 8)))
        self.add_ability(Ability("Magic Shield", damage_range=(2, 5)))

class FeralCat(Character):
    def __init__(self):
        super().__init__(name="Feral Cat", health=15)
        self.strength.value = 8
        self.add_ability(Ability("Forsaken Furball", damage_range=(5, 9)))
        self.add_ability(Ability("Cowardice", damage_range=(3, 6)))

class ExplodingKitten(Character):
    def __init__(self):
        super().__init__(name="Exploding Kitten", health=10)
        self.add_ability(Ability("Nuclear Reactivity", damage_range=(4, 10)))
        self.add_ability(Ability("Controlled Explosion", damage_range=(3, 7)))
