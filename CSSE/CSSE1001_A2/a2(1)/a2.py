# DO NOT modify or add any import statements
from support import *
from display import HearthView

# Name: Tom Summerton  
# Student Number: 49606782
# Favorite Building: Pyramids of Giza
# -----------------------------------------------------------------------------

# Define your classes and functions here
class Card:
    """
    Represents a card in the game, with a name, description, cost, effect, and symbol.
    """
    def __init__(
            self, 
            name: str = CARD_NAME, 
            description: str = CARD_DESC, 
            cost: int = 1, 
            effect: dict[str, int] = {}, 
            symbol = CARD_SYMBOL, 
            **kwargs
            ):
        self._name = name
        self._description = description
        self._cost = cost
        self._effect = effect
        self._symbol = symbol
        self._permanent = False

    def __str__(self) -> str:
        """
        Return a string representation of the card in the format: "name: description".
        """
        return f"{self._name}: {self._description}"

    def __repr__(self) -> str:
        """
        Return a string representation of the card for debugging.
        """
        return f'{self._name}()'

    def get_symbol(self) -> str:
        """
        Return the symbol of the card.
        """
        return self._symbol
    
    def get_name(self) -> str:
        """
        Return the name of the card.
        """
        return self._name
    
    def get_cost(self) -> int:
        """
        Return the energy cost to play the card.
        """
        return self._cost

    def get_effect(self) -> dict[str, int]:
        """
        Return the effect dictionary of the card.
        """
        return self._effect

    def is_permanent(self) -> bool:
        """
        Return whether the card is permanent (e.g., a minion).
        """
        return self._permanent

class Shield(Card):
    """
    Represents a Shield card that adds shield to an entity.
    """
    def __init__(self):
        """
        Initialize a Shield card.
        """
        super().__init__(
            name = SHIELD_NAME,
            description = SHIELD_DESC,
            cost = 1,
            effect = {SHIELD: 5},
            symbol = SHIELD_SYMBOL
        )

class Heal(Card):
    """
    Represents a Heal card that restores health to an entity.
    """
    def __init__(self):
        """
        Initialize a Heal card.
        """
        super().__init__(
            name = HEAL_NAME,
            description = HEAL_DESC,
            cost = 2,
            effect = {HEALTH: 2},
            symbol = HEAL_SYMBOL
        )     

class Fireball(Card):
    """
    Represents a Fireball card that deals increasing damage the longer it is held.
    """
    def __init__(self, turns_in_hand: int):
        """
        Initialize a Fireball card.
        
        Args:
            turns_in_hand (int): The number of turns the card has been in hand.
        """
        self._turns_in_hand = turns_in_hand
        super().__init__(
            name = FIREBALL_NAME,
            description = f"{FIREBALL_DESC} Currently dealing {3 + self._turns_in_hand} damage.",
            cost = 3,
            effect = {DAMAGE: 3 + self._turns_in_hand},
            symbol = str(self._turns_in_hand)
        )
        
    def __repr__(self):
        """
        Return a string representation of the Fireball card for debugging.
        """
        return f'{self._name}({self._turns_in_hand})'  
            
    def increment_turn(self):
        """
        Increment the number of turns the Fireball has been in hand and update its effect.
        """
        self._turns_in_hand += 1
        self._description = f"{FIREBALL_DESC} Currently dealing {3 + self._turns_in_hand} damage."
        self._effect = {DAMAGE: 3 + self._turns_in_hand}
        self._symbol = str(self._turns_in_hand)

