# LOVE ME — corte final (24,2s)

Arquivo: `entrega/guerreiros-grill-LOVEME-24s.mp4`
1080×1920 · 9:16 · H.264 · 30 fps · AAC 48 kHz estéreo · 24,20 s

## Fontes
| Alias | Uso |
|---|---|
| VIDEO 1 | abertura falada — "Eu tô sabendo que você tá com fome" (1,50 s) |
| VIDEO 2 | base da montagem (19 momentos distintos) |
| VIDEO 3 | frango no rolete + fumaça (2 janelas sem texto queimado) |
| VIDEO 4 | **referência apenas** — nenhum frame usado; forneceu a trilha e a estrutura |
| VIDEO 5 | fecho com logo + frase falada |

Áudio "Love Me" extraído do VIDEO 4, que é a exportação do próprio cliente.
Nada foi baixado de fonte não oficial.

## Grade musical decodificada do VIDEO 4
80 BPM · tempo 0,75 s · compasso 3,0 s.
Compassos em 0,50 / 3,50 / 6,50 / 9,50 / 12,50 s do áudio original.
A música toca 3 tempos e cala 1 — os silêncios (−45 dB) caem em 5,62 / 8,60 / 11,60 s.
É neles que a referência corta para preto. O corte reproduz isso.

## Emenda da trilha (15,02 s → 22,02 s)
Três pedaços, todos emendados **dentro do silêncio** e alinhados ao compasso:

| Pedaço | Trecho da música | Tempo do vídeo |
|---|---|---|
| A | 2,00 → 12,00 | 0,00 → 10,00 |
| B | 6,00 → 12,00 | 10,00 → 16,00 |
| C | 9,00 → 15,02 | 16,00 → 22,02 |

Medido nas emendas: −50 dB. Inaudível.

## Linha do tempo
| Tempo | Bloco |
|---|---|
| 0,00–1,50 | VÍDEO 1 — voz em primeiro plano, música baixa por baixo |
| **1,50** | **fim da frase = corte seco + música em cheio** |
| 1,50–3,70 | montagem 1 (4 cortes) |
| 3,70–4,33 | cartela preta · LOVE vermelho |
| 4,33–6,67 | montagem 2 (4 cortes) |
| 6,67–7,30 | cartela · ME |
| 7,30–9,67 | montagem 3 (4 cortes) |
| 9,67–10,33 | cartela · OH |
| 10,33–12,67 | montagem 4 (4 cortes) |
| 12,67–13,30 | cartela · BABY |
| 13,30–15,67 | montagem 5 (4 cortes) |
| 15,67–16,30 | cartela · LOVE |
| 16,30–18,67 | montagem 6 (4 cortes) |
| 18,67–19,37 | cartela · BABY |
| 19,37–24,20 | VÍDEO 5 — logo, música caindo, frase final no silêncio |

24 cortes de comida (a referência tem 12), de 0,37 s a 0,87 s.
21 dos 23 troca-palavras caem exatamente em cima de um corte.

## Tipografia — a correção do "não está mudando as fontes"
A versão anterior trocava de fonte a cada 0,25 s (7 frames) e lia como estática.
O VIDEO 4, analisado quadro a quadro, troca a cada **2 frames**.

Agora: **12 tipos girando a cada 2 frames** (15 trocas por segundo).
Grotesca pesada · condensada · serifada itálica bold · serifada itálica fina ·
DejaVu serif · monoespaçada · expandida · oblíqua inclinada 18° ·
Liberation serif itálica · sans oblíqua · espaçada · vazada.

Altura de caixa 138 px, centralizada, a 61,5% da altura.
Branco quente `#FAF6EE` com sombra sobre comida; vermelho `#D6161C` sobre preto.
Entrada com pop 1,20 → 1,03 em 3 frames.

## Mixagem
| Trecho | Música | Voz |
|---|---|---|
| 0,00–1,40 | 0,26 (−11,7 dB) | cheia |
| 1,40–1,50 | rampa até cheia | — |
| 1,50–19,37 | cheia | — |
| 19,37–20,10 | cai para 0,22 | fala 1 do fecho |
| 20,10–21,55 | 0,22 (cama) | fala 1 |
| 21,55–22,35 | some | — |
| 22,87–23,82 | silêncio | **a frase** |

Limitador em 0,94 — pico −0,5 dB, sem clipe.

## Grade
`contrast=1,12 · brightness=+0,030 · saturation=1,12`
curva R +9% / B −7% nos médios · vinheta PI/5,5 · unsharp 0,65
Nos planos do VIDEO 3, rolloff de altas antes da grade (o céu/fumaça estourava).

## Controle de qualidade
- **Passe 1 (mudo)** — 726 frames medidos: 0 frames pretos indevidos, 0 frames moles, 0 saltos de exposição. Faixa de brilho por plano 34,9–81,0 (era 34,9–100,3 antes do ajuste no VIDEO 3).
- **Passe 2 (com som)** — 31 cortes, desvio máximo da grade de semicolcheia: 88 ms; as 6 cartelas pretas caem em janelas de −44 a −47 dB; frase final em silêncio digital antes de entrar.
- **Passe 3 (contra o VIDEO 4)** — mesma gramática: vermelho sobre preto no silêncio, branco sobre comida no compasso, fontes girando a cada 2 frames, mesma cadência de compasso. Material, cortes e ordem são próprios.
