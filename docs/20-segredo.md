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
