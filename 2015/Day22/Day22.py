from typing import List

class Spell:
    def __init__(self, index: int, name: str, mana_cost: int, damage: int, heal: int, duration: int, armor: int, mana_gain: int) -> None:
        self.index = index
        self.name = name
        self.mana_cost = mana_cost
        self.damage = damage
        self.heal = heal
        self.duration = duration
        self.armor = armor
        self.mana_gain = mana_gain

    def __repr__(self) -> str:
        return self.name

class Game:

    spells = [
        Spell(0, "Magic Missle", 53, 4, 0, 0, 0, 0),
        Spell(1, "Drain", 73, 2, 2, 0, 0, 0),
        Spell(2, "Shield", 113, 0, 0, 6, 7, 0),
        Spell(3, "Poison", 173, 3, 0, 6, 0, 0),
        Spell(4, "Recharge", 229, 0, 0, 5, 0, 101)
    ]

    def __init__(self, hard_mode = False) -> None:
        self.min_mana = 2**16
        self.hard_mode = hard_mode

    def get_castable_spells(mana: int, active_spells: List[int]):
        for spell in Game.spells:
            if spell.mana_cost > mana:
                continue
            if active_spells[spell.index] > 0:
                continue
            yield spell

    def sim(self, players_turn: bool, hp: int, mana: int, boss_hp: int, active_spells: List[int], mana_spent: int):
        if mana_spent > self.min_mana:
            return

        if players_turn and self.hard_mode:
            hp -= 1
            if hp <= 0:
                return

        armor = 0

        for i in range(len(active_spells)):
            duration = active_spells[i]
            if duration > 0:
                spell = Game.spells[i]

                armor += spell.armor
                hp += spell.heal
                mana += spell.mana_gain
                boss_hp -= spell.damage

                active_spells[i] -= 1

        if boss_hp <= 0:
            self.min_mana = min(self.min_mana, mana_spent)
            return

        if players_turn:
            castable_spells = list(Game.get_castable_spells(mana, active_spells))

            if len(castable_spells) == 0:
                return
            
            for spell in castable_spells:
                if spell.duration == 0:
                    if boss_hp - spell.damage <= 0:
                        self.min_mana = min(self.min_mana, mana_spent + spell.mana_cost)
                        continue
                    self.sim(not players_turn, hp + spell.heal, mana - spell.mana_cost, boss_hp - spell.damage, active_spells.copy(), mana_spent + spell.mana_cost)
                else:
                    new_active_spells = active_spells.copy()
                    assert new_active_spells[spell.index] == 0
                    new_active_spells[spell.index] = spell.duration
                    self.sim(not players_turn, hp, mana - spell.mana_cost, boss_hp, new_active_spells, mana_spent + spell.mana_cost)
                pass

        else:
            assert armor < 9
            hp -= (9 - armor) # boss dmg
            if hp <= 0:
                return
            self.sim(not players_turn, hp, mana, boss_hp, active_spells.copy(), mana_spent)

def main():
    game = Game()
    game.sim(True, 50, 500, 51, [0, 0, 0, 0, 0], 0) # player stats, boss hp
    print(game.min_mana)

    game = Game(True)
    game.sim(True, 50, 500, 51, [0, 0, 0, 0, 0], 0) # player stats, boss hp
    print(game.min_mana)

if __name__ == '__main__':
    main()