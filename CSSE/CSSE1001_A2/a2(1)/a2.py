# DO NOT modify or add any import statements
from support import *
from display import HearthView

# Name: Tom Summerton  
# Student Number: 49606782
# Favorite Building: Pyramids of Giza
# -----------------------------------------------------------------------------

# Define your classes and functions here
class Card:
    def __init__(self, name: str = CARD_NAME, description: str = CARD_DESC, cost: int = 1, effect: dict[str, int] = {}, symbol = CARD_SYMBOL, **kwargs):
       self.name = name
       self.description = description
       self.cost = cost
       self.effect = effect
       self.symbol = symbol
       self.permanent = False

    def __str__(self) -> str:
        return f"{self.name}: {self.description}"

    def __repr__(self) -> str:
        return f'{self.name}()'

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
            name = SHIELD_NAME,
            description = SHIELD_DESC,
            cost = 1,
            effect = {SHIELD: 5},
            symbol = SHIELD_SYMBOL
            
        )
    
class Heal(Card):
    def __init__(self):
        super().__init__(
            name = HEAL_NAME,
            description = HEAL_DESC,
            cost = 2,
            effect = {HEALTH: 2},
            symbol = HEAL_SYMBOL
            
        )     
 
    

class Fireball(Card):
    def __init__(self, turns_in_hand: int):
        self.turns_in_hand = turns_in_hand
        super().__init__(
            name = FIREBALL_NAME,
            description = f"{FIREBALL_DESC} Currently dealing {3 + self.turns_in_hand} damage.",
            cost = 3,
            effect = {DAMAGE: 3 + self.turns_in_hand},
            symbol = str(self.turns_in_hand)
        
        )
        
        
    def __repr__(self):
        return f'{self.name}({self.turns_in_hand})'  
            
    def increment_turn(self):
        self.turns_in_hand += 1
        self.description = f"{FIREBALL_DESC} Currently dealing {3 + self.turns_in_hand} damage."
        self.effect = {DAMAGE: 3 + self.turns_in_hand}
        self.symbol = str(self.turns_in_hand)


class CardDeck():
    def __init__(self, cards: list[Card]):
        self.deck = cards
        self.size = len(cards)
        self.cards_left = len(cards)
        
        pass
    
    def __str__(self) -> str:
        deck = ','.join(item.symbol for item in self.deck)
        return deck
        
        
    def __repr__(self):
        return f'CardDeck({self.deck})'
    
    
    def is_empty(self) -> bool:
        if self.size == 0:
            return True
        else:
            return False

    def remaining_count(self) -> int:
        return self.size
    
    def draw_cards(self, num: int) -> list[Card]:
        drawn_cards = []
        if num > self.size:
            num = self.size
        
        drawn_cards = self.deck[:num]
        self.deck = self.deck[num:]
        
        self.size -= num
        
        
        return drawn_cards
    
    def add_card(self, card: Card):
        self.deck.append(card)
        self.size += 1
        self.cards_left += 1

class Entity():
    def __init__(self, health: int, shield: int):
        self.health = health
        self.shield = shield
    
    def __repr__(self):
        return f"Entity({self.health}, {self.shield})"
    
    def __str__(self):
        return f"{self.health},{self.shield}"
    
    def get_health(self):
        return self.health
    
    def get_shield(self):
        return self.shield
    
    def apply_shield(self, shield: int):
        self.shield += shield      
    
    def apply_health(self, health: int):
        self.health += health
        
    def apply_damage(self, damage: int):
        while self.shield > 0 and damage > 0:
            self.shield -= 1
            damage -= 1
        
        while self.health > 0 and damage > 0:
            self.health -= 1
            damage -= 1
    
    def apply_effect(self, effect: dict[str, int]):

        if DAMAGE in effect:
            self.apply_damage(effect[DAMAGE])
        if SHIELD in effect:
            self.apply_shield(effect[SHIELD])
        if HEALTH in effect:
            self.apply_health(effect[HEALTH])
    
    def is_alive(self): 
        if self.health > 0:
            return True
        else: 
            return False
        

