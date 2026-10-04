# O Segredo — reel de humor (11,2 s, 337 quadros, 30 fps)

Conceito: o dono chama a câmera como quem vai contar algo confidencial. O segredo é
"Sabe o que tem aqui no Guerreiro's Grill? Carne boa." e logo depois entra um
"the making" de cinema com as carnes reais da casa.

## Inventário
| Arquivo | Duração | Conteúdo | Uso |
|---|---|---|---|
| IMG_1440 | 8,1 s | Chama com o dedo e vem até a câmera; depois cochicha colado na lente (2 vezes) | 0–1,27 s (só o gesto, sem a fala) |
| IMG_1441 | 8,3 s | Fala 1 (1,4–2,9), olha pros lados desconfiado (3,0–4,9), fala 2 (5,0–6,7) e ri | 3,0–7,3 s (desconfiança, fala 2, risada) |
| IMG_1430 / 1431 | 3,0 / 4,9 s | Churrasqueira (já usados na ESCALA) | Não usados |
| COMIDA_DIA (3c86…) | 20,4 s, 60p | Reel editado de comida, dia | Carne levantada no garfo (8,5 s) |
| COMIDA_NOITE (755c…) | 14,4 s, 60p, 720p | Reel editado de comida, noite | Faca na carne crua, fatiando costela, fogo (câmera lenta 2x) |
| REFERENCIA (4204…) | 18,4 s | "The making Steak" (TikTok) | Só referência de estilo |

## Linha do tempo
| Quadros | Take | O que acontece |
|---|---|---|
| 0–37 | 1440 0,00 | Chama com o dedo. Texto "Ele vai contar um segredo…" |
| 38–94 | 1441 3,00 | Olha pros lados. Ambiente 8 dB abaixo (suspense quieto) |
| 95–166 | 1441 4,90 | Punch-in em corte seco (1,15x). Fala com legenda e risada |
| 167–196 | NOITE 1,84 | Faca na carne crua (câmera lenta 2x). Entra a música épica |
| 197–229 | DIA 8,50 | Carne levantada no garfo |
| 230–259 | NOITE 8,50 | Fatiando a costela (câmera lenta 2x) |
| 260–289 | NOITE 11,10 | Fogo na grelha (câmera lenta 2x) |
| 290–336 | T07 | Vinheta |

Legendas (estimadas pela energia da voz, sem transcrição automática): "Sabe o que
tem aqui" 98–122, "no Guerreiro's Grill?" 123–135, "CARNE BOA." 136–160.

Cor: natural no pai; "the making" com look de cinema (sombras fundas, fogo quente,
vinheta), mais leve nas cenas noturnas. Sem zoom animado.

Som: fala original com limpeza leve (passa-alta, redução de ruído, presença,
compressão 2,5:1). Música épica do Kairogen (2 créditos) entra no corte para o
making. Ganho fixo para −14 LUFS (o loudnorm dinâmico levantava o ruído de rua).
Medido: −14,6 LUFS / −2,7 dBFS.

Pipeline: `project/build.sh` → `mktx.py` → `mix.py` → `render.sh`.
Entrega: `entrega/guerreiros-SEGREDO-11s.mp4`.

# v2 — fala certa e sem barulho de carro (12,4 s, 373 quadros)
Feedback: "o segredo tá muito som de carro e tá cortado o vídeo errado".
- Os papéis estavam invertidos: o **1440 é o close da fala** (ele cochicha colado na
  lente) e o 1441 é o da mão. A fala agora sai do 1440, take 2 (fala de 5,40 a 6,75 s),
  inteiro e sem corte: levanta a mão, encosta na lente, conta, se afasta rindo e faz joinha.
- Linha do tempo: 1440 0,00 (chama com o dedo, 42 q) → 1441 3,00 (olha pros lados,
  só imagem, 48 q) → 1440 4,30 (segredo + risada + joinha, 113 q) → making (123 q) → vinheta.
- Ruído: `project/denoise.py` faz subtração espectral com perfil de ruído dos trechos
  sem fala de cada take (grave de motor cortado forte), e o ambiente fica 10 dB abaixo
  fora da fala. Ruído de rua de −21 para −40 dB; a fala fica ~22 dB acima.
- Medido: −14,8 LUFS / −3,0 dBFS. Entrega: `entrega/guerreiros-SEGREDO-12s.mp4`.

# v3 — plano único na chegada e legenda certa (10,2 s, 307 quadros)
Feedback: cortes do começo ruins (quer que, quando ele chama, já venha a câmera indo
na direção dele) e legenda errada. A fala real é **"No Guerreiro's Grill tem carne
de qualidade."**
- O 1441 saiu. O começo é um plano só do 1440 (take 1, 0,00–3,47 s): ele chama, a
  câmera vai até ele e ele cochicha colado na lente (fala de 1,85 a 3,35 s). Depois,
  corte para a risada com joinha (1440, 6,95–8,05 s), making e vinheta.
