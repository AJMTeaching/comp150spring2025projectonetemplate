import sys
import os
import unittest

# Ensure correct pathing to project source
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from project_code.src.entities import Statistic, Character, Ability, Enemy, HealthPotion


# --- STATISTIC TESTS ---
class TestStatistic(unittest.TestCase):

    def setUp(self):
        self.stat = Statistic("Strength", value=10)

    def test_initialization(self):
        self.assertEqual(self.stat.name, "Strength")
        self.assertEqual(self.stat.value, 10)

    def test_modify_within_bounds(self):
        self.stat.modify(5)
        self.assertEqual(self.stat.value, 15)

    def test_modify_above_max(self):
        self.stat.modify(1000)
        self.assertEqual(self.stat.value, self.stat.max_value)

    def test_modify_below_min(self):
        self.stat.modify(-1000)
        self.assertEqual(self.stat.value, self.stat.min_value)


# --- CHARACTER TESTS ---
class TestCharacter(unittest.TestCase):

    def setUp(self):
        self.char = Character("Test Cat", health=20)

    def test_initialization_defaults(self):
        self.assertEqual(self.char.name, "Test Cat")
        self.assertEqual(self.char.health, 20)
        self.assertEqual(self.char.strength.value, 5)
        self.assertEqual(self.char.intelligence.value, 5)

    def test_healing_behavior(self):
        self.char.health = 10
        healed = self.char.heal()
        self.assertGreaterEqual(self.char.health, 10)
        self.assertIsInstance(healed, bool)

    def test_add_ability_to_character(self):
        ability = Ability(name="Test Claw", damage_range=(1, 3))
        self.char.add_ability(ability)
        self.assertIn(ability, self.char.abilities)

    def test_use_item_from_inventory(self):
        potion = HealthPotion()
        self.char.health = 5
        self.char.inventory.append(potion)
        used = self.char.use_item_from_inventory(0)
        self.assertTrue(used)
        self.assertGreater(self.char.health, 5)


# --- ABILITY TESTS ---
class TestAbility(unittest.TestCase):

    def setUp(self):
        self.user = Character("Wizard")
        self.enemy = Enemy("Dog", 10)
        self.ability = Ability("Whisker Blast", damage_range=(3, 5), chance_to_hit=1.0)  # Always hits

    def test_ability_hits_and_damages(self):
        old_health = self.enemy.health
        result = self.ability.use(self.user, self.enemy)
        self.assertTrue(result)
        self.assertLess(self.enemy.health, old_health)

    def test_ability_misses(self):
        ability = Ability("Miss Move", damage_range=(1, 2), chance_to_hit=0.0)  # Always misses
        result = ability.use(self.user, self.enemy)
        self.assertFalse(result)
        self.assertEqual(self.enemy.health, 10)


# --- ENEMY TESTS ---
class TestEnemy(unittest.TestCase):

    def setUp(self):
        self.enemy = Enemy("Puppy Intruder", 10, damage_range=(2, 4))
        self.target = Character("Cat Defender", health=20)

    def test_attack_deals_expected_damage(self):
        old_health = self.target.health
        damage = self.enemy.attack(self.target)
        self.assertTrue(2 <= damage <= 4)
        self.assertEqual(self.target.health, old_health - damage)

# --- HEALTH POTION TESTS ---
class TestHealthPotion(unittest.TestCase):

    def setUp(self):
        self.cat = Character("Potion Tester", health=20)
        self.potion = HealthPotion()

    def test_healing_when_not_full_health(self):
        self.cat.health = 10
        result = self.potion.use(self.cat)
        self.assertTrue(result)
        self.assertGreater(self.cat.health, 10)

    def test_no_heal_when_full_health(self):
        self.cat.health = self.cat.max_health
        result = self.potion.use(self.cat)
        self.assertFalse(result)
        self.assertEqual(self.cat.health, self.cat.max_health)

# --- DEATH LOGIC TESTS ---
class TestDeathCondition(unittest.TestCase):

    def test_is_alive_logic(self):
        cat = Character("Near Death", health=1)
        cat.take_damage(1)
        self.assertFalse(cat.is_alive())

# --- STRENGTH BONUS TESTS ---
class TestAbilityWithStrengthBonus(unittest.TestCase):

    def test_strength_increases_damage(self):
        user = Character("Buff Cat", health=10)
        user.strength.value = 15  # Should increase damage
        enemy = Enemy("Dummy Dog", 20)
        ability = Ability("Mighty Swipe", damage_range=(1, 1), chance_to_hit=1.0)  # Minimum range, but scales
        ability.use(user, enemy)
        self.assertLess(enemy.health, 20)  # Should be <20 because of bonus

# --- INVENTORY EDGE CASES ---
class TestInventoryLogic(unittest.TestCase):

    def test_use_invalid_index(self):
        char = Character("Forgetful Cat", health=10)
        result = char.use_item_from_inventory(0)  # Empty inventory
        self.assertFalse(result)

    def test_inventory_removal_after_use(self):
        char = Character("Hoarder Cat", health=5)
        potion = HealthPotion()
        char.inventory.append(potion)
        char.use_item_from_inventory(0)
        self.assertEqual(len(char.inventory), 0)


if __name__ == '__main__':
    unittest.main()
