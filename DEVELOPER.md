# Dev Docs

These docs should give you everything you need to know to start making your own sets.

## Making New Cards

To get started, install python.
Create a python environment and install the dependencies.

```
(env) zach $ python -m pip install -r requirements.txt
```

To generate cards, make a new card in `./cardModels`.
This script depends on the following subfolders, which you'll have to create:

* blanks: Contains card background blanks.
* cardArt: Contains card art.
* decks: Contains deck files.
* env: The python environment.
Lookup venv and modules.
* fonts: Contains fonts needed to make the cards.
* outputs: Contains output cards.
* preEvolutionArt: Contains art for the top-left corner of the cards.
* premade: Contains cards to be pasted into outputs verbatim.

Ping me for a zip file.

Once you've created and populated the above, you should be able to run `python generateCard.py` and take it from there!

## Creating a Deck

Use the TTS Deck Editor.
Upload only the cards that you want to update.
Save the deck file and export it as a png.
Import it in TTS using the Custom Deck Tool.
Make sure the card back shows properly in hands.

## Updating TTS

After importing, label the cards with the name of the Pokemon, Trainer, Energy, or what have you, by right clicking and updating the name.
Then, update the sets by removing the old pokemon and replacing them in the set.

To make sure generation works, follow these instructions:

1. Right click on an instance of a pack.
Set `enabled = false` and the `filterObjectEnter` function to `return true`.
1. Update the totals in the drop slots object to reflect the new totals of rare, uncommon, and common cards.
1. Make a new copy of the pack.
1. Make a new copy of the set deck.
1. Put the new deck of cards in.
1. Update the script to set `enabled = true` and the `filterObjectEnter` function to `return false`.
1. Make a new copy of the pack.
1. Reset the relevant infinite bag.
1. Drop in the pack.
1. Pull a set of 15 or so and test it out!

That should be everything you need to get started making custom cards!