class Hero(Entity):
    def __init__(self, health: int, shield: int, max_energy: int, deck: CardDeck, hand: list[Card]):
        super().__init__(
            health = health,
            shield = shield,
            
        )
        
        self.max_energy = max_energy
        self.deck = deck
        self.hand = hand
        self.energy = max_energy
        
    def is_alive(self):
        has_health = super().is_alive()
        
        if has_health and self.deck.remaining_count() > 0:
            return True
        else:
            return False

    def __str__(self):
        hand = ','.join(card.symbol for card in self.hand)
        return f"{self.health},{self.shield},{self.max_energy};{self.deck};{hand}"

    def __repr__(self):
        
        return f"Hero({self.health}, {self.shield}, {self.max_energy}, {repr(self.deck)}, {[card for card in self.hand]})"
    
    def get_energy(self):
        return self.energy
    
    def spend_energy(self, energy:int):
        if energy <= self.energy:
            self.energy -= energy
            return True
        else: 
            return False  
    
    def get_max_energy(self):
        return self.max_energy
    
    def get_deck(self):
        return self.deck
    
    def get_hand(self):
        return self.hand
    
    
    def new_turn(self):
        for card in self.hand:
            if isinstance(card, (Fireball)):
                card.increment_turn()
        
        drawn = self.deck.draw_cards(5-len(self.get_hand()))
        self.hand += drawn
        self.max_energy += 1
        self.energy = self.max_energy
        
        

class Minion(Card, Entity):
    def __init__(self, health, shield):
        Card.__init__(
            self, 
            name = MINION_NAME,
            description = MINION_DESC,
            cost = 2,
            effect = {},
            symbol = MINION_SYMBOL
        )
        Entity.__init__(self, health, shield)
        self.permanent = True
        
    
    def __str__(self) -> str:
        return f"{self.name}: {self.description}"
    
    def __repr__(self):
        return f'{self.name}({self.health}, {self.shield})'
    
    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        target = self
        return target
        

class Wyrm(Minion):
    def __init__(self, health, shield):
        Minion.__init__(self, health, shield)
        Card.__init__(
            self, 
            name = WYRM_NAME,
            description = WYRM_DESC,
            cost = 2,
            effect = {HEALTH: 1, SHIELD: 1},
            symbol = WYRM_SYMBOL
            
        )
        self.permanent = True
        
    
    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        wyrm_target = ally_hero
        
        for entity in ally_minions:
            if entity.get_health() < wyrm_target.get_health():    
                wyrm_target = entity
        
        return wyrm_target
    
class Raptor(Minion):
    def __init__(self, health, shield):
        Entity.__init__(self, health, shield)
        Minion.__init__(self, health, shield)
        Card.__init__(
            self, 
            name = RAPTOR_NAME,
            description = RAPTOR_DESC,
            cost = 2,
            effect = {DAMAGE: self.health},
            symbol = RAPTOR_SYMBOL
            
        )
        self.permanent = True

    
    def choose_target(self, ally_hero: Entity, enemy_hero: Entity, ally_minions: list[Entity], enemy_minions: list[Entity]) -> Entity:
        raptor_target = enemy_hero
        if enemy_minions:
            raptor_target = enemy_minions[0]
            for entity in enemy_minions:
                if entity.get_health() > raptor_target.get_health():    
                    raptor_target = entity
        
        return raptor_target
    
    
