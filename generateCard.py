import json
from typing import Any, List, Tuple
from PIL import Image, ImageDraw, ImageFont
import os
import shutil

# ===========================
# COLORS
# ===========================
black = (0, 0, 0, 255)
white = (255, 255, 255, 255)
red = (255, 0, 0, 255)

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
symbolsDict = {}
symbolWidth = 25
y0 = 12
y1 = 72
y2 = 87
y3 = 147

# top row of symbols.png
with Image.open(symbolsFilepath) as symbols:
    symbolsDict["grass"]     = symbols.crop((85,  y0, 147, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["fire"]      = symbols.crop((159, y0, 221, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["water"]     = symbols.crop((233, y0, 295, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["lightning"] = symbols.crop((307, y0, 369, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["electric"]  = symbols.crop((307, y0, 369, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["psychic"]   = symbols.crop((381, y0, 443, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["fighting"]  = symbols.crop((455, y0, 517, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["dark"]      = symbols.crop((529, y0, 591, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["darkness"]  = symbols.crop((529, y0, 591, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["metal"]     = symbols.crop((603, y0, 665, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["steel"]     = symbols.crop((603, y0, 665, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["fairy"]     = symbols.crop((677, y0, 739, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["dragon"]    = symbols.crop((751, y0, 813, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["colorless"] = symbols.crop((825, y0, 887, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["normal"]    = symbols.crop((825, y0, 887, y1)).resize((symbolWidth, symbolWidth), Image.BICUBIC)

    # bottom row of symbols.png
    symbolsDict["poison"]  = symbols.crop((195, y2, 257, y3)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["flying"]  = symbols.crop((269, y2, 331, y3)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["bug"]     = symbols.crop((343, y2, 405, y3)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["ground"]  = symbols.crop((417, y2, 479, y3)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["rock"]    = symbols.crop((491, y2, 553, y3)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["ice"]     = symbols.crop((565, y2, 627, y3)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["ghost"]   = symbols.crop((639, y2, 701, y3)).resize((symbolWidth, symbolWidth), Image.BICUBIC)
    symbolsDict["dragon2"] = symbols.crop((713, y2, 775, y3)).resize((symbolWidth, symbolWidth), Image.BICUBIC)

with Image.open(emptyFilepath) as empty:
    symbolsDict["empty"] = empty.resize((symbolWidth, symbolWidth), Image.BICUBIC)

# ===========================
# FONTS
# ===========================
# thank you https://www.deviantart.com/icycatelf/art/Neo-Font-Guide-for-GIMP-Users-390305613
pokemonNameFont = ImageFont.truetype("fonts/gill-cb.ttf", 25)
pokemonNameEvolutionFont = ImageFont.truetype("fonts/gill-cb.ttf", 40)
hpFont = ImageFont.truetype("fonts/Futura LT Condensed Bold.ttf", 18)
evolvesFromFont = ImageFont.truetype("fonts/gill-rbi.TTF", 12)
abilityNameFont = ImageFont.truetype("fonts/gill-cb.ttf", 20)
abilityEffectFont = ImageFont.truetype("fonts/gill-rp.TTF", 16) # Not sure about this
damageFont = ImageFont.truetype("fonts/gill-rp.TTF", 40) # Not sure about this
attackNameEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 20)
attackNameNoEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 20) # Only size will change
attackEffectFont = ImageFont.truetype("fonts/gill-rp.ttf", 16)
weaknessResistanceFont = ImageFont.truetype("fonts/gill-cb.ttf", 12)
pokedexFont = ImageFont.truetype("fonts/gill-rbi.ttf", 10)

trainerTitleFont = ImageFont.truetype("timesbd.ttf", 30)

mediumAttackNameEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 18)
mediumAttackNameNoEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 18)
mediumAttackEffectFont = ImageFont.truetype("fonts/gill-rp.ttf", 16)
mediumAbilityNameFont = ImageFont.truetype("fonts/gill-cb.ttf", 16)
mediumAbilityEffectFont = ImageFont.truetype("fonts/gill-rp.TTF", 14)

smallAttackNameEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 14)
smallAttackNameNoEffectFont = ImageFont.truetype("fonts/gill-cb.ttf", 14)
smallAttackEffectFont = ImageFont.truetype("fonts/gill-rp.ttf", 12)
smallAbilityNameFont = ImageFont.truetype("fonts/gill-cb.ttf", 14)
smallAbilityEffectFont = ImageFont.truetype("fonts/gill-rp.TTF", 12)

# ===========================
# SIZES
# ===========================
cardWidth = 471
cardHeight = 659
artWidth = (int) (cardWidth * 0.8)
artHeight = (int) (cardWidth * 0.6)
trainerArtWidth = (int) (cardWidth * 0.85)
trainerArtHeight = (int) (cardWidth * 0.5)

absoluteTextBoxTop = 370
absoluteTextBoxBottom = 540
attackOffset = 80
abilityOffset = 60

# ===========================
# FUNCTIONS
# ===========================

# Helper function I used to generate symbolsDict
def dissect_symbols():
    with Image.open(symbolsFilepath) as symbols:
        dissect = ImageDraw.Draw(symbols, "RGBA")
        for x in range(85, 1000, 74):
            dissect.text((x, 0), str(x), fill=white)
            dissect.rectangle((x, 12, x+1, 72), fill=white)
            dissect.text((x + 40, 0), str(x + 62), fill=white)
            dissect.rectangle((x+62, 12, x+63, 72), fill=white)
        dissect.text((0, 12), str(12), fill=white)
        dissect.rectangle((0, 12, 1000, 13), fill=white)
        dissect.text((0, 72), str(72), fill=white)
        dissect.rectangle((0, 72, 1000, 73), fill=white)
    
        for x in range(195, 1000, 74):
            dissect.text((x, 75), str(x), fill=white)
            dissect.rectangle((x, 87, x+1, 147), fill=white)
            dissect.text((x + 40, 75), str(x + 62), fill=white)
            dissect.rectangle((x+62, 87, x+63, 147), fill=white)
        dissect.text((0, 87), str(87), fill=white)
        dissect.rectangle((0, 87, 1000, 88), fill=white)
        dissect.text((0, 147), str(147), fill=white)
        dissect.rectangle((0, 147, 1000, 148), fill=white)
    
        symbols.save("dissected.png")

def draw_title_and_description(
    draw: ImageDraw.Draw,
    title: str,
    titleFont: ImageFont.FreeTypeFont,
    description: str,
    descriptionFont: ImageFont.FreeTypeFont,
    location: Tuple[int, int],
    limit: Tuple[int, int],
    color: Tuple[int, int, int, int],
    titleFill: Tuple[int, int, int, int],
    smallTitleFont: ImageFont.FreeTypeFont,
    smallDescriptionFont: ImageFont.FreeTypeFont,
    mediumTitleFont: ImageFont.FreeTypeFont,
    mediumDescriptionFont: ImageFont.FreeTypeFont,
    ):

    x_limit = limit[0]
    y_limit = limit[1]

    titleOffset = titleFont.getsize(title)[0]
    wrappedText = get_wrapped_text(description, descriptionFont, x_limit, titleOffset + location[0])
    firstLine = wrappedText[0]
    lines = "\n".join(wrappedText[1:])

    projected_absolute_y_end = (descriptionFont.getsize(lines)[1] + location[1]) 
    about_midway = ((y_limit - location[1]) / 2) + location[1]

    if projected_absolute_y_end + 50 > y_limit: # shrink it tiny
        titleOffset = smallTitleFont.getsize(title)[0]
        wrappedText = get_wrapped_text(description, smallDescriptionFont, x_limit, titleOffset + location[0])
        firstLine = wrappedText[0]
        lines = "\n".join(wrappedText[1:])

        draw.text(location, title, font=smallTitleFont, fill=titleFill)
        draw.text((location[0] + 13 + titleOffset, location[1] + 4), firstLine, font=smallDescriptionFont, fill=color, spacing=-1)
        draw.text((location[0], location[1] + 15), lines, font=smallDescriptionFont, fill=color, spacing=-1)

    elif projected_absolute_y_end + 70 > y_limit: # shrink it medium
        titleOffset = mediumTitleFont.getsize(title)[0]
        wrappedText = get_wrapped_text(description, mediumDescriptionFont, x_limit, titleOffset + location[0])
        firstLine = wrappedText[0]
        lines = "\n".join(wrappedText[1:])

        draw.text(location, title, font=mediumTitleFont, fill=titleFill)
        draw.text((location[0] + 13 + titleOffset, location[1] + 4), firstLine, font=mediumDescriptionFont, fill=color, spacing=-1)
        draw.text((location[0], location[1] + 15), lines, font=mediumDescriptionFont, fill=color, spacing=-1)
    
    elif projected_absolute_y_end < about_midway:
        draw.text((location[0], about_midway - 10), title, font=titleFont, fill=titleFill)
        draw.text((location[0] + 13 + titleOffset, about_midway - 6), firstLine, font=descriptionFont, fill=color)
        draw.text((location[0], about_midway + 10), lines, font=descriptionFont, fill=color)

    else:
        draw.text(location, title, font=titleFont, fill=titleFill)
        draw.text((location[0] + 23 + titleOffset, location[1] + 4), firstLine, font=descriptionFont, fill=color)
        draw.text((location[0], location[1] + 20), lines, font=descriptionFont, fill=color)

def draw_retreat_symbols(card: Image.Image, retreat_cost: int, location: tuple([int])):
    symbol = symbolsDict["colorless"]
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

# Adapted from https://stackoverflow.com/questions/8257147/wrap-text-in-pil
def get_wrapped_text(text: str, font: ImageFont.ImageFont,
                     line_length: int, prefix: int = 0):
        lines = ['']
        for word in text.split():
            line = f'{lines[-1]} {word}'.strip()
            limit = line_length
            if (len(lines) == 1):
                limit -= prefix
            if font.getsize(line)[0] <= limit:
                lines[-1] = line
            else:
                lines.append(word)
        return lines

def draw_ability_box(draw, ability, textBoxTop, textBoxBottom, color):
    draw_title_and_description(
        draw,
        "Ability: " + ability["name"].title().strip(),
        abilityNameFont,
        ability["effect"].strip(),
        abilityEffectFont,
        (60, textBoxTop),
        (cardWidth - 100, textBoxBottom),
        color,
        red,
        smallAbilityNameFont,
        smallAbilityEffectFont,
        mediumAbilityNameFont,
        mediumAbilityEffectFont,
    )

def draw_attack_box(card, draw, attack, textBoxTop, textBoxBottom, color):
    center_y = int((textBoxTop + textBoxBottom) / 2)

    if "effect" in attack:
        draw_title_and_description(
            draw,
            attack["name"],
            attackNameEffectFont,
            attack["effect"],
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
        draw.text((cardWidth / 2, center_y), attack["name"], font=attackNameNoEffectFont, fill=color, anchor="mm")

    if "cost" in attack:
        cost = attack["cost"]
        icons = cost.split()
        symbol_center = center_y - 12

        num_icons = len(icons)
        symbols = [symbolsDict[icon] for icon in icons]
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

    if "damage" in attack:
        draw.text((390, center_y), str(attack["damage"]), font=damageFont, fill=color, anchor="lm")

def draw_boxes(card, draw, cardData, color):
    count = 0
    if "ability" in cardData:
        count += 1
    if "attacks" in cardData:
        count += len(cardData["attacks"])

    if count == 0:
        print("No abilities or attacks found. Do you have a typo?")
    elif count == 1:
        if "ability" in cardData:
            draw_ability_box(draw, cardData["ability"], absoluteTextBoxTop, absoluteTextBoxBottom, color)
        else:
            draw_attack_box(card, draw, cardData["attacks"][0], absoluteTextBoxTop, absoluteTextBoxBottom, color)
    elif count < 5 and count >= 2:
        textBoxTop = absoluteTextBoxTop
        interval = (absoluteTextBoxBottom - absoluteTextBoxTop) / count
        textBoxBottom = interval + absoluteTextBoxTop
        attack_index = 0

        if "ability" in cardData:
            draw_ability_box(draw, cardData["ability"], textBoxTop, textBoxBottom, color)
            draw.rectangle((60, textBoxBottom, 380, textBoxBottom + 1), fill=color)
            textBoxTop += interval
            textBoxBottom += interval
        
        while textBoxBottom <= absoluteTextBoxBottom:
            if not attack_index == 0:
                draw.rectangle((60, textBoxTop, 380, textBoxTop + 1), fill=color)
            draw_attack_box(card, draw, cardData["attacks"][attack_index], textBoxTop, textBoxBottom, color)
            attack_index += 1
            textBoxTop += interval
            textBoxBottom += interval
    else: 
        print("Currently up to 4 attacks or 3 attacks with 1 ability are supported.")

def draw_card(cardType, cardData):
    color = black
    if (cardType == "trainer"):
        trainerType = cardType + cardData["type"].strip() + ".png"
        cardBackgroundFilepath = os.path.join(blanksDirectory, trainerType)
        cardArtFilepath = os.path.join(cardArtDirectory, cardData["image"].lower().strip() + ".png")

        newCard = Image.new('RGBA', (cardWidth, cardHeight))

        with Image.open(cardBackgroundFilepath) as cardBackground:
            resizedBackground = cardBackground.resize((cardWidth, cardHeight), Image.BICUBIC)
            with Image.open(cardArtFilepath) as cardArt:
                resizedCardArt = cardArt.resize((trainerArtWidth, trainerArtHeight), Image.BICUBIC)
                newCard.paste(resizedCardArt, (40, 150))
                newCard.paste(resizedBackground, (0, 0), resizedBackground)
            
                draw = ImageDraw.Draw(newCard)

                description = get_wrapped_text(cardData["effect"], attackEffectFont, 375)
                draw.text((50, 110), cardData["name"], font=trainerTitleFont, fill=black)
                draw.text((50, 420), "\n".join(description), font=attackEffectFont, fill=black)

                print("\tGenerating " + cardData["name"] + " as " + cardData["type"] + " " + cardType)
                outputFilename = os.path.join(outputDirectory, cardData["name"])
                newCard.save(outputFilename + ".png", "png")

                return
    
    if (cardType == "dark" or cardType == "ghost"):
        color = white

    # calculate filenames
    cardStageAndType = cardType + cardData["stage"].lower().strip() + ".png"
    cardBackgroundFilepath = os.path.join(blanksDirectory, cardStageAndType)
    cardArtFilepath = os.path.join(cardArtDirectory, cardData["image"].lower().strip() + ".png")

    newCard = Image.new('RGBA', (cardWidth, cardHeight))
    
    with Image.open(cardBackgroundFilepath) as cardBackground:
        resizedBackground = cardBackground.resize((cardWidth, cardHeight), Image.BICUBIC)
        with Image.open(cardArtFilepath) as cardArt:
            resizedCardArt = cardArt.resize((artWidth, artHeight), Image.BICUBIC)
            newCard.paste(resizedCardArt, (45, 80))
            newCard.paste(resizedBackground, (0, 0), resizedBackground)
            if "evolvesFromImage" in cardData:
                preEvolutionFilepath = os.path.join(preEvolutionDirectory, cardData["evolvesFromImage"] + ".png")

                with Image.open(preEvolutionFilepath) as preEvolution:
                    resizedPreEvolution = preEvolution.resize((50, 50), Image.BICUBIC)
                    newCard.paste(resizedPreEvolution, (26, 45), resizedPreEvolution)
            draw = ImageDraw.Draw(newCard)

            # =============================================
            # TEXT
            # =============================================
            name_offset = 50
            if "evolvesFrom" in cardData:
                draw.text((100, 30), "Evolves from " + cardData["evolvesFrom"], font=evolvesFromFont, fill=color)
                name_offset += 60

            draw.text((name_offset, 45), cardData["name"].strip(), font=pokemonNameFont, fill=color)
            draw.text((350, 45), str(cardData["hp"]) + " HP", font=hpFont, fill=color)

            draw_boxes(newCard, draw, cardData, color)

            # =============================================
            # WEAKNESS, RESISTANCE, RETREAT, AND FLAVOR
            # =============================================
            # TODO: Handle unique generation for fairy stage 1 and 2, including drawing correct symbol over
            if cardData["type"].lower() == "fairy" and cardData["stage"].lower().startswith("stage"):
                fairy = symbolsDict["fairy"].resize((40, 40), Image.BICUBIC)
                newCard.paste(fairy, (405, 25), fairy)

                if "weakness" in cardData:
                    weakness = symbolsDict[cardData["weakness"]["type"].lower().strip()]
                    weaknessAmount = str(cardData["weakness"]["value"])
                    newCard.paste(weakness, (85, 565), weakness)
                    draw.text((65, 570), "+" + weaknessAmount, font=weaknessResistanceFont, fill=color)

                if "resistance" in cardData:
                    resistance = symbolsDict[cardData["resistance"]["type"].lower().strip()]
                    resistanceAmount = str(cardData["resistance"]["value"])
                    newCard.paste(resistance, (180, 565), resistance)
                    draw.text((160, 570), "-" + resistanceAmount, font=weaknessResistanceFont, fill=color)

                draw_retreat_symbols(newCard, cardData["retreat"], (134, 595))

                description = get_wrapped_text(cardData["flavor"], pokedexFont, 175)
                draw.text((242, 560), "\n".join(description), font=pokedexFont, fill=color)

            else:
                if "weakness" in cardData:
                    weakness = symbolsDict[cardData["weakness"]["type"].lower().strip()]
                    weaknessAmount = str(cardData["weakness"]["value"])
                    newCard.paste(weakness, (60, 555), weakness)
                    draw.text((87, 560), "+" + weaknessAmount, font=weaknessResistanceFont, fill=color)

                if "resistance" in cardData:
                    resistance = symbolsDict[cardData["resistance"]["type"].lower().strip()]
                    resistanceAmount = str(cardData["resistance"]["value"])
                    newCard.paste(resistance, (215, 555), resistance)
                    draw.text((242, 560), "-" + resistanceAmount, font=weaknessResistanceFont, fill=color)

                draw_retreat_symbols(newCard, cardData["retreat"], (375, 555))

                description = get_wrapped_text(cardData["flavor"], pokedexFont, 375)
                draw.text((45, 590), "\n".join(description), font=pokedexFont, fill=color)

    print("\tGenerating " + cardData["name"] + " as " + cardData["stage"] + " " + cardType)
    outputFilename = os.path.join(outputDirectory, cardData["name"])

    if os.path.exists(outputFilename + ".png"):
        i = 1
        while os.path.exists(outputFilename + str(i) + ".png"):
            i += 1
        outputFilename += str(i)

    print("\tSaving to " + outputFilename)
    newCard.save(outputFilename + ".png", "png")

# ===========================
# MAIN
# ===========================
if os.path.exists(outputDirectory):
    shutil.rmtree(outputDirectory)
os.mkdir(outputDirectory)

for _, _, premadeFilenames in os.walk(premadeDirectory):
    for premadeFilename in premadeFilenames:
        premadeFilepath = os.path.join(premadeDirectory, premadeFilename)
        print("Copying " + premadeFilepath + " to outputs")
        shutil.copy(premadeFilepath, outputDirectory)

for _, subdirectories, _ in os.walk(cardModelsDirectory):
    for subdirectory in subdirectories:
        print("Generating cards in " + subdirectory + " subdirectory")
        for _, _, pokemonFilenames in os.walk(os.path.join(cardModelsDirectory, subdirectory)):
            for pokemonFilename in pokemonFilenames:
                pokemonFilepath = os.path.join(cardModelsDirectory, subdirectory, pokemonFilename)
                pokemonFile = open(pokemonFilepath)
                pokemonData = json.load(pokemonFile)
                try:
                    draw_card(subdirectory, pokemonData)
                except:
                    print("Could not print " + pokemonFilepath + ", skipping")