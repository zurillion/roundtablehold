#!/usr/bin/env python3
"""
Update ashesofwar.yaml: replace English ash-of-war names in data_it link text
with Italian names.  The URLs are preserved unchanged.
"""
import re

# English name in link text  →  Italian name
NAME_MAP = {
    # Heavy
    "Stamp (Upward Cut)":        "Pestata (Taglio Ascendente)",
    "Stamp (Sweep)":             "Pestata (Spazzata)",
    "Wild Strikes":              "Colpi Selvaggi",
    "Lion's Claw":               "Artiglio del Leone",
    "Cragblade":                 "Lama Rupestre",
    "Kick":                      "Calcio",
    "Endure":                    "Resistere",
    "Ground Slam":               "Colpo a Terra",
    "Earthshaker":               "Tremuoto",
    "Hoarah Loux's Earthshaker": "Pestone di Hoarah Loux",
    "War Cry":                   "Grido di Guerra",
    "Barbaric Roar":             "Ruggito Barbarico",
    "Braggart's Roar":           "Ruggito dello Spaccone",
    "Troll's Roar":              "Ruggito del Troll",
    "Spinning Gravity Thrust":   "Affondo Gravitazionale Rotante",
    "Savage Lion's Claw":        "Zampa di Leone Selvaggio",
    # Keen
    "Spinning Slash":            "Taglio Rotante",
    "Impaling Thrust":           "Impalamento",
    "Piercing Fang":             "Zanna Perforante",
    "Repeating Thrust":          "Affondo Ripetuto",
    "Double Slash":              "Doppio Fendente",
    "Sword Dance":               "Danza della Spada",
    "Unsheathe":                 "Sfoderamento",
    "Quickstep":                 "Passo Rapido",
    "Bloodhound's Step":         "Passo del Segugio Sanguinario",
    "Raptor of the Mist":        "Rapace della Nebbia",
    "Beast's Roar":              "Ruggito della Bestia",
    "Piercing Throw":            "Lancio Perforante",
    "Scattershot Throw":         "Lancio a Dispersione",
    "Raging Beast":              "Bestia Infuriata",
    "Savage Claws":              "Artigli Feroci",
    "Blind Spot":                "Punto Cieco",
    "Swift Slash":               "Taglio Rapido",
    "Overhead Stance":           "Postura in Alto",
    # Quality
    "Square Off":                "Fronteggiamento",
    "Charge Forth":              "Carica Avanti",
    "Spinning Strikes":          "Colpi Rotanti",
    "Giant Hunt":                "Caccia ai Giganti",
    "Storm Blade":               "Lama Tempestosa",
    "Storm Assault":             "Assalto Tempestoso",
    "Stormcaller":               "Evocatempesta",
    "Storm Stomp":               "Pestone Tempesta",
    "Vacuum Slice":              "Taglio nel Vuoto",
    "Phantom Slash":             "Fendente Fantasma",
    "Determination":             "Determinazione",
    "Royal Knight's Resolve":    "Risolutezza del Cavaliere Reale",
    "Wing Stance":               "Postura con le Ali",
    # Magic
    "Glintstone Pebble":         "Ciottolo di Gemmarilucente",
    "Glintblade Phalanx":        "Falange di Lame Splendenti",
    "Carian Greatsword":         "Grande Spada Splendente di Carian",
    "Carian Grandeur":           "Magnificenza Cariana",
    "Spinning Weapon":           "Arma Rotante",
    "Loretta's Slash":           "Fendente di Loretta",
    "Waves of Darkness":         "Onde di Oscurità",
    "Gravitas":                  "Gravitas",
    "Carian Sovereignty":        "Sovranità Cariana",
    # Fire
    "Flaming Strike":            "Colpo Infuocato",
    "Flame of the Redmanes":     "Fiamma dei Criniere Rosse",
    "Eruption":                  "Eruzione",
    # Flame
    "Prelate's Charge":          "Carica del Prelato",
    "Black Flame Tornado":       "Tornado di Nera Fiamma",
    "Flame Skewer":              "Spiedo di Fiamma",
    "Flame Spear":               "Lancia di Fiamma",
    # Lightning
    "Thunderbolt":               "Fulmine",
    "Lightning Slash":           "Taglio del Fulmine",
    "Lightning Ram":             "Ariete Fulminante",
    "Blinkbolt":                 "Baleno",
    # Sacred
    "Sacred Blade":              "Lama Sacra",
    "Prayerful Strike":          "Colpo della Preghiera",
    "Sacred Ring of Light":      "Anello Sacro di Luce",
    "Sacred Order":              "Ordine Sacro",
    "Shared Order":              "Ordine Condiviso",
    "Golden Land":               "Terra d'Oro",
    "Golden Slam":               "Colpo d'Oro",
    "Golden Vow":                "Voto d'Oro",
    "Vow of the Indomitable":    "Voto dell'Indomabile",
    "Holy Ground":               "Terra Sacra",
    "Aspects of the Crucible: Wings": "Aspetti del Crogiolo: Ali",
    # Poison
    "Poisonous Mist":            "Nebbia Velenosa",
    "Poison Moth Flight":        "Volo della Falena Velenosa",
    "The Poison Flower Blooms Twice": "Il Fiore Velenoso Sboccia Due Volte",
    # Blood
    "Blood Blade":               "Lama del Sangue",
    "Bloody Slash":              "Fendente Sanguinario",
    "Blood Tax":                 "Tributo di Sangue",
    "Seppuku":                   "Seppuku",
    # Cold
    "Ice Spear":                 "Lancia di Ghiaccio",
    "Chilling Mist":             "Nebbia Glaciale",
    "Hoarfrost Stomp":           "Pestone Brinoso",
    "Divine Beast Frost Stomp":  "Pestone della Bestia Divina",
    "Ghostflame Call":           "Richiamo della Fiamma Spettrale",
    # Occult
    "Spectral Lance":            "Lancia Spettrale",
    "Lifesteal Fist":            "Pugno Rubavita",
    "White Shadow's Lure":       "Esca dell'Ombra Bianca",
    "Assassin's Gambit":         "Stratagemma dell'Assassino",
    "Shriek of Sorrow":          "Grido del Dolore",
    # Standard
    "Mighty Shot":               "Tiro Potente",
    "Through and Through":       "Da Parte a Parte",
    "Barrage":                   "Raffica",
    "Sky Shot":                  "Tiro Celeste",
    "Enchanted Shot":            "Tiro Incantato",
    "Rain of Arrows":            "Pioggia di Frecce",
    "Parry":                     "Parata",
    "Golden Parry":              "Parata d'Oro",
    "Storm Wall":                "Muro Tempestoso",
    "Shield Bash":               "Colpo di Scudo",
    "Shield Crash":              "Carica con lo Scudo",
    "Barricade Shield":          "Scudo di Barricata",
    "Thops's Barrier":           "Barriera di Thops",
    "Carian Retaliation":        "Rappresaglia Cariana",
    "No Skill":                  "Senzanome",
    "Dryleaf Whirlwind":         "Vortice delle Foglie Secche",
    "Palm Blast":                "Esplosione del Palmo",
    "Wall of Sparks":            "Muro di Scintille",
    "Rolling Sparks":            "Scintille Rotanti",
    "Igon's Drake Hunt":         "Caccia alla Draka di Igon",
    "Shield Strike":             "Colpo dello Scudo",
    # Misc (plain text, no link)
    "Lost Ashes of War":         "Ceneri di Guerra Perdute",
}

filepath = 'data/checklists/ashesofwar.yaml'

with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

replaced = 0
output = []
for line in lines:
    if 'data_it:' not in line:
        output.append(line)
        continue
    new_line = line
    for en, it in NAME_MAP.items():
        # Replace in link text:  >English Name</a>  →  >Italian Name</a>
        old = f'>{en}</a>'
        new = f'>{it}</a>'
        if old in new_line:
            new_line = new_line.replace(old, new)
            replaced += 1
        # Also handle plain-text names (Misc section, no link tag)
        # Only replace if it appears as the first quoted string in the array
        plain_old = f'["{en}"'
        plain_new = f'["{it}"'
        if plain_old in new_line:
            new_line = new_line.replace(plain_old, plain_new)
            replaced += 1
    output.append(new_line)

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(output)

print(f"Done. Replaced {replaced} name occurrences across {len(lines)} lines.")

# Verify: count data_it lines still containing English-only names
remaining = 0
for en in NAME_MAP:
    for line in output:
        if 'data_it:' in line and f'>{en}</a>' in line:
            print(f"  STILL ENGLISH: {en}")
            remaining += 1
print(f"Remaining untranslated: {remaining}")