class CardDeck():
    """
    Represents a deck of cards.
    """
    def __init__(self, cards: list[Card]):
        """
        Initialize a CardDeck.
        
        Args:
            cards (list[Card]): The list of cards in the deck.
        """
        self._deck = cards
        self._size = len(cards)
        self._cards_left = len(cards)
    
    def __str__(self) -> str:
        """
        Return a string representation of the deck using card symbols.
        """
        deck = ','.join(item._symbol for item in self._deck)
        return deck
        
    def __repr__(self):
        """
        Return a string representation of the CardDeck for debugging.
        """
        return f'CardDeck({self._deck})'
    
    def is_empty(self) -> bool:
        """
        Return True if the deck is empty, False otherwise.
        """
        return self._size == 0

    def remaining_count(self) -> int:
        """
        Return the number of cards remaining in the deck.
        """
        return self._size
    
    def draw_cards(self, num: int) -> list[Card]:
        """
        Draw a number of cards from the deck.
        
        Args:
            num (int): The number of cards to draw.
        Returns:
            list[Card]: The drawn cards.
        """
        drawn_cards = []
        if num > self._size:
            num = self._size
        drawn_cards = self._deck[:num]
        self._deck = self._deck[num:]
        self._size -= num
        return drawn_cards
    
    def add_card(self, card: Card):
        """
        Add a card to the deck.
        
        Args:
            card (Card): The card to add.
        """
        self._deck.append(card)
        self._size += 1
        self._cards_left += 1

class Entity():
    """
    Represents an entity in the game (hero or minion) with health and shield.
    """
    def __init__(self, health: int, shield: int):
        """
        Initialize an Entity.
        
        Args:
            health (int): The health of the entity.
            shield (int): The shield value of the entity.
        """
        self._health = health
        self._shield = shield
    
    def __repr__(self):
        """
        Return a string representation of the Entity for debugging.
        """
        return f"Entity({self._health}, {self._shield})"
    
    def __str__(self):
        """
        Return a string representation of the Entity.
        """
        return f"{self._health},{self._shield}"
    
    def get_health(self):
        """
        Return the health of the entity.
        """
        return self._health
    
    def get_shield(self):
        """
        Return the shield value of the entity.
        """
        return self._shield
    
    def apply_shield(self, shield: int):
        """
        Add shield to the entity.
        
        Args:
            shield (int): The amount of shield to add.
        """
        self._shield += shield  

    def apply_health(self, health: int):
        """
        Add health to the entity.
        
        Args:
            health (int): The amount of health to add.
        """
        self._health += health
        
    def apply_damage(self, damage: int):
        """
        Apply damage to the entity, reducing shield first, then health.
        
        Args:
            damage (int): The amount of damage to apply.
        """
        if self._shield >= damage:
            self._shield -= damage
        else:
            leftover = damage - self._shield
            self._shield = 0
            self._health -= leftover
            if self._health < 0:
                self._health = 0

    def apply_effect(self, effect: dict[str, int]):
        """
        Apply an effect dictionary to the entity.
        
        Args:
            effect (dict[str, int]): The effect to apply.
        """
        if DAMAGE in effect:
            self.apply_damage(effect[DAMAGE])
        if HEALTH in effect:
            self.apply_health(effect[HEALTH])
        if SHIELD in effect:
            self.apply_shield(effect[SHIELD])
    
    def is_alive(self): 
        """
        Return True if the entity is alive (health > 0), False otherwise.
        """
        return self._health > 0

