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

---

# Revisão 1 — animação de texto e fecho

## O que estava errado
Duas coisas, e as duas procediam:

1. **O texto não tinha animação.** Um pop de escala de 3 frames e pronto. Ficava
   parado 1,9 s — pouco até para ler.
2. **O fecho estava mal feito.** A logo entrava num fade seco. Pior: o asset
   `logo_crop.jpg` é um recorte de frame de vídeo, ou seja, **tem fundo escuro
   texturizado junto**. Colado por cima do plano, virava uma caixa preta.

## Brasão recortado
Extraí o brasão do fundo fotográfico com OpenCV: limiar no contorno branco do
escudo, fechamento morfológico para unir o anel, preenchimento do contorno,
dilatação de 5 px e feather. Resultado em `referencias/logo-brasao-recortado.png`
(607×551 RGBA, 73,6% de cobertura). Agora o escudo assenta no vídeo sem caixa.

## Animação do gancho — 0,27 s a 2,60 s (2,33 s)
| Frame | O que acontece |
|---|---|
| 9–22 | "É ASSIM QUE COMEÇA" **revela da esquerda para a direita** (wipe com borda suave, ease out-cubic), subindo 22 px |
| 24–38 | "O DOMINGO" **entra em impacto**: escala 1,28 → 1,00 com overshoot (out-back) |
| 24–31 | desfoque de movimento 6 px → 0 na entrada do impacto |
| 36–46 | **régua vermelha desenha** da esquerda para a direita sob "O DOMINGO" |
| 9–70 | deriva contínua de subida (0,26 px/frame) — nada fica estático |
| 70–81 | saída: sobe 58 px com ease in-cubic + fade |

## Fecho — 13,4 s a 15,6 s
| Frame | O que acontece |
|---|---|
| 402–418 | **scrim** em degradê sobe do rodapé (0 → 198 de alfa a partir de 50% da altura) |
| 408–426 | **brasão entra** com escala 1,30 → 1,00 (out-back) e desfoque 5 px → 0 |
| 426–437 | **régua vermelha desenha do centro para fora** |
| 432–445 | **FLORAIS** revela em wipe |
| 442–456 | **@GUERREIROSGRILL** entra em fade |
| 402–468 | deriva de subida contínua |

Bloco final reposicionado de y=1288 para **y=1170**: a base do texto agora fica em
**y=1561**, dentro da zona segura do Reels (a interface do Instagram cobre o rodapé).

## Controle de qualidade
468 frames: 0 frames pretos, 0 moles, 0 saltos de exposição fora de corte.
Tinta do texto x=106..975 (margens de 105 px), base y=1561. Verificado por script.
