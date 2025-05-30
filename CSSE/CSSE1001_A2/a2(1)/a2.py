# DO NOT modify or add any import statements
from support import *
from display import HearthView

# Name: Tom Summerton  
# Student Number: 49606782
# Favorite Building: Pyramids of Giza
# -----------------------------------------------------------------------------

# Define your classes and functions here
class Card:
    def __init__(
            self, 
            name: str = CARD_NAME, 
            description: str = CARD_DESC, 
            cost: int = 1, 
            effect: dict[str, int] = {}, 
            symbol = CARD_SYMBOL, 
            **kwargs
            ):
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
        # print(f'shield applied: {shield}')  
        # print(self)  
    
    def apply_health(self, health: int):
        self.health += health
        
    def apply_damage(self, damage: int):
        if self.shield >= damage:
            self.shield -= damage
        else:
            leftover = damage - self.shield
            self.shield = 0
            self.health -= leftover
            if self.health < 0:
                self.health = 0

    def apply_effect(self, effect: dict[str, int]):
        if DAMAGE in effect:
            self.apply_damage(effect[DAMAGE])
        if HEALTH in effect:
            self.apply_health(effect[HEALTH])
        if SHIELD in effect:
            self.apply_shield(effect[SHIELD])
    
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
        
        drawn = self.deck.draw_cards(MAX_HAND-len(self.get_hand()))
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
    
    def choose_target(
            self, 
            ally_hero: Entity, 
            enemy_hero: Entity, 
            ally_minions: list[Entity], 
            enemy_minions: list[Entity]
            ) -> Entity:
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
        
    
    def choose_target(
            self, 
            ally_hero: Entity, 
            enemy_hero: Entity, 
            ally_minions: list[Entity], 
            enemy_minions: list[Entity]
            ) -> Entity:
        
        wyrm_target = ally_hero
        for entity in ally_minions:
            if entity.get_health() < wyrm_target.get_health():    
                wyrm_target = entity

        return wyrm_target
    
class Raptor(Minion):
    def __init__(self, health, shield):
        Minion.__init__(self, health, shield)
        Card.__init__(
            self, 
            name = RAPTOR_NAME,
            description = RAPTOR_DESC,
            cost = 2,
            effect = {DAMAGE: health},
            symbol = RAPTOR_SYMBOL
            
        )
        self.permanent = True

    def get_effect(self):
        return {DAMAGE: self.health}
    
    def choose_target(
            self, 
            ally_hero: Entity, 
            enemy_hero: Entity, 
            ally_minions: list[Entity], 
            enemy_minions: list[Entity]
            ) -> Entity:
        
        raptor_target = enemy_hero
        if enemy_minions:
            raptor_target = enemy_minions[0]
        for entity in enemy_minions:
            if entity.get_health() > raptor_target.get_health():    
                raptor_target = entity
        
        return raptor_target
    
    
