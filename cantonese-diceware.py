#!/usr/bin/python

################################################################
# cantonese-diceware.py
# Modified: 20191101
################################################################
# Generates Diceware lists of pronounceable Cantonese syllables
# (including gibberish and pseudo-English).
# ----------------------------------------------------------------
# See also: Conway's Custom Romanisation for Cantonese
#   https://yawnoc.github.io/pages/conway-cantonese-romanisation.html
# ----------------------------------------------------------------
# Released into the public domain (CC0):
#   https://creativecommons.org/publicdomain/zero/1.0/
# ABSOLUTELY NO WARRANTY, i.e. "GOD SAVE YOU"
################################################################

import itertools
import re

################################################################
# List of dice rolls (7776)
################################################################

DICE_ROLLS = itertools.product('123456', repeat = 5)
DICE_ROLLS = ["".join(d) for d in DICE_ROLLS]

################################################################
# List of initials (24)
################################################################

# Here ? denotes the null initial.

# The pseudo-English initial "r" is included, and
# {ts vs ch}, {ts' vs ch'} and {s vs sh} are left unmerged,
# to boost the number of syllables.

INITIALS = ("""\
  ?
  p p' m f
  t t' n l
  k k' ng h kw k'w w
  ts ts' ch ch' s sh y
  r
  """
).split()

################################################################
# List of finals (60)
################################################################

# Here we use the ASCII substitutes
#   oe for œ (U+0153),
#   ue for ü (U+00FC).

# The pseudo-English finals "en", "et", "oen" and "oet" are included
# to boost the number of syllables.

FINALS = ("""\
  aa aai aau aam aan aang aap aat aak
  ai au am an ang ap at ak
  e ei eu em en eng ep et ek
  ee eeu eem een ing eep eet ik
  or oi ou orn ong ort ok
  oo ooi oon ung oot uk
  oe oen oeng oet oek
  _ue _n _t
  ue uen uet
  m ng
  """
).split()

################################################################
# List of pitches (6)
################################################################

# I only refer to pitches as tones after entering tones have been canonicalised
# as tones 7, 8 and 9.

PITCHES = map(str, range(1, 1 + 6))

################################################################
# List of non-Conway romanisation schemes
################################################################

ROMANISATIONS = [
  "conway",
  "jyutping"
]

NON_CONWAY_ROMANISATIONS = ROMANISATIONS[1:]

################################################################
# Dictionaries of romanisation conversion rules
################################################################

ROMANISATION_CONVERSIONS_DICTIONARY = {}

for romanisation in NON_CONWAY_ROMANISATIONS:
  
  ROMANISATION_CONVERSIONS_DICTIONARY[romanisation] = {}

# ----------------------------------------------------------------
# Initials
# ----------------------------------------------------------------

# NOTE: I have added zh, ch and sh to Jyutping for ch, ch' and sh.
ROMANISATION_CONVERSIONS_DICTIONARY["jyutping"]["initials"] = """\
  p b
  p' p
  t d
  t' t
  k g
  k' k
  kw gw
  k'w kw
  ts z
  ts' c
  ch zh
  ch' ch
  y j
  """

# ----------------------------------------------------------------
# Finals
# ----------------------------------------------------------------

ROMANISATION_CONVERSIONS_DICTIONARY["jyutping"]["finals"] = """\
  ee i
  eeu iu
  eem im
  een in
  eep ip
  eet it
  or o
  orn on
  ort ot
  oo u
  ooi ui
  oon un
  oot ut
  _ue eoi
  _n eon
  _t eot
  ue yu
  uen yun
  uet yut
  """

# ----------------------------------------------------------------
# Tones
# ----------------------------------------------------------------

# All non-Conway romanisations have 1, 3 and 6 for entering tones 7, 8 and 9

for romanisation in NON_CONWAY_ROMANISATIONS:
  
  ROMANISATION_CONVERSIONS_DICTIONARY[romanisation]["tones"] = """\
    7 1
    8 3
    9 6
  """

################################################################
# Convert romanisations
################################################################

