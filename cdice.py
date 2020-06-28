#!/usr/bin/env python3

"""
----------------------------------------------------------------
cdice.py
----------------------------------------------------------------
Generates Diceware lists of pronounceable Cantonese syllables
(including gibberish and pseudo-English).
----------------------------------------------------------------
See also: Conway's Custom Romanisation for Cantonese
  <https://yawnoc.github.io/cantonese/conway-romanisation>
----------------------------------------------------------------
Released into the public domain (CC0):
  <https://creativecommons.org/publicdomain/zero/1.0/>
ABSOLUTELY NO WARRANTY, i.e. "GOD SAVE YOU"
"""


import itertools
import re


# List of dice rolls (7776)

DICE_ROLLS = itertools.product('123456', repeat=5)
DICE_ROLLS = ["".join(d) for d in DICE_ROLLS]


# List of initials (24) in Conway's Custom Romanisation

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
)


# List of finals (60) in Conway's Custom Romanisation

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
)


# List of pitches (6)

# I only refer to pitches as tones after entering tones have been canonicalised
# as tones 7, 8 and 9.

PITCHES = " ".join(map(str, range(1, 1 + 6)))


# List of all and non-Conway romanisation schemes

ROMANISATIONS = [
  "conway",
  "jyutping",
  "sidney_lau"
]

NON_CONWAY_ROMANISATIONS = ROMANISATIONS[1:]


# Dictionaries of romanisation conversion rules...

ROMANISATION_CONVERSIONS_DICTIONARY = {}

for romanisation in NON_CONWAY_ROMANISATIONS:
  ROMANISATION_CONVERSIONS_DICTIONARY[romanisation] = {}

# ...for initials

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

# NOTE: I have added jh, chh and sh to Sidney Lau for ch, ch' and sh.
# The replacement ch -> jh must be performed before ts' -> ch.
ROMANISATION_CONVERSIONS_DICTIONARY["sidney_lau"]["initials"] = """\
  p b
  p' p
  t d
  t' t
  k g
  k' k
  kw gw
  k'w kw
  ch jh
  ch' chh
  ts j
  ts' ch
  """
  
# ...for finals

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

ROMANISATION_CONVERSIONS_DICTIONARY["sidney_lau"]["finals"] = """\
  aa a
  ee i
  eeu iu
  eem im
  een in
  eep ip
  eet it
  or oh
  ou o
  orn on
  ort ot
  oe euh
  oen eun
  oeng eung
  oet eut
  oek euk
  _ue ui
  _n un
  _t ut
  """
  
# ...for tones

# All non-Conway romanisations have 1, 3 and 6 for entering tones 7, 8 and 9

for romanisation in NON_CONWAY_ROMANISATIONS:
  
  ROMANISATION_CONVERSIONS_DICTIONARY[romanisation]["tones"] = """\
    7 1
    8 3
    9 6
  """


def convert_romanisation(romanisation, syllables):
  """
  Convert syllables in Conway romanisation to romanisation.
  """
  
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
      patts = ["[|]" + p + "[|]" for p in patts]
      repls = ["|" + r + "|" for r in repls]
    
    # Perform replacements
    for p, r in zip(patts, repls):
      syllables = regex_replace(p, r, syllables)
    
  return syllables



def regex_remove(patt, string, count=0):
  """
  Replace a regex pattern with the empty string.
  """
  
  return regex_replace(patt, "", string, count=count)



def regex_replace(patt, repl, string, count=0):
  """
  Replace a regex pattern with a replacement (multiline mode).
  """
  
  return re.sub(patt, repl, string, count=count, flags=re.MULTILINE)



def main():
  
  # ----------------------------------------------------------------
  # Generate all syllables in Conway's Custom Romanisation
  # ----------------------------------------------------------------
  
  # Take Cartesian product of the lists of initials, finals and pitches
  conway_syllables = itertools.product(
    *[component.split() for component in [INITIALS, FINALS, PITCHES]]
  )
  # (8640 syllables)
  
  # Join each combination using | as the separator
  conway_syllables = ["|".join(s) for s in conway_syllables]
  
  # Put them into a newline-separated string
  conway_syllables = "\n".join(conway_syllables)
  
  # ----------------------------------------------------------------
  # Filter unpronounceable syllables
  # ----------------------------------------------------------------
  
  # Remove all syllables with
  # non-null initial (not ?) and pure nasal final (m or ng)
  conway_syllables = regex_remove("^[^?|]+[|](?:m|ng)[|].$", conway_syllables)
  # (8364 syllables)
  
  # Remove entering tones vernacularised as tone 5
  conway_syllables = regex_remove("^.+[ptk][|]5$", conway_syllables)
  # (7884 syllables)
  
  # ----------------------------------------------------------------
  # Reduce list down to 6 ** 5 == 7776 syllables
  # ----------------------------------------------------------------
  
  # Remove entering tones vernacularised as tone 4
  syllable_surplus = len(conway_syllables.split()) - 6 ** 5
  conway_syllables = regex_remove("^.+[ptk][|]4$", conway_syllables, syllable_surplus)
  # (7776 syllables)
  
  # ----------------------------------------------------------------
  # Canonicalise non-vernacularised entering tones
  # ----------------------------------------------------------------
  
  conway_syllables = regex_replace("([ptk][|])1", r"\g<1>7", conway_syllables)
  conway_syllables = regex_replace("([ptk][|])3", r"\g<1>8", conway_syllables)
  conway_syllables = regex_replace("([ptk][|])6", r"\g<1>9", conway_syllables)
  
  # ----------------------------------------------------------------
  # Convert Conway's Custom Romanisation to other romanisations
  # ----------------------------------------------------------------
  
  syllables_dictionary = {}
  syllables_dictionary["conway"] = conway_syllables
  
  for romanisation in NON_CONWAY_ROMANISATIONS:
    
    syllables_dictionary[romanisation] = (
      convert_romanisation(romanisation, conway_syllables)
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
    syllables = "\n".join(syllables) + "\n"
    
    # Output
    with open(
      "cantonese-diceware-{}.txt".format(romanisation),
      "w",
      encoding="utf-8"
    ) as output_file:
      output_file.write(syllables)

if __name__ == "__main__":
  
  main()
