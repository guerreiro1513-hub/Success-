# Bronca Fake — 19,4 s

Vídeo de comédia com o pai, só com os vídeos 1 e 2, editado na linguagem do
vídeo-modelo (`copy_7B80…`). Nenhum take da ESCALA.
Receita: `projetos/bronca/project/build.sh`, `mktx.py`, `mix.py`, `render.sh`.

Brutos:
- **Vídeo 2** (IMG_1442, 4K): trabalha calado até 1,7 s, levanta a cabeça e dá
  a bronca olhando para a câmera (o trecho mais alto do áudio, 1,75–2,6 s),
  continua falando e volta a trabalhar.
- **Vídeo 1** (`copy_5283…`, exportação do CapCut, 1080p): o 2º take inteiro,
  8,67–17,73 s (a emenda do CapCut vai até 8,63). Ele na churrasqueira, a câmera abre, cestos cheios girando na frente, ele andando e falando, os
  braços abertos em ~16,4 s. Depois de 17,8 s é a marca do CapCut.

**Sem legenda, a pedido.** Nenhuma palavra foi cortada ou reordenada.

## Linguagem do modelo aplicada
- Preto e branco no "problema" (a bronca) e **corte seco para a cor** quando a
  carne aparece.
- Punch-in seco no rosto quando ele levanta a cabeça para dar a bronca.
- Fala sem picotar, takes longos.
- Logo grande por cima da imagem no fim, com o @ embaixo. Pop de 6 quadros.
- Sem transição de efeito.

## Linha do tempo (30 fps, 582 quadros)

Revisão do cliente: o vídeo 2 fica como estava; o vídeo 1 entra em **4,70 s**
e vai até o fim. A emenda do CapCut entre os takes do vídeo 1 (8,53–8,63) fica
de fora e vira um corte seco.

| Quadro | Tempo | Dura | Fonte | O quê |
|---|---|---|---|---|
| 0 | 0,00 | 0,77 | Vídeo 2, 1,00 | Trabalhando calado e sério. P&B |
| 23 | 0,77 | 4,53 | Vídeo 2, 1,77–6,30 | **A bronca**. Punch-in seco para 1,22. P&B |
| 159 | 5,30 | 3,83 | Vídeo 1, 4,70–8,53 | **Corte seco para a cor.** Ele na churrasqueira. A trilha entra baixa |
| 274 | 9,13 | 9,07 | Vídeo 1, 8,67–17,73 | A câmera abre, cestos cheios, ele andando, braços abertos |
| 540 | 18,00 | — | — | O logo entra por cima do céu, o @ 8 quadros depois. A trilha sobe |
| 546 | 18,20 | 1,20 | Último quadro do vídeo 1 | Parado, aproximação lenta |

Verificado: só os cortes de 0,77, 5,30 e 9,13 s.

## Som
- Voz: passa-alta 90 Hz, redução de ruído leve, −2 dB em 250 Hz, +2,5 dB em
  3,2 kHz, compressão 2,5:1. As duas fontes ficaram no mesmo nível.
- Trilha gaúcha (`entrega/trilha-gaucha-100bpm.wav`, sintetizada no
  repositório, sem dono), a partir de 2,50 s. 11 dB abaixo da voz enquanto ele
  fala; sobe para −1 dB no logo; desce nos últimos 0,9 s.
- Medido: com trilha −14,3 LUFS, pico −3,0 dBTP. Sem trilha −14,2 LUFS, pico −3,4 dBTP.

## Entrega
- `entrega/guerreiros-BRONCA-FAKE-19s.mp4`
- `entrega/guerreiros-BRONCA-FAKE-19s-SEM-MUSICA.mp4`
