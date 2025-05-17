# DO NOT modify or add any import statements
from support import *
from display import HearthView

# Name: Tom Summerton  
# Student Number: 49606782
# Favorite Building: Pyramids of Giza
# -----------------------------------------------------------------------------

# Define your classes and functions here
class Card:
    def __init__(self, name, description, cost, effect, symbol, **kwargs):
       self.name = name
       self.description = description
       self.cost = cost
       self.effect = effect
       self.symbol = symbol

    def __str__(self) -> str:
        return f"{self.name} {self.description}"

    def __repr__(self) -> str:
        pass
    def get_symbol(self) -> str:
        return self.symbol
    
    def get_cost(self) -> int:
        return self.cost

    def get_effect(self) -> dict[str, int]:
        return self.effect

    def is_permanent(self) -> bool:
        return 
        
        

def main() -> None:
    pass

if __name__ == "__main__":
    main()