class Hero(Entity):
    """
    Represents a hero in the game, which is a special type of entity with energy, a deck, and a hand.
    """
    def __init__(self, health: int, shield: int, max_energy: int, deck: CardDeck, hand: list[Card]):
        """
        Initialize a Hero.
        
        Args:
            health (int): The health of the hero.
            shield (int): The shield value of the hero.
            max_energy (int): The maximum energy of the hero.
            deck (CardDeck): The hero's deck.
            hand (list[Card]): The hero's hand.
        """
        super().__init__(
            health = health,
            shield = shield,
        )
        self._max_energy = max_energy
        self._deck = deck
        self._hand = hand
        self._energy = max_energy
        
    def is_alive(self):
        """
        Return True if the hero is alive and has cards in their deck, False otherwise.
        """
        has_health = super().is_alive()
        if has_health and self._deck.remaining_count() > 0:
            return True
        else:
            return False

    def __str__(self):
        """
        Return a string representation of the hero, including health, shield, energy, deck, and hand.
        """
        hand = ','.join(card._symbol for card in self._hand)
        return f"{self._health},{self._shield},{self._max_energy};{self._deck};{hand}"

    def __repr__(self):
        """
        Return a string representation of the Hero for debugging.
        """
        return f"Hero({self._health}, {self._shield}, {self._max_energy}, {repr(self._deck)}, {[card for card in self._hand]})"
    
    def get_energy(self):
        """
        Return the current energy of the hero.
        """
        return self._energy
    
    def spend_energy(self, energy:int):
        """
        Spend energy from the hero.
        
        Args:
            energy (int): The amount of energy to spend.
        Returns:
            bool: True if energy was spent, False otherwise.
        """
        if energy <= self._energy:
            self._energy -= energy
            return True
        else: 
            return False  
    
    def get_max_energy(self):
        """
        Return the maximum energy of the hero.
        """
        return self._max_energy
    
    def get_deck(self):
        """
        Return the hero's deck.
        """
        return self._deck
    
    def get_hand(self):
        """
        Return the hero's hand.
        """
        return self._hand
    
    def new_turn(self):
        """
        Start a new turn for the hero: increment fireball turns, draw up to max hand, and refresh energy.
        """
        for card in self._hand:
            if isinstance(card, (Fireball)):
                card.increment_turn()
        drawn = self._deck.draw_cards(MAX_HAND-len(self._hand))
        self._hand += drawn
        self._max_energy += 1
        self._energy = self._max_energy

class Minion(Card, Entity):
    """
    Represents a minion card that is also an entity.

    Example:
        >>> m = Minion(3, 2)
        >>> m.get_health()
        3
        >>> m.get_shield()
        2
        >>> m.is_permanent()
        True
    """
    def __init__(self, health, shield):
        """
        Initialize a Minion.

        Args:
            health (int): The health of the minion.
            shield (int): The shield value of the minion.

        Example:
            >>> Minion(3, 2)
        """
        Entity.__init__(self, health, shield)
        Card.__init__(
            self, 
            name = MINION_NAME,
            description = MINION_DESC,
            cost = 2,
            effect = {},
            symbol = MINION_SYMBOL
        )
        self._permanent = True
    
    def __str__(self) -> str:
        """
        Return a string representation of the minion.

        Example:
            >>> str(Minion(3, 2))
            'Minion: A basic minion.'
        """
        return f"{self._name}: {self._description}"
    
    def __repr__(self):
        """
        Return a string representation of the minion for debugging.

        Example:
            >>> repr(Minion(3, 2))
            'Minion(3, 2)'
        """
        return f'{self._name}({self._health}, {self._shield})'
    
    def choose_target(
            self, 
            ally_hero: Entity, 
            enemy_hero: Entity, 
            ally_minions: list[Entity], 
            enemy_minions: list[Entity]
            ) -> Entity:
        """
        Choose a target for the minion's effect.

        Example:
            >>> m = Minion(3, 2)
            >>> m.choose_target(Entity(10, 0), Entity(8, 0), [], [])
            Minion(3, 2)
        """
        target = self
        return target

class Wyrm(Minion):
    """
    Represents a Wyrm minion with a healing and shielding effect.

    Example:
        >>> w = Wyrm(2, 1)
        >>> w.get_effect()
        {'health': 1, 'shield': 1}
    """
    def __init__(self, health, shield):
        """
        Initialize a Wyrm minion.

        Example:
            >>> Wyrm(2, 1)
        """
        Minion.__init__(self, health, shield)
        Card.__init__(
            self, 
            name = WYRM_NAME,
            description = WYRM_DESC,
            cost = 2,
            effect = {HEALTH: 1, SHIELD: 1},
            symbol = WYRM_SYMBOL
        )
        self._permanent = True
    
    def choose_target(
            self, 
            ally_hero: Entity, 
            enemy_hero: Entity, 
            ally_minions: list[Entity], 
            enemy_minions: list[Entity]
            ) -> Entity:
        """
        Choose the ally with the lowest health as the target for the Wyrm's effect.

        Example:
            >>> w = Wyrm(2, 1)
            >>> hero = Entity(10, 0)
            >>> minion = Minion(5, 0)
            >>> w.choose_target(hero, None, [minion], [])
            Minion(5, 0)
        """
        wyrm_target = ally_hero
        for entity in ally_minions:
            if entity.get_health() < wyrm_target.get_health():    
                wyrm_target = entity
        return wyrm_target