- Legendas pela pausa da voz em 2,42 s (fim de "Grill", 5ª de 13 sílabas):
  "No Guerreiro's Grill" (q 55–72), "tem carne" + "DE QUALIDADE." (q 73–103).
- Entrega: `entrega/guerreiros-SEGREDO-10s.mp4` (substitui a de 12 s).

# v4 — pergunta + resposta, começo editado, making maior (15,6 s, 468 quadros)
Feedback: a fala do take 1 é a pergunta **"Sabe o que tem no Guerreiro's Grill?"**;
a resposta **"No Guerreiro's Grill tem carne de qualidade."** vem de outra fala (take 2).
Vídeo curto: mais cinema, começo mais editado para segurar quem assiste.
- Gancho: "O SEGREDO / do Guerreiro's Grill" no 1º quadro; punch-in seco no dedo
  chamando (1,22x); chegada da câmera acelerada 1,6x.
- Fala: pergunta 1440 1,80–3,42 s (q 45–93) e resposta 1440 5,25–6,80 s (q 94–140),
  emendadas no mesmo enquadramento colado na lente; risada e joinha (q 141–177).
- Som: música de suspense "na ponta dos pés" (Kairogen, 2 créditos) 13 dB abaixo da fala
  até o impacto; corte seco para a épica no making (q 178).
- Making com 8 planos (~8 s): fogo, faca na carne crua, grelha giratória, carne no
  garfo, tesoura no frango, fatiando costela, fatiando na tábua, o dono fatiando com fumaça.
  Câmera lenta 2x só nos planos com 60 quadros reais (sem quadro repetido).
- Medido: −15,2 LUFS / −1,9 dBFS. Entrega: `entrega/guerreiros-SEGREDO-15s.mp4`.

# v5 — começo de cinema, mais claro, legenda nova e música nova (15,6 s)
Feedback: começo cinematográfico, takes menos escuros, falas = "Sabe o que tem no
Guerreiro's Grill?" e, no corte, só "Carne de qualidade.", legenda bonita, trocar música.
- Cor: cinema claro em tudo (curva fílmica com meios-tons erguidos, sombras frias,
  altas quentes) + halation e grão fino no render (menos a vinheta). Brilho médio:
  pai 113 → 121, making 60 → 84 (escala 0–255).
- Abertura: título "o segredo do / Guerreiro's Grill" em Playfair itálico, marca em
  dourado com brilho (no estilo do "The making / Steak" da referência).
- Legendas palavra a palavra (Poppins ExtraBold): a palavra entra com pop e fica dourada
  enquanto é dita; marca e QUALIDADE em dourado. Tempo por sílaba dentro de cada trecho
  de fala (pergunta 1,85–2,42 / 2,45–3,35 s do take 1; resposta 5,45–6,75 s do take 2).
- Música (Kairogen, 5 créditos): "trailer" (piano, relógio, cordas, sobe até um drop)
  por baixo da fala, com o drop (12,065 s) no corte do making; ali entra o "groove"
  épico no impacto dele (1,06 s) até o fim.
- Medido: −14,8 LUFS / −3,3 dBFS.

# v6 — making todo em câmera lenta e a música escolhida pelo cliente (16,7 s, 501 quadros)
- Os 8 planos do making agora são todos em câmera lenta 2x. Os de 60 quadros reais
  usam os quadros da câmera; os dois de 30 quadros (fatiando na tábua e o dono com
  fumaça) são interpolados (`minterpolate` mci). Nenhum quadro repetido.
- Música: a do vídeo que o cliente mandou (`source/MUSICA_REF.mp4`, até 19,9 s; a
  vinheta sonora do TikTok no fim fica de fora). ~97 BPM; a batida de grave de 7,22 s
  cai no corte do making (q 178). Fica 12 dB abaixo nas falas e sobe no corte.
- Medido: −14,6 LUFS / −2,6 dBFS. Entrega: `entrega/guerreiros-SEGREDO-16s.mp4`.

# v7 — mais cinema (16,7 s)
Render: reforço de cor (sombras frias, altas quentes, sem escurecer), bordas
desfocadas como lente aberta (`project/mkmask.py` + maskedmerge), halation mais forte,
leve aberração cromática, grão e faixas pretas de cinema (140 px em cima e embaixo,
menos na vinheta). Brilho médio mantido: pai 122,8 / making 84,6.
