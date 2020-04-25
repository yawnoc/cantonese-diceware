[English](README.md)

# 粵音 Diceware

表者，為可誦粵音 `6 ** 5 == 7776` 個，含無字及仿英之音，以作密碼一句。

自行擲骰仔者，每字得熵 `5 * log(6) / log(2) == 12.9` 位元。詳見 Arnold G. Reinhold [Diceware 一頁][d] 與 [FAQ][df]。

## 音

務音之夠數，則以

1. 添仿英聲母 [r]，
2. 不併 {[ts] 與 [tɕ]}、{[tsʰ] 與 [tɕʰ]}、{[s] 與 [ɕ]}，
3. 添仿英韻母 [ɛːn]、[ɛːt̚]、[œːn]、[œːt̚]。

入聲字，只收其文讀之調（即七、八、九，一曰一、三、六）及其語讀為陰上（第二）、陽平（第四）者，並不收其讀作陽上（第五）之音。

## 拼

音表先以 [Conway 拼][ccr] 產生，然後再轉為他拼。

下列受括者，乃係各拼不收之音也，添之以承 {[ts] 與 [tɕ]}、{[tsʰ] 與 [tɕʰ]}、{[s] 與 [ɕ]} 之不併耳：

| 拼 | [ts] | [tɕ] | [tsʰ] | [tɕʰ] | [s] | [ɕ] |
| --- | --- | --- | --- | --- | --- | --- |
| [Conway][ccr]（[表][lc]） | ts | ch | ts' | ch' | s | sh |
| [粵拼][jtp]（[表][lj]） | z | (zh) | c | (ch) | s | (sh) |
| [劉錫祥][sl]（[表][ls]） | j | (jh) | ch | (chh) | s | (sh) |

下列為仿英音：

| 拼 | [r] | [ɛːn] | [ɛːt̚] | [œːn] | [œːt̚]
| --- | --- | --- | --- | --- | --- |
| [Conway][ccr]（[表][lc]） | r | en | et | oen | oet |
| [粵拼][jtp]（[表][lj]） | r | en | et | oen | oet |
| [劉錫祥][sl]（[表][ls]） | r | en | et | eun | eut |

[ccr]: https://yawnoc.github.io/cantonese/conway-romanisation
[d]: http://world.std.com/~reinhold/diceware.html
[df]: http://world.std.com/%7Ereinhold/dicewarefaq.html
[jtp]: https://www.lshk.org/jyutping
[sl]: http://sidneylau.com/
[lc]: cantonese-diceware-conway.txt
[lj]: cantonese-diceware-jyutping.txt
[ls]: cantonese-diceware-sidney_lau.txt