class Raptor(Minion):
    """
    Represents a Raptor minion that deals damage equal to its health.

    Example:
        >>> r = Raptor(4, 1)
        >>> r.get_effect()
        {'damage': 4}
    """
    def __init__(self, health, shield):
        """
        Initialize a Raptor minion.

        Example:
            >>> Raptor(4, 1)
        """
        Minion.__init__(self, health, shield)
        Card.__init__(
            self, 
            name = RAPTOR_NAME,
            description = RAPTOR_DESC,
            cost = 2,
            effect = {DAMAGE: health},
            symbol = RAPTOR_SYMBOL
        )
        self._permanent = True

    def get_effect(self):
        """
        Return the effect of the Raptor (damage equal to its current health).

        Example:
            >>> r = Raptor(4, 1)
            >>> r.get_effect()
            {'damage': 4}
        """
        return {DAMAGE: self._health}
    
    def choose_target(
            self, 
            ally_hero: Entity, 
            enemy_hero: Entity, 
            ally_minions: list[Entity], 
            enemy_minions: list[Entity]
            ) -> Entity:
        """
        Choose the enemy minion with the highest health, or the enemy hero if no minions.

        Example:
            >>> r = Raptor(4, 1)
            >>> hero = Entity(10, 0)
            >>> minion1 = Minion(3, 0)
            >>> minion2 = Minion(5, 0)
            >>> r.choose_target(None, hero, [], [minion1, minion2])
            Minion(5, 0)
        """
        raptor_target = enemy_hero
        if enemy_minions:
            raptor_target = enemy_minions[0]
        for entity in enemy_minions:
            if entity.get_health() > raptor_target.get_health():    
                raptor_target = entity
        return raptor_target

