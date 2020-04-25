[中文](README.ch.md)

# Cantonese Diceware

Lists of `6 ** 5 == 7776` pronounceable syllables in Cantonese,
including gibberish and pseudo-English, to be used for building passphrases.

Roll your own physical dice to get
`5 * log(6) / log(2) == 12.9` bits of entropy per word.
See Arnold G. Reinhold's [Diceware page][d] and [FAQ][df] for details.

## Syllables

To boost the number of syllables to the required quantity, I have:

1. Added the pseudo-English initial [r],
2. Not merged {[ts] vs [tɕ]}, {[tsʰ] vs [tɕʰ]} and {[s] vs [ɕ]},
   and
3. Added the pseudo-English finals [ɛːn], [ɛːt̚], [œːn] and [œːt̚].

I have only included entering tones (入聲) in their literary pitches
(7, 8 and 9 or 1, 3 and 6) and vernacularised as tone 2 (陰上) and tone 4 (陽平).
No word of entering tone is included as tone 5 (陽上).

## Romanisations

The list of syllables is first generated in
[Conway's Custom Romanisation for Cantonese][ccr]
before being converted to other romanisation schemes.

The round-bracketed entries below do not exist
in the corresponding romanisations, and have been added to account for
the unmerged pairs {[ts] vs [tɕ]}, {[tsʰ] vs [tɕʰ]} and {[s] vs [ɕ]}:

| Romanisation | [ts] | [tɕ] | [tsʰ] | [tɕʰ] | [s] | [ɕ] |
| --- | --- | --- | --- | --- | --- | --- |
| [Conway][ccr] ([list][lc]) | ts | ch | ts' | ch' | s | sh |
| [Jyutping][jtp] ([list][lj]) | z | (zh) | c | (ch) | s | (sh) |
| [Sidney Lau][sl] ([list][ls]) | j | (jh) | ch | (chh) | s | (sh) |

The following are pseudo-English sounds:

| Romanisation | [r] | [ɛːn] | [ɛːt̚] | [œːn] | [œːt̚]
| --- | --- | --- | --- | --- | --- |
| [Conway][ccr] ([list][lc]) | r | en | et | oen | oet |
| [Jyutping][jtp] ([list][lj]) | r | en | et | oen | oet |
| [Sidney Lau][sl] ([list][ls]) | r | en | et | eun | eut |

[ccr]: https://yawnoc.github.io/cantonese/conway-romanisation
[d]: http://world.std.com/~reinhold/diceware.html
[df]: http://world.std.com/%7Ereinhold/dicewarefaq.html
[jtp]: https://www.lshk.org/jyutping
[sl]: http://sidneylau.com/
[lc]: cantonese-diceware-conway.txt
[lj]: cantonese-diceware-jyutping.txt
[ls]: cantonese-diceware-sidney_lau.txt
