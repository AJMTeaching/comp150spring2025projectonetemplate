from .entities import Character, Ability

class WizardCat(Character):
    def __init__(self):
        super().__init__(name="Wizard Cat", health=12)
        self.intelligence.value = 8
        self.add_ability(Ability(
            name="Arcane Blast",
            damage_range=(4, 8),
            description="Unleashes a wave of mystical energy. Strong against dog illusions and fast attackers."
        ))
        self.add_ability(Ability(
            name="Teleport Puff",
            damage_range=(3, 6),
            description="Vanish and reappear with a puff of smoke, dealing surprise damage."
        ))

class FeralCat(Character):
    def __init__(self):
        super().__init__(name="Feral Cat", health=15)
        self.strength.value = 8
        self.add_ability(Ability(
            name="Savage Pounce",
            damage_range=(5, 9),
            description="A frenzied leap that slams the enemy. Highly effective in close combat."
        ))
        self.add_ability(Ability(
            name="Alley Swipe",
            damage_range=(3, 6),
            description="Quick claw strikes from the shadows. Balanced damage output."
        ))

class ExplodingKitten(Character):
    def __init__(self):
        super().__init__(name="Exploding Kitten", health=10)
        self.add_ability(Ability(
            name="Nuclear Furball",
            damage_range=(4, 10),
            description="Unstable attack with unpredictable explosion radius. High risk, high reward."
        ))
        self.add_ability(Ability(
            name="Detonation Dash",
            damage_range=(3, 7),
            description="Explode while dashing past enemies. Medium damage to all in the path."
        ))