class HearthModel():
    def __init__(
            self, 
            player: Hero, 
            active_player_minions: list[Minion], 
            enemy: Hero, 
            active_enemy_minions: list[Minion]
            ):
        self.player = player
        self.active_player_minions = active_player_minions
        self.enemy = enemy
        self.active_enemy_minions = active_enemy_minions
        
        
    
    def __str__(self) -> str:
        enemy_minions = ';'.join(f"{minion.get_symbol()},{minion.get_health()},{minion.get_shield()}" \
                                 for minion in self.active_enemy_minions)
        player_minions = ';'.join(f"{minion.get_symbol()},{minion.get_health()},{minion.get_shield()}" \
                                  for minion in self.active_player_minions)
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
        return (self.player.is_alive() and not self.player.get_deck().is_empty() and \
               (not self.enemy.is_alive() or self.enemy.get_deck().is_empty()))
        
    
    def has_lost(self) -> bool:
        return (not self.player.is_alive() or self.player.get_deck().is_empty())    
    def play_card(self, card: Card, target: Entity) -> bool:
        
        if card.get_cost() > self.player.get_energy():
            return False
        
        if  isinstance(card, Minion):
            if len(self.get_player_minions()) >= MAX_MINIONS:
                self.get_player_minions().pop(0)

            self.get_player_minions().append(card)

        else:
            target.apply_effect(card.get_effect())
            if target in self.get_enemy_minions() and not target.is_alive():
                self.active_enemy_minions.remove(target)
        
        self.player.get_hand().remove(card)
        self.player.spend_energy(card.get_cost())
        return True
        
    
    def discard_card(self, card: Card):
        if isinstance(card, Fireball):
            card.turns_in_hand = 0
        self.player.hand.remove(card)
        self.player.deck.add_card(card)
    
    def end_turn(self) -> list[str]:
        for minion in self.get_player_minions():
            target = minion.choose_target(
                self.get_player(), 
                self.get_enemy(), 
                self.get_player_minions(), 
                self.get_enemy_minions()
                )
            # print(f'{minion.__repr__()} {target.__repr__()}')
            target.apply_effect(minion.get_effect())
            if target in self.active_enemy_minions and not target.is_alive():
                self.active_enemy_minions.remove(target)
        
        self.enemy.new_turn()
        enemy_cards_played = []
        
        if self.has_won() or self.has_lost():
            return enemy_cards_played
        
        
        enemy_hand_copy = self.enemy.hand.copy()
        i = 0
        while i < len(enemy_hand_copy):
            card = enemy_hand_copy[i]
            if card.get_cost() <= self.enemy.get_energy():
                enemy_cards_played.append(card.get_name())
                self.enemy.hand.remove(card)
                self.enemy.spend_energy(card.get_cost())
                if not isinstance(card, Minion):
                    target = self.get_player() 
                    if DAMAGE not in card.get_effect():
                        target = self.get_enemy()
                    target.apply_effect(card.get_effect())
                else:
                    if len(self.active_enemy_minions) >= MAX_MINIONS:
                        self.active_enemy_minions.pop(0)
                    self.active_enemy_minions.append(card)
                
                enemy_hand_copy = self.enemy.get_hand().copy()
                i = 0
            else:
                i += 1

        
        for enemy_minion in self.active_enemy_minions:
            minion_target = enemy_minion.choose_target(
                self.get_enemy(), 
                self.get_player(), 
                self.get_enemy_minions(), 
                self.get_player_minions()
                )
            # print(f'{enemy_minion.__repr__()} {minion_target.__repr__()}')
            minion_target.apply_effect(enemy_minion.get_effect())
            # print(minion_target.__repr__())
            if minion_target in self.active_player_minions and not minion_target.is_alive():
                self.active_player_minions.remove(minion_target)
        
        if not self.has_won() and not self.has_lost():
            self.player.new_turn()
        return enemy_cards_played