class HearthModel():
    """
    Represents the state of the game, including both players and their minions.
    """
    def __init__(
            self, 
            player: Hero, 
            active_player_minions: list[Minion], 
            enemy: Hero, 
            active_enemy_minions: list[Minion]
            ):
        """
        Initialize the HearthModel.
        """
        self._player = player
        self._active_player_minions = active_player_minions
        self._enemy = enemy
        self._active_enemy_minions = active_enemy_minions
    
    def __str__(self) -> str:
        """
        Return a string representation of the game state.
        """
        enemy_minions = ';'.join(f"{minion._symbol},{minion._health},{minion._shield}" for minion in self._active_enemy_minions)
        player_minions = ';'.join(f"{minion._symbol},{minion._health},{minion._shield}" for minion in self._active_player_minions)
        return f"{str(self._player)}|{player_minions}|{str(self._enemy)}|{enemy_minions}"
    
    def __repr__(self) -> str:
        """
        Return a string representation of the HearthModel for debugging.
        """
        return f"HearthModel({repr(self._player)}, {repr(self._active_player_minions)}, {repr(self._enemy)}, {repr(self._active_enemy_minions)})"
    
    def get_player(self) -> Hero:
        """
        Return the player hero.
        """
        return self._player
    
    def get_enemy(self) -> Hero:
        """
        Return the enemy hero.
        """
        return self._enemy
    
    def get_player_minions(self) -> list[Minion]:
        """
        Return the list of active player minions.
        """
        return self._active_player_minions
    
    def get_enemy_minions(self) -> list[Minion]:
        """
        Return the list of active enemy minions.
        """
        return self._active_enemy_minions  
    
    def has_won(self) -> bool:
        """
        Return True if the player has won the game.
        """
        return (self._player.is_alive() and not self._player._deck.is_empty() and \
               (not self._enemy.is_alive() or self._enemy._deck.is_empty()))
    
    def has_lost(self) -> bool:
        """
        Return True if the player has lost the game.
        """
        return (not self._player.is_alive() or self._player._deck.is_empty())    
    
    def play_card(self, card: Card, target: Entity) -> bool:
        """
        Play a card, applying its effect to the target or summoning a minion.
        
        Args:
            card (Card): The card to play.
            target (Entity): The target of the card's effect.
        Returns:
            bool: True if the card was played, False otherwise.
        """
        if card._cost > self._player._energy:
            return False
        if  isinstance(card, Minion):
            if len(self._active_player_minions) >= MAX_MINIONS:
                self._active_player_minions.pop(0)
            self._active_player_minions.append(card)
        else:
            target.apply_effect(card._effect)
            if target in self._active_enemy_minions and not target.is_alive():
                self._active_enemy_minions.remove(target)
        self._player._hand.remove(card)
        self._player.spend_energy(card._cost)
        return True
    
    def discard_card(self, card: Card):
        """
        Discard a card from the player's hand and add it to the deck.
        
        Args:
            card (Card): The card to discard.
        """
        if isinstance(card, Fireball):
            card._turns_in_hand = 0
        self._player._hand.remove(card)
        self._player._deck.add_card(card)
    
    def end_turn(self) -> list[str]:
        """
        End the player's turn, process minion actions, and handle the enemy's turn.
        
        Returns:
            list[str]: The names of enemy cards played.
        """
        for minion in self._active_player_minions:
            target = minion.choose_target(
                self._player, 
                self._enemy, 
                self._active_player_minions, 
                self._active_enemy_minions
                )
            target.apply_effect(minion.get_effect())
            if target in self._active_enemy_minions and not target.is_alive():
                self._active_enemy_minions.remove(target)
        
        self._enemy.new_turn()
        enemy_cards_played = []
        
        if self.has_won() or self.has_lost():
            return enemy_cards_played
        
        enemy_hand_copy = self._enemy._hand.copy()
        i = 0
        while i < len(enemy_hand_copy):
            card = enemy_hand_copy[i]
            if card._cost <= self._enemy._energy:
                enemy_cards_played.append(card._name)
                self._enemy._hand.remove(card)
                self._enemy.spend_energy(card._cost)
                if not isinstance(card, Minion):
                    target = self._player 
                    if DAMAGE not in card._effect:
                        target = self._enemy
                    target.apply_effect(card._effect)
                else:
                    if len(self._active_enemy_minions) >= MAX_MINIONS:
                        self._active_enemy_minions.pop(0)
                    self._active_enemy_minions.append(card)
                enemy_hand_copy = self._enemy._hand.copy()
                i = 0
            else:
                i += 1

        for enemy_minion in self._active_enemy_minions:
            minion_target = enemy_minion.choose_target(
                self._enemy, 
                self._player, 
                self._active_enemy_minions, 
                self._active_player_minions
                )
            minion_target.apply_effect(enemy_minion.get_effect())
            if minion_target in self._active_player_minions and not minion_target.is_alive():
                self._active_player_minions.remove(minion_target)
        
        if not self.has_won() and not self.has_lost():
            self._player.new_turn()
        return enemy_cards_played

