# GUERREIRO'S GRILL FLORAIS — bastidor de domingo (15,6 s)

`entrega/guerreiros-florais-BTS-15s.mp4` — 1080×1920 · 9:16 · H.264 · 30 fps · AAC · 15,60 s

## Fontes (5 vídeos, 55,9 s de bruto → 15,6 s de corte)
| | Duração | Conteúdo | Planos usados |
|---|---|---|---|
| F1 | 19,91 s | churrasqueira, brasa, soprador, fumaça, grelha carregada | 7 |
| F2 | 5,50 s | atendente no balcão | 1 |
| F3 | 7,32 s | frangos dourados no rolete | 5 |
| F4 | 17,02 s | mãos temperando e cortando a costela | 7 |
| F5 | 6,13 s | equipe montando a linha de serviço | 2 |

Todos já nativos 1080×1920 — nenhuma barra, nenhum reenquadramento forçado.

## Estrutura
| Tempo | Bloco | Planos |
|---|---|---|
| 0,0–2,1 | **GANCHO** — fogo na brasa, soprador, fumaça | 3 |
| 2,1–6,0 | **BASTIDOR** — brasa, a equipe montando, balcão, sal na costela | 5 |
| 6,0–11,1 | **CRESCENDO** — rolete e faca alternando, cortes de 0,30 s | 10 |
| 11,1–15,6 | **PAYOFF** — frangos dourados, costela, fecho com a logo | 4 |

22 planos. O mais curto 0,30 s, o mais longo 1,80 s (o fecho).
Ritmo acelera de propósito: o bloco do crescendo tem cortes de 0,30–0,60 s.

## Grade de corte — 100 BPM
Todos os 22 cortes caem em múltiplos de 9 frames (meio tempo a 100 BPM,
1 tempo = 18 frames = 0,60 s). **Nenhum corte fora da grade.**

Isso é de propósito: você joga um áudio em alta do Instagram/TikTok por cima e os
cortes já batem, sem precisar reeditar. 100 BPM é a faixa mais comum do
short-form de comida. Se o áudio escolhido for 50 ou 200 BPM, também encaixa.

## Áudio
Nenhuma trilha foi fornecida para este projeto e não baixei nada de fonte não
oficial. O que está no arquivo é o **som natural do próprio material**:

- áudio sincronizado plano a plano (fogo, soprador, faca, vozes da equipe),
  com fade de 25 ms nas bordas de cada corte para não estalar
- uma cama de ambiente contínua tirada do F1 por baixo, a 0,42, que cola os cortes
- compressor 3:1 e limitador em 0,92

Mixagem: média −16,1 dB, pico −0,7 dB. Serve para postar como está, ou é só
substituir pelo áudio oficial no app.

## Texto
Só no gancho, saindo em 2,1 s:

```
É ASSIM QUE COMEÇA
O DOMINGO
```

Linha de apoio pequena, linha de impacto grande. Verificado por script: a tinta do
texto nunca passa de x=84..997 num quadro de 1080 — não encosta na borda.

Fecho: logo Guerreiro's Grill + **FLORAIS**, entrando em 14,0 s. Sem cartela cheia.

## Cor
O material já é quente (sol forte, chão de terra vermelha em Cuiabá): R/B de 1,507.
A primeira versão da grade levou isso para **1,745** — laranja demais, contra o
que o brief pediu. Rebalanceei levantando o azul em vez de empurrar o vermelho:

| | R/B |
|---|---|
| fonte | 1,507 |
| 1ª versão | 1,745 ❌ |
| **entregue** | **1,547** ✅ |

Contraste 1,14 · saturação 1,14 · rolloff de altas · vinheta PI/6 · unsharp 0,55.
F5 estava chapado e com névoa, levou contraste 1,26 e rolloff mais forte.

## Controle de qualidade
468 frames: 0 frames pretos, 0 moles, 0 saltos de exposição fora de corte.
Brilho por plano 48,7–90,6. Pico de áudio −0,7 dB, sem clipe.
