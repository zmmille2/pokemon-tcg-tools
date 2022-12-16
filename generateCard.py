import argparse
import json
from typing import Dict, Literal
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

from cardData import (
    TM,
    Ability,
    AbilityType,
    Active,
    Attack,
    Bug,
    CardData,
    Dark,
    Dragon,
    Electric,
    Fairy,
    Fighting,
    Fire,
    Flying,
    Ghost,
    Grass,
    Ground,
    Ice,
    Normal,
    Passive,
    Poison,
    PokemonCardData,
    PokemonType,
    Psychic,
    Rock,
    Stadium,
    Stage1,
    Stage2,
    Steel,
    Supporter,
    TrainerCardData,
    Unique,
    Water,
    WeakRes,
    PokemonData,
)

# ===========================
# COLORS
# ===========================
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
red = (255, 0, 0, 255)
green = (0, 255, 0, 255)
blue = (0, 0, 255, 255)

# ===========================
# DIRECTORIES
# ===========================
blanksDirectory = "blanks"
cardModelsDirectory = "cardModels"
cardArtDirectory = "cardArt"
fontsDirectory = "fonts"
outputDirectory = "outputs"
premadeDirectory = "premade"
preEvolutionDirectory = "preEvolutionArt"

# ===========================
# SYMBOLS
# ===========================
emptyFilepath = "empty.png"
symbolsFilepath = "symbols.png"
symbolsDict: Dict[PokemonType, Image.Image] = {}
symbolWidth = 25
y0 = 12
y1 = 72
y2 = 87
y3 = 147


