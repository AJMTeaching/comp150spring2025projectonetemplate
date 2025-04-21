from .entities import Character, Ability

class WizardCat(Character):
    def __init__(self):
        super().__init__(name="Wizard Cat", health=12)
        self.intelligence.value = 8
        self.add_ability(Ability(
            name="Fireball",
            damage_range=(4, 8),
            description="A flaming burst of arcane energy. Deals moderate magic damage."
        ))
        self.add_ability(Ability(
            name="Magic Shield",
            damage_range=(2, 5),
            description="A reactive shield of mana. Reflects minor damage while reducing incoming hits."
        ))

class FeralCat(Character):
    def __init__(self):
        super().__init__(name="Feral Cat", health=15)
        self.strength.value = 8
        self.add_ability(Ability(
            name="Forsaken Furball",
            damage_range=(5, 9),
            description="A wild, scrappy barrage. Deals strong physical damage—chaotic but effective."
        ))
        self.add_ability(Ability(
            name="Cowardice",
            damage_range=(3, 6),
            description="A fake retreat followed by a sneak attack. Less predictable but still fierce."
        ))

class ExplodingKitten(Character):
    def __init__(self):
        super().__init__(name="Exploding Kitten", health=10)
        self.add_ability(Ability(
            name="Nuclear Reactivity",
            damage_range=(4, 10),
            description="Volatile core surges with energy. High-risk, high-damage attack."
        ))
        self.add_ability(Ability(
            name="Controlled Explosion",
            damage_range=(3, 7),
            description="A tactical blast. Medium-range damage with less risk of self-destruction."
        ))
