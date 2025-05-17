# DO NOT modify or add any import statements
from support import *
from display import HearthView

# Name: Tom Summerton  
# Student Number: 49606782
# Favorite Building: Pyramids of Giza
# -----------------------------------------------------------------------------

# Define your classes and functions here
class Card:
    def __init__(self, name: str = "Card", description: str = 'A card', cost: int = 1, effect: dict[str, int] = {}, symbol = 'C', **kwargs):
       self.name = name
       self.description = description
       self.cost = cost
       self.effect = effect
       self.symbol = symbol
       self.permanent = False

    def __str__(self) -> str:
        return f"{self.name}: {self.description}."

    def __repr__(self) -> str:
        return 'Card()'

    def get_symbol(self) -> str:
        return self.symbol
    
    def get_name(self) -> str:
        return self.name
    
    def get_cost(self) -> int:
        return self.cost

    def get_effect(self) -> dict[str, int]:
        return self.effect

    def is_permanent(self) -> bool:
        return self.permanent
        
class Shield(Card):
    def __init__(self):
        super().__init__(
            name = "Shield",
            description = "Cast a protective shield that can absorb 5 damage",
            cost = 1,
            effect = {"shield": 5},
            symbol = "S"
            
        )     
    def __repr__(self):
        return 'Shield()'
    
class Heal(Card):
    def __init__(self):
        super().__init__(
            name = "Heal",
            description = "Cast an aura on target. It recovers 2 health",
            cost = 2,
            effect = {"health": 2},
            symbol = "H"
            
        )     
    def __repr__(self):
        return 'Heal()' 
    

class Fireball(Card):
    def __init__(self, turns_in_hand: int):
        self.turns_in_hand = turns_in_hand
        super().__init__(
            name = "Fireball",
            description = f"FIREBALL! Deals 3 + [turns in hand] damage. Currently dealing {3 + self.turns_in_hand} damage",
            cost = 3,
            effect = {"damage": 3 + self.turns_in_hand},
            symbol = str(self.turns_in_hand)
        )
        
    def __repr__(self):
        return f'Fireball({self.turns_in_hand})'  
            
    def increment_turn(self):
        self.turns_in_hand += 1
    
    
    
        
    
def main() -> None:
    
    pass

if __name__ == "__main__":
    main()