#!/usr/bin/python

################################################################
# cantonese-diceware.py
# Modified: 20191101
################################################################
# Generates a Diceware list of pronounceable Cantonese syllables
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

PITCHES = map(str, range(1, 1 + 6))

################################################################
# Remove a regular expression (i.e. replace with the empty string)
################################################################

def regex_remove(pattern, string, count = 0):
  
  return regex_replace(pattern, "", string, count = count)

################################################################
# Replace a regular expression
################################################################

def regex_replace(pattern, repl, string, count = 0):
  
  return re.sub(pattern, repl, string, count = count, flags = re.MULTILINE)

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
  # Make pretty and output to file
  # ----------------------------------------------------------------
  
  # Remove null initial markers ?
  syllables = regex_remove("[?]", syllables)
  
  # Remove separators |
  syllables = regex_remove("[|]", syllables)
  
  # Sort
  syllables = sorted(syllables.split())
  
  # Prefix with dice rolls
  dice_rolls = itertools.product('123456', repeat = 5)
  dice_rolls = ["".join(d) for d in dice_rolls]
  syllables = ["{} {}".format(d, s) for d, s in zip(dice_rolls, syllables)]
  
  # Put into a newline-separated string
  syllables = "\n".join(syllables)
  
  # Output
  output_file = open("cantonese-diceware.txt", "w", encoding = "utf-8")
  output_file.write(syllables)

if __name__ == "__main__":
  
  main()