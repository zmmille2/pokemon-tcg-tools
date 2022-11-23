from typing import List, NamedTuple, Optional

class WeakRes(NamedTuple):
    type: str
    value: int


class Attack(NamedTuple):
    name: str
    effect: Optional[str] = None
    cost: Optional[str] = None
    damage: Optional[int] = None


class Passive(NamedTuple):
    name: str
    effect: str
    type: str


class TrainerCardData(NamedTuple):
    name: str
    image: str
    type: str
    effect: Optional[str] = None
    attacks: Optional[List[Attack]] = None


class CardData(NamedTuple):
    name: str
    hp: int
    stage: str
    type: str
    image: str
    retreat: int
    rarity: int
    flavor: str
    evolvesFrom: Optional[str] = None
    passive: Optional[Passive] = None
    attacks: Optional[List[Attack]] = None
    weakness: Optional[WeakRes] = None
    resistance: Optional[WeakRes] = None

PokemonData = Attack | CardData | Passive | TrainerCardData | WeakRes