class HearthModel():
    def __init__(self, player: Hero, active_player_minions: list[Minion], enemy: Hero, active_enemy_minions: list[Minion]):
        self.player = player
        self.active_player_minions = active_player_minions
        self.enemy = enemy
        self.active_enemy_minions = active_enemy_minions
        
        
    
    def __str__(self) -> str:
        enemy_minions = ';'.join(f"{minion.symbol},{minion.health},{minion.shield}" for minion in self.active_enemy_minions)
        player_minions = ';'.join(f"{minion.symbol},{minion.health},{minion.shield}" for minion in self.active_player_minions)
        return f"{str(self.player)}|{player_minions}|{str(self.enemy)}|{enemy_minions}"
    
    def __repr__(self) -> str:
        return f"HearthModel({repr(self.player)}, {repr(self.active_player_minions)}, {repr(self.enemy)}, {repr(self.active_enemy_minions)})"
    
    def get_player(self) -> Hero:
        return self.player
    
    def get_enemy(self) -> Hero:
        return self.enemy
    
    def get_player_minions(self) -> list[Minion]:
        return self.active_player_minions
    
    def get_enemy_minions(self) -> list[Minion]:
        return self.active_enemy_minions  
    
    def has_won(self) -> bool:
        return ((self.player.is_alive() and self.player.deck.size > 0) and (not self.enemy.is_alive() or self.enemy.deck.size == 0))
        
    
    def has_lost(self) -> bool:
        return ((not self.player.is_alive() or self.player.deck.size == 0) and (self.enemy.is_alive() or self.enemy.deck.size > 0))
        
    
    
    def play_card(self, card: Card, target: Entity) -> bool:
        
        if card.get_cost() > self.player.get_energy():
            return False
        
        if  isinstance(card, Minion):
            if len(self.active_player_minions) <= 5:
                self.get_player_minions().append(card)
            else:
                self.get_player_minions().append(card)
                self.get_player_minions().remove(self.get_player_minions()[0])
        else:
            target.apply_effect(card.get_effect())
            if target in self.get_enemy_minions() and target.get_health() <= 0:
                self.active_enemy_minions.remove(target)
        
        self.player.get_hand().remove(card)
        self.player.spend_energy(card.get_cost())
        return True
        
    
    def discard_card(self, card: Card):
        self.player.hand.remove(card)
        self.player.deck.add_card(card)
    
    def end_turn(self) -> list[str]:
        
        for minion in self.get_player_minions():
            target = minion.choose_target(self.get_player(), self.get_enemy(), self.get_player_minions(), self.get_enemy_minions())
            target.apply_effect(minion.get_effect())
            if minion.get_effect() == DAMAGE and not target.is_alive() and target != self.get_enemy():
                self.active_enemy_minions.remove(target)
        
        self.enemy.new_turn()
        enemy_cards_played = []
        if not self.get_enemy().is_alive():
            return "Game Over"
        
        for card in self.enemy.get_hand():
            if card.get_cost() <= self.enemy.get_energy():
                enemy_cards_played.append(card.get_name())
                self.enemy.hand.remove(card)
                self.enemy.spend_energy(card.get_cost())
                target = Entity(0,0)
                if card.is_permanent() == False:
                    if card.get_effect() == DAMAGE:
                        target = self.get_player()
                        if self.get_player_minions():
                            target = self.get_player_minions()[0]
                    else:
                        target = self.get_enemy()
                    
                    target.apply_effect(card.get_effect())
                    
                
        
        for enemy_minion in self.active_enemy_minions:
            minion_target = enemy_minion.choose_target(self.get_enemy(), self.get_player(), self.get_enemy_minions(), self.get_player_minions())
            minion_target.apply_effect(enemy_minion.get_effect())
        
        
        self.player.new_turn()
        return enemy_cards_played

    
def main() -> None:
    deck1 = CardDeck([Shield(),Heal(),Fireball(3),Heal(),Raptor(1,0),Wyrm(1,0),Shield(),Heal(),Heal(),Raptor(1,0)])
    hand1 = [Raptor(2,2), Heal(), Shield(),Fireball(8)]
    player = Hero(5,0,2,deck1,hand1)
    deck2 = CardDeck([Heal(),Shield(),Heal(),Heal(),Raptor(1,2),Wyrm(1,3),Shield(),Heal(),Heal(),Raptor(2,2)])
    hand2 = [Wyrm(1,0),Fireball(0),Raptor(1,0),Shield()]
    enemy = Hero(10,0,3,deck2,hand2)
    player_minions = [Raptor(1,0),Wyrm(1,1)]
    enemy_minions = [Wyrm(1,2)]
    model = HearthModel(Hero(5, 5, 3, CardDeck([Heal(), Raptor(1, 0), Wyrm(1, 0), Shield(), Heal(), Heal(), Raptor(1, 0), Raptor(2, 2)]), [Heal(), Fireball(9), Shield(), Heal(), Fireball(3)]), [Raptor(2, 0), Wyrm(1, 1)], Hero(10, 0, 4, CardDeck([Shield(), Heal(), Heal(), Raptor(1, 2), Wyrm(1, 3), Shield(), Heal(), Heal(), Raptor(2, 2)]), [Fireball(1), Shield(), Heal()]), [Wyrm(2, 2), Wyrm(2, 1), Raptor(1, 0)])
    
    
    print(model.end_turn())


if __name__ == "__main__":
    main()