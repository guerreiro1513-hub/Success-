# GUERREIRO'S GRILL — anúncio do PACU (20,4 s)

`entrega/guerreiros-PACU-20s.mp4` — 1080×1920 · 9:16 (SAR 1:1) · H.264 · 30 fps · AAC · 20,40 s · 21 MB

Exportado a 8,2 Mbps (CRF 22, preset slow). O primeiro export saiu com 32 MB e
estourava o limite de 30 MB do envio; o Instagram recomprime de qualquer forma.

## O material e a decisão central
Os três vídeos são a **mesma cena à noite**, sob luz amarela forte. As **duas fotos**
são de longe o melhor material: nítidas, o peixe glaceado, luz neutra, 1450×2576
(exatamente 9:16, escala sem corte).

Então: **as fotos carregam o gancho, a revelação e o tamanho**; os vídeos carregam o
movimento, a faca e a cena de gente servindo — que é o que vende "serve até 8".

| Fonte | Papel | Planos |
|---|---|---|
| FOTO A | macro do gancho (curiosidade) | 2 |
| FOTO B | revelação, tamanho, fecho | 3 |
| P1 / P2 / P3 | servir, cortar, gente em volta | 11 |
| Florais (F1/F3/F4) | o churrasco de sempre | 6 |

## Correção de cor — o problema mais sério
A luz de sódio da noite deixou os vídeos com **R/B de 2,90 a 3,46**. As fotos estão
em 1,52–1,59. Sem corrigir, o peixe fica amarelo doentio e o corte não fecha com o
material do churrasco.

Levantei muito o azul e puxei o vermelho:

| | antes | depois |
|---|---|---|
| P1 | 3,46 | **2,15** |
| P2 | 2,90 | **1,80** |
| P3 | 3,34 | **2,02** |
| fotos | 1,52–1,59 | 1,67–1,88 |
| Florais | — | 1,75 |

O vídeo inteiro agora fecha na mesma faixa.

## Estrutura (22 planos, tudo na grade de 100 BPM)
| Tempo | Bloco | Texto |
|---|---|---|
| 0,0–2,1 | macro na pele marcada — não dá pra saber o que é | **TEM NOVIDADE** |
| 2,1–5,1 | revelação do peixe inteiro | **AGORA TEM / PACU** |
| 5,1–8,1 | montagem: faca, servir, textura | — |
| 8,1–11,1 | o peixe com a galera em volta | **AOS SÁBADOS / E DOMINGOS** |
| 11,1–13,5 | peixe inteiro, plano aberto | **SERVE ATÉ / 8 PESSOAS** |
| 13,5–17,1 | frango no rolete, costela, fogo, carne | — |
| 17,1–18,6 | volta pro pacu | **MAIS UMA OPÇÃO PRO / SEU FIM DE SEMANA** |
| 18,6–20,4 | foto herói + marca | brasão · SÁB E DOM · @guerreirosgrill |

Tipografia com a mesma animação do reel do Florais: linha de apoio revela em wipe,
linha de impacto entra em overshoot saindo de desfoque, régua vermelha desenha.
Nenhuma informação aparece junto com outra.

## Áudio
Nenhuma trilha foi fornecida; nada baixado de fonte não oficial. Som natural:
áudio sincronizado plano a plano (faca, gente, grelha) sobre três camas de ambiente
— noite para a parte do pacu, grelha diurna para o churrasco, noite de novo no fecho.
Os planos de foto entram em silêncio e só a cama sustenta, o que dá um respiro
antes da revelação. Média −16,3 dB, pico −0,6 dB.

Cortes todos em múltiplos de 9 frames (meio tempo a 100 BPM) — dá pra jogar um áudio
em alta por cima sem reeditar.

## Sem exagero
Só o que sabemos: Pacu · sábados e domingos · serve até 8 pessoas.
Nenhuma alegação de "melhor", "maior" ou "imperdível".

## Controle de qualidade
612 frames: 0 frames pretos, 0 moles, 0 saltos de exposição fora de corte.
Brilho 61,7–107,1. Tinta do texto x=118..962, base y=1575 (zona segura do Reels).
SAR forçado para 1:1 — as fotos são 1450×2576 e geravam pixel não-quadrado.

---

# Revisão 1 — texto por letra, foto em movimento, variedade com o Video A

## 1. Tipografia — animação por letra
A referência que você mandou é um tutorial de presets de texto do CapCut
("Letras Aleatórias", "Subida aleatória", "Crescer", "Estremecer"). O que eu tinha
animava a **linha inteira**; agora cada **letra** anima sozinha.

Motor novo (`mkpktext2.py`), por caractere:
- **entrada em cascata** — cada letra entra com atraso de 2 frames em relação à anterior
- **letras aleatórias** — nos primeiros ~5 frames a letra mostra um caractere sorteado
  antes de assentar no certo ("RH" → "PACU")
- **subida com overshoot** — sobe 38 px e escala 1,55 → 1,00 com ease out-back
- **jitter horizontal** por letra (±9 px) que assenta em zero, com semente fixa
  (determinístico entre frames, não treme sozinho)
- **rastro fantasma** — duas cópias acima em 22% e 10% de alfa durante a entrada
- **saída em cascata invertida** — as letras caem e somem da última para a primeira

## 2. As fotos agora têm gesto, e entregam pro vídeo
Como você sugeriu: a foto **entra em zoom in**, e **na hora do texto dá o zoom out
e corta pro vídeo**.

| Plano | Movimento |
|---|---|
| 0,0–1,2 s | foto, escala 1,05 → 2,25 (**zoom in**) |
| 2,1–3,6 s | foto, escala 2,25 → 1,02 (**zoom out**) — assenta exatamente quando "PACU" para de embaralhar |
| 3,6 s | **corta pro vídeo** |

É um gesto só atravessando o corte. As outras duas aparições de foto viraram vídeo:
o plano do "SERVE ATÉ 8 PESSOAS" agora é o P2 com o peixe inteiro **e a galera em
volta**, que sustenta melhor a mensagem do que uma foto parada.

Sobraram 3 momentos de foto (era 5): abre, revela e fecha.

## 3. Variedade com o Video A
O bloco do churrasco agora é liderado pelo Video A (1080×1920 nativo, o de maior
resolução do acervo):

| Tempo | Plano |
|---|---|
| 13,5 | frango dourado, close |
| 14,1 | braço levantando a costela contra o céu |
| 14,7 | costela com bacon no espeto |
| 15,3 | fogo na brasa (Florais) |
| 15,9 | frangos na grelha com a rua atrás |
| 16,5 | carne na tábua (Florais) |

## Controle de qualidade
612 frames, 0 frames pretos, 0 moles, 0 saltos de exposição fora de corte.
Tinta do texto x=148..932, base y=1562. SAR 1:1. 22 MB.