class Hearthstone():
    def __init__(self, file: str):
        self.file = file
        # self.model = HearthModel
        self.view = HearthView()

    def __str__(self) -> str:
        return f'{CONTROLLER_DESC}{self.file}'

    def __repr__(self) -> str:
        return f'Hearthstone({self.file})' 

    def string_played_minion_convert(self, string_rep: str) -> Card:
        if string_rep[0] == RAPTOR_SYMBOL:
            return Raptor(string_rep[1],string_rep[2])
        elif string_rep[0] == WYRM_SYMBOL:
            return Wyrm(string_rep[1],string_rep[2])

    def string_unplayed_card_convert(self, string_rep: str) -> Card:

        if string_rep == RAPTOR_SYMBOL:
            return Raptor(1,0)
        elif string_rep == WYRM_SYMBOL:
            return Wyrm(1,0)
        elif string_rep == HEAL_SYMBOL:
            return Heal()
        elif string_rep == SHIELD_SYMBOL:
            return Shield()
        elif ord(string_rep[0]) <= 57 and ord(string_rep[0]) >= 48:
            return Fireball(int(string_rep))
    
    def string_player_stats_convert(self, string_rep: str) -> list[int]:
        output = []
        for character in string_rep:
            if character != ',':
                output.append(int(character))

        return output

    def build_model(self, string_rep: str) -> HearthModel:
        PLAYER_INDEX = 0
        PLAYER_MINIONS_INDEX = 1
        ENEMY_INDEX = 2
        ENEMY_MINIONS_INDEX = 3
        STATS_SUBINDEX = 0
        DECK_SUBINDEX = 1
        HAND_SUBINDEX = 2

        sep_parts = string_rep.split('|')
        for i in range(len(sep_parts)):
            sep_parts[i] = sep_parts[i].split(';')

        model_output = ''

        string_rep_player_stats = sep_parts[PLAYER_INDEX][STATS_SUBINDEX]
        string_rep_player_deck = sep_parts[PLAYER_INDEX][DECK_SUBINDEX]
        string_rep_player_hand = sep_parts[PLAYER_INDEX][HAND_SUBINDEX]

        string_rep_player_minions = sep_parts[PLAYER_MINIONS_INDEX]

        string_rep_enemy_stats = sep_parts[ENEMY_INDEX][STATS_SUBINDEX]
        string_rep_enemy_deck = sep_parts[ENEMY_INDEX][DECK_SUBINDEX]
        string_rep_enemy_hand = sep_parts[ENEMY_INDEX][HAND_SUBINDEX]

        string_rep_enemy_minions = sep_parts[ENEMY_MINIONS_INDEX]

        player_stats = self.string_player_stats_convert(string_rep_player_stats)
        player_health = player_stats[0]
        player_shield = player_stats[1]
        player_max_energy = player_stats[2]
        player_deck_list = []
        for card_in_deck in string_rep_player_deck:
            card_in_deck = self.string_unplayed_card_convert(card_in_deck)
            player_deck_list.append(card_in_deck)
        player_deck = CardDeck(player_deck_list)

        player_hand = []
        for card_in_hand in string_rep_player_hand:
            card_in_hand = self.string_unplayed_card_convert(card_in_hand)
            player_hand.append(card_in_hand)

        player_minions = []
        for player_active_minion in string_rep_player_minions:
            player_active_minion = self.string_played_minion_convert(player_active_minion)
            player_minions.append(player_active_minion)
        

        enemy_stats = self.string_player_stats_convert(string_rep_enemy_stats)
        enemy_health = enemy_stats[0]
        enemy_shield = enemy_stats[1]
        enemy_max_energy = enemy_stats[2]
        enemy_deck_list = []
        for card_in_enemy_deck in string_rep_enemy_deck:
            card_in_enemy_deck = self.string_unplayed_card_convert(card_in_enemy_deck)
            enemy_deck_list.append(card_in_enemy_deck)
        enemy_deck = CardDeck(enemy_deck_list)

        enemy_hand = []
        for card_in_enemy_hand in string_rep_enemy_hand:
            card_in_enemy_hand = self.string_unplayed_card_convert(card_in_enemy_hand)
            enemy_hand.append(card_in_hand)

        enemy_minions = []
        for enemy_active_minion in string_rep_enemy_minions:
            enemy_active_minion = self.string_played_minion_convert(enemy_active_minion)
            enemy_minions.append(enemy_active_minion)


        player_output = Hero(player_health, player_shield, player_max_energy, player_deck, player_hand)
        player_minion_output = player_minions
        enemy_output = Hero(enemy_health, enemy_shield, enemy_max_energy, enemy_deck, enemy_hand)
        enemy_minion_output = enemy_minions

        model_output = HearthModel(player_output, player_minion_output, enemy_output, enemy_minion_output)

        return model_output

    def update_display(self, messages: list[str]):
        pass 

    # def get_command(self) -> str:
    #     user_command = input(COMMAND_PROMPT) 
    #     if user_command.lower() == HELP_COMMAND:
    #         return HELP_MESSAGES
    #     elif user_command.lower() == END_TURN_COMMAND:
    #         return self.model.end_turn()
    #     elif PLAY_COMMAND in user_command.lower():
    #         card_to_play = user_command[len(user_command-1)]
            
    #     elif user_command.lower() == DISCARD_COMMAND:
    #         return DISCARD_COMMAND
    #     elif user_command.lower() == LOAD_COMMAND:
    #         return LOAD_COMMAND
    #     else:
    #         return INVALID_COMMAND

    # def get_target_entity(self) -> str:
    #     input_target_for_card = input(ENTITY_PROMPT)
    #     target_for_card = ''
    #     if 'm' in input_target_for_card.lower():
    #         target_for_card = self.model.get_player()
    #         return str(target_for_card)
    #     elif 'o' in input_target_for_card.lower():
    #         target_for_card = self.model.get_enemy()
    #         return str(target_for_card)
    #     elif int(input_target_for_card) in range(10):
    #         if int(input_target_for_card) <= 5:
    #             target_for_card = int(input_target_for_card)-1
    #             return f'{PLAYER_SELECT}{str(target_for_card)}'
    #         else:
    #             target_for_card = int(input_target_for_card)-6
    #             return f'{ENEMY_SELECT}{str(target_for_card)}' 
    #     else:
    #         self.get_target_entity()

    def save_game(self):
        save_loc = open(SAVE_LOC, 'w')
        save_loc.write() 

    def load_game(self, file: str):
        print(file)
        file_instance = file.open(file, 'r')
        print(file_instance.read())
        data = file_instance.read()
        return data


    def play(self):
        pass 

    
def main() -> None:
    
    stone = Hearthstone('practice_deck.txt')

    # string = stone.load_game(stone.file)

    f = open(practice_deck.txt, 'r')
    string = f.read()
    print(string)
    pass

if __name__ == "__main__":
    main()