from typing import List, Literal, NamedTuple, Optional, Tuple


Grass = Literal["grass"]
Fire = Literal["fire"]
Water = Literal["water"]
Electric = Literal["electric"]
Psychic = Literal["psychic"]
Fighting = Literal["fighting"]
Dark = Literal["dark"]
Steel = Literal["steel"]
Fairy = Literal["fairy"]
Dragon = Literal["dragon"]
Normal = Literal["normal"]
Poison = Literal["poison"]
Flying = Literal["flying"]
Bug = Literal["bug"]
Ground = Literal["ground"]
Rock = Literal["rock"]
Ice = Literal["ice"]
Ghost = Literal["ghost"]

PokemonType = (
    Grass
    | Fire
    | Water
    | Electric
    | Psychic
    | Fighting
    | Dark
    | Steel
    | Fairy
    | Dragon
    | Normal
    | Poison
    | Flying
    | Bug
    | Ground
    | Rock
    | Ice
    | Ghost
    | None
)

Basic = Literal["basic"]
Stage1 = Literal["stage1"]
Stage2 = Literal["stage2"]

Stage = Basic | Stage1 | Stage2

Stadium = Literal["stadium"]
Standard = Literal["standard"]
Supporter = Literal["supporter"]
TM = Literal["tm"]
Tool = Literal["tool"]

TrainerType = Stadium | Standard | Supporter | TM | Tool

Active = Literal["active"]
Passive = Literal["passive"]
Unique = Literal["unique"]

AbilityType = Active | Passive | Unique


class WeakRes(NamedTuple):
    type: PokemonType
    value: int


class Attack(NamedTuple):
    name: str
    effect: Optional[str] = None
    cost: Optional[List[PokemonType | Tuple[PokemonType, PokemonType]]] = None
    damage: Optional[int] = None


class Ability(NamedTuple):
    name: str
    effect: str
    type: AbilityType


class TrainerCardData(NamedTuple):
    name: str
    image: str
    type: TrainerType
    effect: Optional[str] = None
    attacks: Optional[List[Attack]] = None


class PokemonCardData(NamedTuple):
    name: str
    hp: int
    stage: str
    type: PokemonType
    image: str
    retreat: int
    rarity: int
    flavor: str
    evolvesFrom: Optional[str] = None
    passive: Optional[Ability] = None
    attacks: Optional[List[Attack]] = None
    weakness: Optional[WeakRes] = None
    resistance: Optional[WeakRes] = None


CardData = TrainerCardData | PokemonCardData

PokemonData = Attack | CardData | Ability | WeakRes
