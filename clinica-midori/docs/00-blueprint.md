# 00 · Blueprint — decupado da referência

A referência chegou. Está em `01_REFERENCE/` com a análise completa em
`01_REFERENCE/ANALISE.md`. Este documento é o que foi importado dela pro corte.

---

## O que foi medido na referência

| | Referência | Corte v2 (medido no MP4 final) |
|---|---|---|
| planos / duração | 20 planos · 44,3s | 12 planos · 19,8s (limpo) · 21 planos · 39,0s (estrutura) |
| mediana de plano | **1,90s** | **1,65s** |
| plano mais curto | 0,47s | 0,60s |
| plano mais longo | 3,0s (fora os blocos de entrevista) | 3,0s |
| desvio das durações | ~0,67 (fora entrevista) | **0,74** |
| luma média | 0,430 | **0,415** |
| contraste (p95−p5) | 0,716 | **0,703** |
| saturação média | 0,235 | 0,286 |
| sombras R−B | −0,062 | **−0,063** |
| meios R−B | +0,039 | +0,084 |
| altas R−B | +0,055 | **+0,070** |
| pixels quase pretos | 5,0% | **5,3%** |

Os dois desvios que sobraram são decisões, não erro:

- **Saturação +0,05.** Você pediu imagem viva, não cinza. E o material tem uma
  parede verde e uma TV com cachoeira que a referência não tem. Se quiser
  fechar o número, é trocar `saturation=0.70` por `0.62` no `show_look`.
- **Meios +0,045 mais quentes.** A recepção é uma sala de tungstênio com
  ripado de madeira. Para levar o meio-tom dela até o número da referência eu
  precisaria de um ganho de azul tão forte que **o verde do logo da Midori
  vira azul** — testei e medi. Ficou num meio-termo: a recepção continua
  quente (como a referência deixa o exterior e a entrada dela), os
  consultórios ficam frios e limpos.

## A assinatura de cor: split tone

Sombra fria, meio-tom e alta quentes. É o que faz a referência parecer filme.
Contido, não é teal-and-orange.

```
por clipe (neutralização da dominante, resolvida por medição):
  colorchannelmixer=rr=…:gg=…:bb=…     ← um por sala, em timeline.json

look único por cima:
  eq=contrast=1.18:brightness=0.070:saturation=0.70:gamma=1.09
  curves=master='0/0.026 0.25/0.248 0.5/0.528 0.75/0.815 1/1'
  colorbalance=rs=-0.125:bs=0.145:rm=-0.05:bm=0.05:rh=0.025:bh=-0.025
  unsharp=5:5:0.30   vignette=PI/6.2
```

O `colorchannelmixer` de cada sala não foi escolhido no olho: é a solução
analítica que leva o meio-tom daquela sala ao alvo medido na referência,
preservando a luminância.

## O ritmo não é métrico

A referência tem plano de 0,47s e plano de 3,0s no mesmo filme. Corte sempre
na mesma duração é o que faz parecer template.

A v1 era metronômica: cinco planos seguidos de exatamente 1,8s. A v2 varia
`2,1 · 1,8 · 0,6 · 1,2 · 1,8 · 0,9 · 3,0 · 0,9 · 1,5 · 1,8 · 1,2 · 3,0`,
com desvio 0,74 contra 0,67 da referência.

A grade mudou de 0,6s para **0,3s** (meio tempo a 100 BPM). É o que permite
0,9s e 1,5s sem sair da batida.

## A entrevista é a espinha

A mudança estrutural mais importante. Na referência a entrevista **volta ~6
vezes** ao longo dos 44s, e todo o B-roll é cutaway por cima da fala.

A v1 tratava entrevista como um bloco único de 3,6s. A v2 tem **5 blocos**
(`P01`, `P02`, `P04`, `P05`, `P08`), cada um com um briefing próprio do que o
soundbite precisa cobrir. Isso é, na prática, o roteiro da diária de gravação.

## Transições

**Corte seco em tudo.** A referência não tem um dissolve sequer. Os dissolves
da v1 foram removidos — `"dissolves": false` no `timeline.json`.

## O que não dá pra importar

A referência foi gravada com câmera de verdade: profundidade de campo rasa,
luz controlada, gimbal. E principalmente: **tem gente** — um dentista falando,
paciente na cadeira, mãos trabalhando.

Isso é gravação, não montagem. O corte reproduz ritmo, estrutura e cor. O
resto depende do que for gravado, e é por isso que 9 dos 21 blocos são slot.

## Formato

A referência é **16:9 horizontal**. O material da Midori é **9:16 vertical**.
O corte ficou em 9:16 — recortar vertical pra 16:9 jogaria fora 3/4 do quadro,
e Reels/TikTok penalizam vídeo deitado. Foi importada a linguagem, não a
proporção.

## Estabilização: desligada, de propósito

O `vidstab` deste build deforma a imagem neste material — tenta remover o pan
intencional junto com o tremor e preenche a borda com conteúdo de frames
anteriores. O código continua lá (`build.py --estab`) pro dia em que chegar
material realmente trêmulo.

## Som

| Camada | Origem | Nível |
|---|---|---|
| Trilha | **scratch, sintetizada** — 100 BPM, 19 compassos, arranjo enxuto pra caber embaixo de voz em qualquer ponto | base |
| Ambiência | room tone **real** dos próprios clipes | −5 dB |
| Transições | 2 passagens de ruído (entrada do bloco clínico + assinatura) | discreto |
| Mix | loudnorm −14 LUFS · **medido −14,0** | padrão Reels |

A trilha continua não sendo a final — `docs/03-trilha.md`.