# top row of symbols.png
with Image.open(symbolsFilepath) as symbols:
    symbolsDict["grass"] = symbols.crop((85, y0, 147, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict["fire"] = symbols.crop((159, y0, 221, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict["water"] = symbols.crop((233, y0, 295, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict["electric"] = symbols.crop((307, y0, 369, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict["psychic"] = symbols.crop((381, y0, 443, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict["fighting"] = symbols.crop((455, y0, 517, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict["dark"] = symbols.crop((529, y0, 591, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict["steel"] = symbols.crop((603, y0, 665, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict["fairy"] = symbols.crop((677, y0, 739, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict[Dragon] = symbols.crop((751, y0, 813, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict[Normal] = symbols.crop((825, y0, 887, y1)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )

    # bottom row of symbols.png
    symbolsDict[Poison] = symbols.crop((195, y2, 257, y3)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict[Flying] = symbols.crop((269, y2, 331, y3)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict[Bug] = symbols.crop((343, y2, 405, y3)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict[Ground] = symbols.crop((417, y2, 479, y3)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict[Rock] = symbols.crop((491, y2, 553, y3)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict[Ice] = symbols.crop((565, y2, 627, y3)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    symbolsDict[Ghost] = symbols.crop((639, y2, 701, y3)).resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )
    # symbolsDict["dragon2"] = symbols.crop((713, y2, 775, y3)).resize(
    #     (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    # )

with Image.open(emptyFilepath) as empty:
    symbolsDict[None] = empty.resize(
        (symbolWidth, symbolWidth), Image.Resampling.BICUBIC
    )

# ===========================
# FONTS
# ===========================
# thank you https://www.deviantart.com/icycatelf/art/Neo-Font-Guide-for-GIMP-Users-390305613
pokemonNameFont = ImageFont.truetype("fonts/gill-cb.ttf", 25)
pokemonNameEvolutionFont = ImageFont.truetype("fonts/gill-cb.ttf", 40)
hpFont = ImageFont.truetype("fonts/Futura LT Condensed Bold.ttf", 18)
evolvesFromFont = ImageFont.truetype("fonts/gill-rbi.TTF", 12)
passiveNameFont = ImageFont.truetype("fonts/gill-cb.ttf", 20)
passiveEffectFont = ImageFont.truetype("fonts/gill-rp.TTF", 16)  # Not sure about this
damageFont = ImageFont.truetype("fonts/gill-rp.TTF", 40)  # Not sure about this
attackNameEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 20)
attackNameNoEffectFont = ImageFont.truetype(
    "fonts/gill-cb.ttf", 20
)  # Only size will change
attackEffectFont = ImageFont.truetype("fonts/gill-rp.TTF", 16)
weaknessResistanceFont = ImageFont.truetype("fonts/gill-cb.ttf", 12)
pokedexFont = ImageFont.truetype("fonts/gill-rbi.TTF", 10)

trainerTitleFont = (
    ImageFont.truetype("fonts/timesbd.ttf", 30)
    if os.path.exists("fonts/timesbd.ttf")
    else ImageFont.truetype("timesbd.ttf", 30)
)

mediumAttackNameEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 18)
mediumAttackNameNoEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 18)
mediumAttackEffectFont = ImageFont.truetype("fonts/gill-rp.TTF", 16)
mediumPassiveNameFont = ImageFont.truetype("fonts/gill-cb.ttf", 16)
mediumPassiveEffectFont = ImageFont.truetype("fonts/gill-rp.TTF", 14)

smallAttackNameEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 14)
smallAttackNameNoEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 14)
smallAttackEffectFont = ImageFont.truetype("fonts/gill-rp.TTF", 12)
smallPassiveNameFont = ImageFont.truetype("fonts/gill-cb.ttf", 14)
smallPassiveEffectFont = ImageFont.truetype("fonts/gill-rp.TTF", 12)

# ===========================
# SIZES
# ===========================
cardWidth = 471
cardHeight = 659
artWidth = (int)(cardWidth * 0.8)
artHeight = (int)(cardWidth * 0.6)
trainerArtWidth = (int)(cardWidth * 0.85)
trainerArtHeight = (int)(cardWidth * 0.5)

absoluteTextBoxTop = 370
absoluteTextBoxBottom = 540
attackOffset = 80
passiveOffset = 60

# ===========================
# FUNCTIONS
# ===========================

# Helper function I used to generate symbolsDict
def dissect_symbols():
    with Image.open(symbolsFilepath) as symbols:
        dissect = ImageDraw.Draw(symbols, "RGBA")
        for x in range(85, 1000, 74):
            dissect.text((x, 0), str(x), fill=white)
            dissect.rectangle((x, 12, x + 1, 72), fill=white)
            dissect.text((x + 40, 0), str(x + 62), fill=white)
            dissect.rectangle((x + 62, 12, x + 63, 72), fill=white)
        dissect.text((0, 12), str(12), fill=white)
        dissect.rectangle((0, 12, 1000, 13), fill=white)
        dissect.text((0, 72), str(72), fill=white)
        dissect.rectangle((0, 72, 1000, 73), fill=white)

        for x in range(195, 1000, 74):
            dissect.text((x, 75), str(x), fill=white)
            dissect.rectangle((x, 87, x + 1, 147), fill=white)
            dissect.text((x + 40, 75), str(x + 62), fill=white)
            dissect.rectangle((x + 62, 87, x + 63, 147), fill=white)
        dissect.text((0, 87), str(87), fill=white)
        dissect.rectangle((0, 87, 1000, 88), fill=white)
        dissect.text((0, 147), str(147), fill=white)
        dissect.rectangle((0, 147, 1000, 148), fill=white)

        symbols.save("dissected.png")


def draw_title_and_description(
    draw: ImageDraw.ImageDraw,
    title: str,
    titleFont: ImageFont.FreeTypeFont,
    description: str,
    descriptionFont: ImageFont.FreeTypeFont,
    location: tuple[int, int],
    limit: tuple[int, int],
    color: tuple[int, int, int, int],
    titleFill: tuple[int, int, int, int],
    smallTitleFont: ImageFont.FreeTypeFont,
    smallDescriptionFont: ImageFont.FreeTypeFont,
    mediumTitleFont: ImageFont.FreeTypeFont,
    mediumDescriptionFont: ImageFont.FreeTypeFont,
):

    x_limit = limit[0]
    y_limit = limit[1]

    titleOffset = titleFont.getwidth(title)
    wrappedText = get_wrapped_text(
        description, descriptionFont, x_limit, titleOffset + location[0]
    )
    firstLine = wrappedText[0]
    lines = "\n".join(wrappedText[1:])

    projected_absolute_y_end = descriptionFont.getheight(lines) + location[1]
    about_midway = ((y_limit - location[1]) / 2) + location[1]

    if projected_absolute_y_end + 50 > y_limit:  # shrink it tiny
        titleOffset = smallTitleFont.getwidth(title)
        wrappedText = get_wrapped_text(
            description, smallDescriptionFont, x_limit, titleOffset + location[0]
        )
        firstLine = wrappedText[0]
        lines = "\n".join(wrappedText[1:])

        draw.text(location, title, font=smallTitleFont, fill=titleFill)
        draw.text(
            (location[0] + 13 + titleOffset, location[1] + 4),
            firstLine,
            font=smallDescriptionFont,
            fill=color,
            spacing=-1,
        )
        draw.text(
            (location[0], location[1] + 15),
            lines,
            font=smallDescriptionFont,
            fill=color,
            spacing=-1,
        )

    elif projected_absolute_y_end + 70 > y_limit:  # shrink it medium
        titleOffset = mediumTitleFont.getwidth(title)
        wrappedText = get_wrapped_text(
            description, mediumDescriptionFont, x_limit, titleOffset + location[0]
        )
        firstLine = wrappedText[0]
        lines = "\n".join(wrappedText[1:])

        draw.text(location, title, font=mediumTitleFont, fill=titleFill)
        draw.text(
            (location[0] + 13 + titleOffset, location[1] + 4),
            firstLine,
            font=mediumDescriptionFont,
            fill=color,
            spacing=-1,
        )
        draw.text(
            (location[0], location[1] + 15),
            lines,
            font=mediumDescriptionFont,
            fill=color,
            spacing=-1,
        )

    elif projected_absolute_y_end < about_midway:
        draw.text(
            (location[0], about_midway - 10), title, font=titleFont, fill=titleFill
        )
        draw.text(
            (location[0] + 13 + titleOffset, about_midway - 6),
            firstLine,
            font=descriptionFont,
            fill=color,
        )
        draw.text(
            (location[0], about_midway + 10), lines, font=descriptionFont, fill=color
        )

    else:
        draw.text(location, title, font=titleFont, fill=titleFill)
        draw.text(
            (location[0] + 23 + titleOffset, location[1] + 4),
            firstLine,
            font=descriptionFont,
            fill=color,
        )
        draw.text(
            (location[0], location[1] + 20), lines, font=descriptionFont, fill=color
        )


def draw_retreat_symbols(
    card: Image.Image, retreat_cost: int, location: tuple[int, int]
):
    symbol = symbolsDict[Normal]
    y = location[1]
    if retreat_cost == 1 or retreat_cost == 3 or retreat_cost == 5:
        card.paste(symbol, location, symbol)
    if retreat_cost == 2 or retreat_cost == 4:
        card.paste(symbol, (location[0] - 15, y), symbol)
        card.paste(symbol, (location[0] + 15, y), symbol)
    if retreat_cost == 3 or retreat_cost == 5:
        card.paste(symbol, (location[0] - 30, y), symbol)
        card.paste(symbol, (location[0] + 30, y), symbol)
    if retreat_cost == 4:
        card.paste(symbol, (location[0] - 45, y), symbol)
        card.paste(symbol, (location[0] + 45, y), symbol)
    if retreat_cost == 5:
        card.paste(symbol, (location[0] - 60, y), symbol)
        card.paste(symbol, (location[0] + 60, y), symbol)


def getwidth(self: ImageFont.ImageFont, line: str) -> int:
    left, _, right, _ = self.getbbox(line)
    return right - left


def getheight(self: ImageFont.ImageFont, line: str) -> int:
    _, top, _, bottom = self.getbbox(line)
    return top - bottom


# Adapted from https://stackoverflow.com/questions/8257147/wrap-text-in-pil
def get_wrapped_text(
    text: str, font: ImageFont.ImageFont, line_length: int, prefix: int = 0
):
    lines = [""]
    for word in text.split():
        line = f"{lines[-1]} {word}".strip()
        limit = line_length
        if len(lines) == 1:
            limit -= prefix
        if font.getwidth(line) <= limit:
            lines[-1] = line
        else:
            lines.append(word)
    return lines


def draw_passive_box(
    draw: ImageDraw.ImageDraw,
    passive: AbilityType,
    textBoxTop: int,
    textBoxBottom: int,
    color: tuple[int, int, int, int],
):
    if passive.type == Passive:  # No restrictions
        passive_color = blue
        prefix = "Passive Ability: "
    elif passive.type == Unique:  # Unique to this pokemon
        passive_color = green
        prefix = "Unique Ability: "
    elif passive.type == Active:  # Unique to this pokemon while Active
        passive_color = red
        prefix = "Active Ability: "
    else:
        raise Exception(f"I don't know what a {passive.type} passive is")

    draw_title_and_description(
        draw,
        prefix + passive.name,
        passiveNameFont,
        passive.effect,
        passiveEffectFont,
        (60, textBoxTop),
        (cardWidth - 100, textBoxBottom),
        color,
        passive_color,
        smallPassiveNameFont,
        smallPassiveEffectFont,
        mediumPassiveNameFont,
        mediumPassiveEffectFont,
    )


mask = Image.new("L", (symbolWidth, 1), color=0xFF)
for x in range(symbolWidth):
    if x <= 11:
        mask.putpixel((x, 0), 0)
    if x < 13 and x > 11:
        mask.putpixel((x, 0), 128)
    if x >= 13:
        mask.putpixel((x, 0), 255)

gradient = mask.resize((symbolWidth, symbolWidth)).rotate(-45)


def generate_symbol(icon: PokemonType | tuple[PokemonType, PokemonType]) -> Image.Image:
    if type(icon) is PokemonType:
        return symbolsDict[icon]
    elif type(icon) is tuple[PokemonType, PokemonType]:
        first, second = icon
        first_symbol = symbolsDict[first].copy()
        second_symbol = symbolsDict[second]

        first_symbol.paste(second_symbol, None, gradient)

        return first_symbol

    else:
        raise Exception(f"I don't know what a {icon} icon is.")


def draw_attack_box(
    card: Image.Image,
    draw: ImageDraw.ImageDraw,
    attack: Attack,
    textBoxTop: int,
    textBoxBottom: int,
    color: tuple[int, int, int, int],
):
    center_y = int((textBoxTop + textBoxBottom) / 2)

    if attack.effect is not None:
        draw_title_and_description(
            draw,
            attack.name,
            attackNameEffectFont,
            attack.effect,
            attackEffectFont,
            (80, textBoxTop),
            (cardWidth - 160, textBoxBottom),
            color,
            color,
            smallAttackNameEffectFont,
            smallAttackEffectFont,
            mediumAttackNameEffectFont,
            mediumAttackEffectFont,
        )
    else:
        draw.text(
            (cardWidth / 2, center_y),
            attack.name,
            font=attackNameNoEffectFont,
            fill=color,
            anchor="mm",
        )

    if attack.cost is not None:
        icons = attack.cost.split()
        symbol_center = center_y - 12

        num_icons = len(icons)

        symbols = [generate_symbol(icon) for icon in icons]

        if num_icons == 1:
            card.paste(symbols[0], (40, symbol_center), symbols[0])
        if num_icons == 2:
            card.paste(symbols[0], (25, symbol_center), symbols[0])
            card.paste(symbols[1], (55, symbol_center), symbols[1])
        if num_icons == 3:
            card.paste(symbols[0], (25, symbol_center - 11), symbols[0])
            card.paste(symbols[1], (55, symbol_center - 11), symbols[1])
            card.paste(symbols[2], (40, symbol_center + 11), symbols[2])
        if num_icons == 4:
            card.paste(symbols[0], (25, symbol_center - 15), symbols[0])
            card.paste(symbols[1], (55, symbol_center - 15), symbols[1])
            card.paste(symbols[2], (25, symbol_center + 15), symbols[2])
            card.paste(symbols[3], (55, symbol_center + 15), symbols[3])
        if num_icons == 5:
            card.paste(symbols[0], (25, symbol_center - 20), symbols[0])
            card.paste(symbols[1], (55, symbol_center - 20), symbols[1])
            card.paste(symbols[2], (40, symbol_center), symbols[2])
            card.paste(symbols[3], (25, symbol_center + 20), symbols[3])
            card.paste(symbols[4], (55, symbol_center + 20), symbols[4])

    if attack.damage is not None:
        draw.text(
            (390, center_y),
            attack.damage,
            font=damageFont,
            fill=color,
            anchor="lm",
        )


def draw_boxes(
    card: Image.Image,
    draw: ImageDraw.ImageDraw,
    cardData: CardData,
    color: tuple[int, int, int, int],
):
    count = 0
    if cardData.passive is not None:
        count += 1
    if cardData.attacks is not None:
        count += len(cardData.attacks)

    if count == 0:
        print("No abilities or attacks found. Do you have a typo?")
    elif count == 1:
        if cardData.passive is not None:
            draw_passive_box(
                draw,
                cardData.passive,
                absoluteTextBoxTop,
                absoluteTextBoxBottom,
                color,
            )
        else:
            draw_attack_box(
                card,
                draw,
                cardData.attacks[0],
                absoluteTextBoxTop,
                absoluteTextBoxBottom,
                color,
            )
    elif count < 5 and count >= 2:
        textBoxTop = absoluteTextBoxTop
        interval = (absoluteTextBoxBottom - absoluteTextBoxTop) / count
        textBoxBottom = interval + absoluteTextBoxTop
        attack_index = 0

        if cardData.passive is not None:
            draw_passive_box(draw, cardData.passive, textBoxTop, textBoxBottom, color)
            draw.rectangle((60, textBoxBottom, 380, textBoxBottom + 1), fill=color)
            textBoxTop += interval
            textBoxBottom += interval

        while textBoxBottom <= absoluteTextBoxBottom:
            if not attack_index == 0:
                draw.rectangle((60, textBoxTop, 380, textBoxTop + 1), fill=color)
            draw_attack_box(
                card,
                draw,
                cardData.attacks[attack_index],
                textBoxTop,
                textBoxBottom,
                color,
            )
            attack_index += 1
            textBoxTop += interval
            textBoxBottom += interval
    else:
        print("Currently up to 4 attacks or 3 attacks with 1 passive are supported.")


def draw_trainer(cardData: TrainerCardData):
    trainerType = "trainer" + cardData.type.strip()
    cardBackgroundFilepath = os.path.join(blanksDirectory, trainerType + ".png")
    cardArtFilepath = os.path.join(cardArtDirectory, cardData.image + ".png")

    newCard = Image.new("RGBA", (cardWidth, cardHeight))

    with Image.open(cardBackgroundFilepath) as cardBackground:
        resizedBackground = cardBackground.resize(
            (cardWidth, cardHeight), Image.Resampling.BICUBIC
        )
        with Image.open(cardArtFilepath) as cardArt:
            resizedCardArt = cardArt.resize(
                (trainerArtWidth, trainerArtHeight), Image.Resampling.BICUBIC
            )
            newCard.paste(resizedCardArt, (40, 150))
            newCard.paste(resizedBackground, (0, 0), resizedBackground)

            draw = ImageDraw.Draw(newCard)
            draw.text((50, 110), cardData.name, font=trainerTitleFont, fill=black)

            if cardData.type is TM:
                draw_boxes(newCard, draw, cardData, black)
            else:
                description = get_wrapped_text(cardData.effect, attackEffectFont, 375)
                if cardData.type in [Supporter, Stadium]:
                    draw.text(
                        (50, 470),
                        "\n".join(description),
                        font=attackEffectFont,
                        fill=black,
                    )
                else:
                    draw.text(
                        (50, 420),
                        "\n".join(description),
                        font=attackEffectFont,
                        fill=black,
                    )

            print(
                "\tGenerating "
                + cardData.name
                + " as "
                + cardData.type
                + " "
                + "trainer"
            )
            outputFilename = os.path.join(outputDirectory, cardData.name)
            newCard.save(outputFilename + ".png", "png")


def draw_pokemon(cardData: PokemonCardData, filename: str):
    color = black if cardData.type is Dark or cardData.type is Ghost else white

    # calculate filenames
    cardStageAndType = cardData.type + cardData.stage + ".png"
    cardBackgroundFilepath = os.path.join(blanksDirectory, cardStageAndType)
    cardArtFilepath = os.path.join(cardArtDirectory, cardData.image + ".png")

    newCard = Image.new("RGBA", (cardWidth, cardHeight))

    with Image.open(cardBackgroundFilepath) as cardBackground:
        resizedBackground = cardBackground.resize(
            (cardWidth, cardHeight), Image.Resampling.BICUBIC
        )
        with Image.open(cardArtFilepath) as cardArt:
            resizedCardArt = cardArt.resize(
                (artWidth, artHeight), Image.Resampling.BICUBIC
            )
            newCard.paste(resizedCardArt, (45, 80))
            newCard.paste(resizedBackground, (0, 0), resizedBackground)
            if cardData.evolvesFrom is not None:
                preEvolutionFilepath = os.path.join(
                    preEvolutionDirectory,
                    cardData.evolvesFrom.replace(" ", "-") + ".png",
                )

                with Image.open(preEvolutionFilepath) as preEvolution:
                    resizedPreEvolution = preEvolution.resize(
                        (50, 50), Image.Resampling.BICUBIC
                    )
                    newCard.paste(resizedPreEvolution, (26, 45), resizedPreEvolution)
            draw = ImageDraw.Draw(newCard)

            # =============================================
            # TEXT
            # =============================================
            name_offset = 50
            if cardData.evolvesFrom is not None:
                draw.text(
                    (100, 30),
                    "Evolves from " + " ".join(cardData.evolvesFrom.split("-")).title(),
                    font=evolvesFromFont,
                    fill=color,
                )
                name_offset += 60

            draw.text(
                (name_offset, 45),
                cardData.name,
                font=pokemonNameFont,
                fill=color,
            )
            hp = str(cardData.hp)
            if cardData.hp < 100:
                draw.text((350, 45), hp + " HP", font=hpFont, fill=color)
            else:
                draw.text((335, 45), hp + " HP", font=hpFont, fill=color)

            draw_boxes(newCard, draw, cardData, color)

            # =============================================
            # WEAKNESS, RESISTANCE, RETREAT, AND FLAVOR
            # =============================================
            if cardData.type == Fairy and cardData.stage in [Stage1, Stage2]:
                fairy = symbolsDict[Fairy].resize((40, 40), Image.Resampling.BICUBIC)
                newCard.paste(fairy, (405, 25), fairy)

                if cardData.weakness is not None:
                    weakness = generate_symbol(cardData.weakness.type)
                    newCard.paste(weakness, (85, 565), weakness)
                    # TODO: Support for Union Types
                    draw.text(
                        (65, 570),
                        "+" + str(cardData.weakness.value),
                        font=weaknessResistanceFont,
                        fill=color,
                    )

                if cardData.resistance is not None:
                    resistance = generate_symbol(cardData.resistance.type)
                    newCard.paste(resistance, (180, 565), resistance)
                    # TODO: Support for Union Types
                    draw.text(
                        (160, 570),
                        "-" + str(cardData.resistance.value),
                        font=weaknessResistanceFont,
                        fill=color,
                    )

                draw_retreat_symbols(newCard, cardData.retreat, (134, 595))

                description = get_wrapped_text(cardData.flavor, pokedexFont, 175)
                draw.text(
                    (242, 560), "\n".join(description), font=pokedexFont, fill=color
                )
            else:
                if cardData.type == Flying:
                    flying = symbolsDict[Flying].resize(
                        (35, 35), Image.Resampling.BICUBIC
                    )
                    newCard.paste(flying, (388, 33), flying)

                if cardData.weakness is not None:
                    weakness = generate_symbol(cardData.weakness.type)
                    newCard.paste(weakness, (60, 555), weakness)
                    # TODO: Support for Union Types
                    draw.text(
                        (87, 560),
                        "+" + str(cardData.weakness.value),
                        font=weaknessResistanceFont,
                        fill=color,
                    )

                if cardData.resistance is not None:
                    resistance = generate_symbol(cardData.resistance.type)
                    newCard.paste(resistance, (215, 555), resistance)
                    # TODO: Support for Union Types
                    draw.text(
                        (242, 560),
                        "-" + str(cardData.resistance.value),
                        font=weaknessResistanceFont,
                        fill=color,
                    )

                draw_retreat_symbols(newCard, cardData.retreat, (375, 555))

                description = get_wrapped_text(cardData.flavor, pokedexFont, 375)
                draw.text(
                    (45, 590), "\n".join(description), font=pokedexFont, fill=color
                )

    print(
        "\tGenerating " + cardData.name + " as " + cardData.stage + " " + cardData.type
    )
    outputFilename = os.path.join(outputDirectory, filename)

    if os.path.exists(outputFilename):
        print(f"WARNING: Overwriting {outputFilename}")

    print("\tSaving to " + outputFilename)
    newCard.save(outputFilename, "png")


def draw_card(cardData: CardData, filename: str):
    if type(cardData) is TrainerCardData:
        draw_trainer(cardData)
        return
    elif type(cardData) is PokemonCardData:
        draw_pokemon(cardData, filename)


def shouldRecreate(
    pokemonFilepath: str, outputFilepath: str, cardArtFilename: str
) -> bool:
    if not os.path.exists(outputFilepath):
        print(
            f"Creating new card {pokemonFilepath} at {outputFilepath} because it does not exist yet."
        )
        return True
    elif os.path.getmtime("./generateCard.py") > os.path.getmtime(outputFilepath):
        print(
            f"Creating {pokemonFilepath} at {outputFilepath} because generateCard.py is newer."
        )
        return True
    elif os.path.getmtime(cardArtFilename) > os.path.getmtime(outputFilepath):
        print(
            f"Creating {pokemonFilepath} at {outputFilepath} because there is new card art."
        )
        return True
    elif os.path.getmtime(pokemonFilepath) > os.path.getmtime(outputFilepath):
        print(
            f"Creating {pokemonFilepath} at {outputFilepath} because the model was updated/created."
        )
        return True

    print(
        f"Skipping {pokemonFilepath} due to collision with preexisting {outputFilepath}"
    )
    return False


def copyPremadeCards(recopyIsForced: bool):
    for _, _, premadeFilenames in os.walk(premadeDirectory):
        for premadeFilename in premadeFilenames:
            premadeFilepath = os.path.join(premadeDirectory, premadeFilename)
            outputFilepath = os.path.join(outputDirectory, premadeFilename)
            shouldCopy = False
            if recopyIsForced or not os.path.exists(outputFilepath):
                shouldCopy = True
            elif os.path.getmtime("./generateCard.py") > os.path.getmtime(
                outputFilepath
            ):
                print(
                    f"Copying {premadeFilepath} to {outputDirectory} because generateCard.py is newer than {outputFilepath}."
                )
                shouldCopy = True

            if shouldCopy:
                shutil.copy(premadeFilepath, outputDirectory)


def parseObjectDictToCard(jsondict: dict) -> PokemonData:
    print(jsondict)
    if "type" not in jsondict.keys():
        # TODO: Fix type parsing here
        return Attack(**jsondict)
    elif "value" in jsondict.keys():
        return WeakRes(**jsondict)
    elif "hp" in jsondict.keys():
        return PokemonCardData(**jsondict)
    elif "image" in jsondict.keys():
        return TrainerCardData(**jsondict)
    else:
        # TODO: Fix ability parsing here
        return Ability(**jsondict)


def createNewCards(recreateIsForced: bool):
    for _, subdirectories, _ in os.walk(cardModelsDirectory):
        for subdirectory in subdirectories:
            print("Generating cards in " + subdirectory + " subdirectory")
            for _, _, pokemonFilenames in os.walk(
                os.path.join(cardModelsDirectory, subdirectory)
            ):
                for pokemonFilename in pokemonFilenames:
                    pokemonFilepath = os.path.join(
                        cardModelsDirectory, subdirectory, pokemonFilename
                    )
                    pokemonFile = open(pokemonFilepath)
                    pokemonData: CardData = json.load(
                        pokemonFile, object_hook=parseObjectDictToCard
                    )
                    try:
                        outputFilename = pokemonFilename.replace(".json", ".png")

                        outputFilepath = os.path.join(outputDirectory, outputFilename)
                        cardArtFilename = os.path.join(
                            cardArtDirectory, f"{pokemonData.image}.png"
                        )

                        if recreateIsForced or shouldRecreate(
                            pokemonFilepath, outputFilepath, cardArtFilename
                        ):
                            draw_card(pokemonData, outputFilename)
                    except Exception as e:
                        print(e)
                        print(f"Could not create {pokemonFilepath}, skipping")


# ===========================
# MAIN
# ===========================
def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-a",
        "--all",
        help="Should cards all be force refreshed? Defaults to false.",
        action="store_true",
    )

    parser.add_argument(
        "-n",
        "--new",
        help="Should new cards be force refreshed? Defaults to false.",
        action="store_true",
    )

    parser.add_argument(
        "-p",
        "--premade",
        help="Should premade cards be force refreshed? Defaults to false.",
        action="store_true",
    )

    arguments = parser.parse_args()
    if not os.path.exists(outputDirectory):
        os.mkdir(outputDirectory)

    if arguments.all:
        print(f"Recreating all files.")

    # copyPremadeCards(arguments.all or arguments.premade)
    createNewCards(arguments.all or arguments.new)


if __name__ == "__main__":
    main()