class Hearthstone():
    """
    The main controller class for the Hearthstone game.
    Handles loading, saving, and running the game loop.
    """
    def __init__(self, file: str):
        """
        Initialize the Hearthstone controller.
        
        Args:
            file (str): The file path to load the game state from.
        """
        self._file = file
        self._model = 0
        self.load_game(self._file)
        self._view = HearthView()

    def __str__(self) -> str:
        """
        Return a string representation of the controller.
        """
        return f'{CONTROLLER_DESC}{self._file}'

    def __repr__(self) -> str:
        """
        Return a string representation of the controller for debugging.
        """
        return f'Hearthstone({self._file})' 

    def string_played_minion_convert(self, string_rep: str) -> Card:
        """
        Convert a string representation of a played minion to a Minion object.
        
        Args:
            string_rep (str): The string representation.
        Returns:
            Card: The corresponding Minion object, or None if invalid.
        """
        if string_rep != '':
            if string_rep[0] == RAPTOR_SYMBOL:
                return Raptor(string_rep[1],string_rep[2])
            elif string_rep[0] == WYRM_SYMBOL:
                return Wyrm(string_rep[1],string_rep[2])
            elif string_rep[0] == MINION_SYMBOL:
                return Minion(string_rep[1],string_rep[2])

    def string_unplayed_card_convert(self, string_rep: str) -> Card:
        """
        Convert a string representation of an unplayed card to a Card object.
        
        Args:
            string_rep (str): The string representation.
        Returns:
            Card: The corresponding Card object, or None if invalid.
        """
        if string_rep == RAPTOR_SYMBOL:
            return Raptor(1,0)
        elif string_rep == WYRM_SYMBOL:
            return Wyrm(1,0)
        elif string_rep == MINION_SYMBOL:
            return Minion(1,0)
        elif string_rep == HEAL_SYMBOL:
            return Heal()
        elif string_rep == SHIELD_SYMBOL:
            return Shield()
        elif ord(string_rep[0]) <= 57 and ord(string_rep[0]) >= 48:
            return Fireball(int(string_rep))
    
    def string_player_stats_convert(self, string_rep: str) -> list[int]:
        """
        Convert a string representation of player stats to a list of integers.
        
        Args:
            string_rep (str): The string representation.
        Returns:
            list[int]: The player stats as integers.
        """
        output = []
        string_rep = string_rep.split(',')
        for character in string_rep:
            output.append(int(character))
        return output

    def build_model(self, string_rep: str) -> HearthModel:
        """
        Build a HearthModel from a string representation of the game state.
        
        Args:
            string_rep (str): The string representation.
        Returns:
            HearthModel: The constructed game model.
        """
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
            if card_in_deck is not None:
                player_deck_list.append(card_in_deck)
        player_deck = CardDeck(player_deck_list)

        player_hand = []
        for card_in_hand in string_rep_player_hand:
            card_in_hand = self.string_unplayed_card_convert(card_in_hand)
            if card_in_hand is not None:
                player_hand.append(card_in_hand)

        player_minions = []
        for player_active_minion in string_rep_player_minions:
            player_active_minion = self.string_played_minion_convert(player_active_minion)
            if player_active_minion is not None:
                player_minions.append(player_active_minion)
        
        enemy_stats = self.string_player_stats_convert(string_rep_enemy_stats)
        enemy_health = enemy_stats[0]
        enemy_shield = enemy_stats[1]
        enemy_max_energy = enemy_stats[2]
        enemy_deck_list = []
        for card_in_enemy_deck in string_rep_enemy_deck:
            card_in_enemy_deck = self.string_unplayed_card_convert(card_in_enemy_deck)
            if card_in_enemy_deck is not None:
                enemy_deck_list.append(card_in_enemy_deck)
        enemy_deck = CardDeck(enemy_deck_list)

        enemy_hand = []
        for card_in_enemy_hand in string_rep_enemy_hand:
            card_in_enemy_hand = self.string_unplayed_card_convert(card_in_enemy_hand)
            if card_in_enemy_hand is not None:
                enemy_hand.append(card_in_enemy_hand)

        enemy_minions = []
        for enemy_active_minion in string_rep_enemy_minions:
            enemy_active_minion = self.string_played_minion_convert(enemy_active_minion)
            if enemy_active_minion is not None:
                enemy_minions.append(enemy_active_minion)

        player_output = Hero(player_health, player_shield, player_max_energy, player_deck, player_hand)
        player_minion_output = player_minions
        enemy_output = Hero(enemy_health, enemy_shield, enemy_max_energy, enemy_deck, enemy_hand)
        enemy_minion_output = enemy_minions

        model_output = HearthModel(player_output, player_minion_output, enemy_output, enemy_minion_output)
        return model_output

    def update_display(self, messages: list[str]):
        """
        Update the game display with the current model and messages.
        
        Args:
            messages (list[str]): The messages to display.
        """
        view = HearthView() 
        view.update(self._model.get_player(), self._model.get_enemy(),self._model.get_player_minions(),self._model.get_enemy_minions(), messages)
    
    def get_command(self) -> str:
        """
        Get a command from the user.
        
        Returns:
            str: The command entered by the user.
        """
        user_command = input(COMMAND_PROMPT) 
        if user_command.lower() == HELP_COMMAND:
            return HELP_MESSAGES
        elif user_command.lower() == END_TURN_COMMAND:
            return user_command.lower()
        elif PLAY_COMMAND in user_command.lower():
            return user_command[0:6].lower()
        elif DISCARD_COMMAND in user_command.lower():
            return user_command.lower()
        elif user_command.lower() == LOAD_COMMAND:
            return user_command.lower()
        else:
            print(INVALID_COMMAND)
            self.get_command()
                  

    def get_target_entity(self) -> str:
        """
        Get the target entity for a card from user input.
        
        Returns:
            str: The target entity identifier.
        """
        input_target_for_card = input(ENTITY_PROMPT)
        if 'm' in input_target_for_card.lower():
            return PLAYER_SELECT
        elif 'o' in input_target_for_card.lower():
            return ENEMY_SELECT
        elif int(input_target_for_card) in range(10):
            if int(input_target_for_card) <= 5:
                target_for_card = int(input_target_for_card)-1
                return f'{ENEMY_SELECT}{str(target_for_card)}' 
            else:
                target_for_card = int(input_target_for_card)-5
                return f'{PLAYER_SELECT}{str(target_for_card)}'
        else:
            self.update_display([INVALID_ENTITY])
            self.get_target_entity()

    def save_game(self):
        """
        Save the current game state to a file.
        """
        save_loc = open(SAVE_LOC, 'w')
        save_loc.write(self._model.__str__()) 

    def load_game(self, file: str):
        """
        Load the game state from a file.
        
        Args:
            file (str): The file path to load from.
        """
        file_instance = open(file, 'r')
        data = file_instance.read()
        self._model = self.build_model(data)

    def play(self):
        """
        Run the main game loop.
        """
        game = self.load_game(self._file)
        self.update_display([WELCOME_MESSAGE])
        game_on = True
        while game_on:
            input = self.get_command()
            if input == HELP_MESSAGES:
                for message in input:
                    print(message)
            elif DISCARD_COMMAND in input:
                discarded_card = self._model._player._hand[int(input[-1])]
                self._model.discard_card(discarded_card)
                self.update_display([f'{DISCARD_MESSAGE}{discarded_card._name}'])
            elif PLAY_COMMAND in input:
                pass
            elif input == END_TURN_COMMAND:
                actions = self._model.end_turn()
                end_turn_message = []
                for move in actions:
                    end_turn_message.append(f'{ENEMY_PLAY_MESSAGE}{move}')
                if self._model.has_won() or self._model.has_lost():
                    game_on = False
                    break
                self.save_game()
                end_turn_message.append(GAME_SAVE_MESSAGE)
                self.update_display(end_turn_message)

        if self._model.has_won():
            self.update_display([WIN_MESSAGE])
        else:
            self.update_display([LOSS_MESSAGE])

def play_game(file: str):
    """
    Constructs a controller and plays a single game of Hearthstone.
    If loading the given file fails with ValueError or FileNotFoundError,
    attempts to load from 'autosave.txt' instead.
    """
    try:
        controller = Hearthstone(file)
    except (ValueError, FileNotFoundError):
        controller = Hearthstone('autosave.txt')
    controller.play()

def main() -> None:
    """
    The main entry point for the program.
    """
    play_game('levels/deck1.txt')

if __name__ == "__main__":
    main()