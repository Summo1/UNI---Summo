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
        self.description = f"FIREBALL! Deals 3 + [turns in hand] damage. Currently dealing {3 + self.turns_in_hand} damage"
        self.effect = {"damage": 3 + self.turns_in_hand}
        self.symbol = str(self.turns_in_hand)


class CardDeck():
    def __init__(self, cards: list[Card]):
        self.deck = cards
        self.size = len(cards)
        self.cards_left = len(cards)
        
        pass
    def __str__(self) -> str:
        for item in self.deck:
            return item +','
    def __repr__(self):
        return 'CardDeck()'
    def is_empty(self) -> bool:
        if self.size == 0:
            return True
        else:
            return False
    def remaining_count(self) -> int:
        return self.cards_left
    
    def draw_cards(self, num: int) -> list[Card]:
        drawn_cards = []
        if num > self.size:
            num = self.size
        
        drawn_cards = self.deck[:num]
        self.deck = self.deck[num-1:]
        
        self.size -= num
        self.cards_left -= num
        
        
        return drawn_cards
    
    def add_card(self, card: Card):
        self.deck.append(card)

    
    
        
    
def main() -> None:
    cards = [Card(), Card(), Shield(), Heal(), Fireball(6)]
    deck = CardDeck(cards)
    print(deck.draw_cards(2))
    pass

if __name__ == "__main__":
    main()