def convert_romanisation(romanisation, syllables):
  
  for type in ROMANISATION_CONVERSIONS_DICTIONARY[romanisation]:
    
    rules = ROMANISATION_CONVERSIONS_DICTIONARY[romanisation][type]
    rules = rules.split()
    
    # Entries 0, 2, 4, etc. are patterns
    patts = rules[0::2]
    
    # Entries 1, 3, 5, etc. are replacements
    repls = rules[1::2]
    
    # Make patterns and replacements unambiguous (using | separator)
    if type == "initials":
      patts = ["^" + p + "[|]" for p in patts]
      repls = [r + "|" for r in repls]
    elif type == "finals":
      patts = ["[|]" + p for p in patts]
      repls = ["|" + r for r in repls]
    
    # Perform replacements
    for p, r in zip(patts, repls):
      syllables = regex_replace(p, r, syllables)
    
  return syllables

################################################################
# Remove a regular expression (i.e. replace with the empty string)
################################################################

def regex_remove(patt, string, count = 0):
  
  return regex_replace(patt, "", string, count = count)

################################################################
# Replace a regular expression
################################################################

def regex_replace(patt, repl, string, count = 0):
  
  return re.sub(patt, repl, string, count = count, flags = re.MULTILINE)

################################################################
# Main
################################################################

def main():
  
  # ----------------------------------------------------------------
  # Generate all syllables
  # ----------------------------------------------------------------
  
  # Take Cartesian product of the lists of initials, finals and pitches
  syllables = itertools.product(INITIALS, FINALS, PITCHES)
  # (8640 syllables)
  
  # Join each combination using | as the separator
  syllables = ["|".join(s) for s in syllables]
  
  # Put them into a newline-separated string
  syllables = "\n".join(syllables)
  
  # ----------------------------------------------------------------
  # Filter unpronounceable syllables
  # ----------------------------------------------------------------
  
  # Remove all syllables with
  # non-null initial (not ?) and pure nasal final (m or ng)
  syllables = regex_remove("^[^?|]+[|](?:m|ng)[|].$", syllables)
  # (8364 syllables)
  
  # Remove entering tones vernacularised as tone 5
  syllables = regex_remove("^.+[ptk][|]5$", syllables)
  # (7884 syllables)
  
  # ----------------------------------------------------------------
  # Reduce list down to 6 ** 5 == 7776 syllables
  # ----------------------------------------------------------------
  
  # Remove entering tones vernacularised as tone 4
  syllable_surplus = len(syllables.split()) - 6 ** 5
  syllables = regex_remove("^.+[ptk][|]4$", syllables, syllable_surplus)
  # (7776 syllables)
  
  # ----------------------------------------------------------------
  # Canonicalise non-vernacularised entering tones
  # ----------------------------------------------------------------
  
  syllables = regex_replace("([ptk][|])1", r"\g<1>7", syllables)
  syllables = regex_replace("([ptk][|])3", r"\g<1>8", syllables)
  syllables = regex_replace("([ptk][|])6", r"\g<1>9", syllables)
  
  # ----------------------------------------------------------------
  # Convert Conway's Custom Romanisation to other romanisations
  # ----------------------------------------------------------------
  
  syllables_dictionary = {}
  syllables_dictionary["conway"] = syllables
  
  for romanisation in NON_CONWAY_ROMANISATIONS:
    
    syllables_dictionary[romanisation] = (
      convert_romanisation(romanisation, syllables)
    )
  
  # ----------------------------------------------------------------
  # Make pretty and output to file
  # ----------------------------------------------------------------
  
  for romanisation in ROMANISATIONS:
    
    syllables = syllables_dictionary[romanisation]
    
    # Remove null initial markers ?
    syllables = regex_remove("[?]", syllables)
    
    # Remove separators |
    syllables = regex_remove("[|]", syllables)
    
    # Sort
    syllables = sorted(syllables.split())
    
    # Prefix with dice rolls
    syllables = ["{} {}".format(d, s) for d, s in zip(DICE_ROLLS, syllables)]
    
    # Put into a newline-separated string
    syllables = "\n".join(syllables)
    
    # Output
    output_file = open(
      "cantonese-diceware-{}.txt".format(romanisation),
      "w",
      encoding = "utf-8"
    )
    output_file.write(syllables)

if __name__ == "__main__":
  
  main()