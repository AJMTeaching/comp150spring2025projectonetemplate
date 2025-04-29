from .entities import Character, Ability

DEFAULT_HEALTH = 12
DEFAULT_DAMAGE = (3, 7)

class WizardCat(Character):
    def __init__(self):
        super().__init__(name="Wizard Cat", health=DEFAULT_HEALTH)
        self.intelligence.value = 8
        self.add_ability(Ability(
            name="Arcane Blast",
            damage_range=DEFAULT_DAMAGE,
            description="Unleashes a wave of mystical energy. Strong against illusions and fast attackers."
        ))
        self.add_ability(Ability(
            name="Teleport Puff",
            damage_range=DEFAULT_DAMAGE,
            description="Vanish and reappear with a puff of smoke, dealing surprise damage."
        ))

class FeralCat(Character):
    def __init__(self):
        super().__init__(name="Feral Cat", health=DEFAULT_HEALTH)
        self.strength.value = 8
        self.add_ability(Ability(
            name="Savage Pounce",
            damage_range=DEFAULT_DAMAGE,
            description="A frenzied leap that slams the enemy. Highly effective in close combat."
        ))
        self.add_ability(Ability(
            name="Alley Swipe",
            damage_range=DEFAULT_DAMAGE,
            description="Quick claw strikes from the shadows. Balanced damage output."
        ))

class ExplodingKitten(Character):
    def __init__(self):
        super().__init__(name="Exploding Kitten", health=DEFAULT_HEALTH)
        self.add_ability(Ability(
            name="Nuclear Furball",
            damage_range=DEFAULT_DAMAGE,
            description="Unstable attack with unpredictable explosion radius. High risk, high reward."
        ))
        self.add_ability(Ability(
            name="Detonation Dash",
            damage_range=DEFAULT_DAMAGE,
            description="Explode while dashing past enemies. Medium damage to all in the path."
        ))
