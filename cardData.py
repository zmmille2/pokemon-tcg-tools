from typing import List, NamedTuple

class WeakRes(NamedTuple):
  type: str
  value: int

class Attack(NamedTuple):
  name: str
  cost: str
  damage: int
  effect: str

class Passive(NamedTuple):
  name: str
  effect: str
  type: str

class CardData(NamedTuple):
  name: str
  hp: int
  stage: str
  evolvesFrom: str
  type: str
  image: str
  passive: Passive
  attacks: List[Attack]
  weakness: WeakRes
  resistance: WeakRes
  retreat: int
  rarity: int
  flavor: str
