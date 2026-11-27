# Bronca Fake — 18,2 s

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

**Texto** (a pedido, no visual dos textos do CapCut; o CapCut e seus modelos não
existem neste ambiente, então o estilo foi recriado):

- **Frase da trend**, TikTok Sans ExtraBold branca **sem borda**, só uma sombra
  suave por trás; "10 curtidas" em vermelho (caixas e contorno saíram a pedido): "quando o marketing pede pra / gravar mais um vídeo
  que / vai dar 10 curtidas". Entra em 0,4 s (não no primeiro quadro) e sai no
  corte para a cor.
- **Legenda do vídeo 1** no estilo que mais viraliza hoje (Hormozi/MrBeast):
  Montserrat Black MAIÚSCULA, branca, contorno preto grosso, sombra dura,
  2 a 3 palavras por vez numa linha só, a palavra falada em vermelho com um pop
  leve (3,5 %). Cada bloco sai no quadro em que o próximo entra: antes eles se
  sobrepunham por 3 quadros na troca e a legenda "bugava".
  **Cada palavra acende no quadro exato em que começa no áudio**, marcado no
  espectrograma do mix final (antes era proporcional às sílabas, e algumas
  entravam até 0,4 s fora). Quadros de início: rapaaaz 180 · tá 268 · macia 275 ·
  bicho 290 · vale 321 · até 332 · uma 339 · dancinha 353 · besta 384 · de 397 ·
  tão 405 · macia 423 · que 431 · tá 439 · eita 450 · trem 460 · bom 465 ·
  rapaz 474 · eeeee 521.

Transcrição do cliente: "Rapaz tá macia mesmo hein (na legenda: "tá macia bicho", correção do cliente), vale até uma dancinha besta
de tão macia que tá, eita trem bom rapaz, eeeee". Ela cobre o trecho do vídeo 1
depois de 4,55 s. Posições no vídeo 1, medidas no espectrograma: rapaaaz
4,62–5,95 · tá macia mesmo hein 7,60–8,50 · vale até uma dancinha 9,50–11,45 ·
besta de tão macia que tá 11,60–13,40 · eita trem bom 13,45–14,65 · rapaz
14,85–15,55 · eeeee 16,15–16,75 (braços abertos). Transcrição do vídeo 2 (a bronca), corrigida pelo cliente: "não é hora de
gravar vídeo não, tô vendo se a costela tá boa e tá macia". Quadros de início:
não 40 · é 45 · hora 49 · de 57 · gravar 61 · vídeo 67 · não 79 · tô 121 · vendo 124 · se 133 · a 135 ·
costela 137 · tá 147 · boa 150 · e 155 · tá 156 · macia 160.

## Linguagem do modelo aplicada
- Preto e branco no "problema" (a bronca) e **corte seco para a cor** quando a
  carne aparece.
- Punch-in seco no rosto quando ele levanta a cabeça para dar a bronca.
- Fala sem picotar, takes longos.
- Sem transição de efeito.

## Linha do tempo (30 fps, 545 quadros)

Revisão: corte direto da bronca para o "rapaaaz". A bronca acaba em 6,22 no
vídeo 2 (antes o corte ia até 8,20: 2 s dele calado); o "ra-" começa em 4,64
no vídeo 1. Agora a bronca termina no quadro 173, o corte cai no 177 e o
"rapaaaz" começa no 180.

| Quadro | Tempo | Dura | Fonte | O quê |
|---|---|---|---|---|
| 0 | 0,00 | 1,37 | Vídeo 2, 0,40–1,77 | Trabalhando calado e sério. P&B |
| 12 | 0,40 | — | — | Entra a frase da trend |
| 41 | 1,37 | 4,53 | Vídeo 2, 1,77–6,30 | **A bronca**. Punch-in seco para 1,22 → 1,16. P&B |
| 177 | 5,90 | 3,93 | Vídeo 1, 4,60–8,53 | **Corte seco para a cor**, direto no "rapaaaz". A trilha entra baixa |
| 295 | 9,83 | 8,33 | Vídeo 1, 8,67–17,00 | Take B entra 10% mais fechado e abre até 1,02 |

## Som
- Voz: passa-alta 90 Hz, redução de ruído leve, −2 dB em 250 Hz, +2,5 dB em
  3,2 kHz, compressão 2,5:1. As duas fontes ficaram no mesmo nível.
- Trilha gaúcha (`entrega/trilha-gaucha-100bpm.wav`, sintetizada no
  repositório, sem dono), a partir de 2,50 s. 11 dB abaixo da voz enquanto ele
  fala; sobe depois do "eeeee" e desce nos últimos 0,9 s.
- Medido: com trilha −14,3 LUFS, pico −4,2 dBTP. Sem trilha −14,3 LUFS, pico −3,7 dBTP.

## Música
O cliente vai colocar a música de fundo ele mesmo: a versão para postar é a
`-SEM-MUSICA` (voz e ambiente, −14,3 LUFS, pico −3,7 dBTP).

## Variante colorida
No teste do Instagram muita gente pulou no começo em preto e branco. A
variante `-COR` tem a bronca colorida (mesma correção de pele do vídeo 1),
todo o resto idêntico. Gerada com `COR=1 ./build.sh` e `SUF=-COR ./render.sh`.
Medido: −14,3 LUFS, pico −4,2 dBTP (com trilha) e −3,7 dBTP (sem).

## Entrega
- `entrega/guerreiros-BRONCA-FAKE-18s.mp4`
- `entrega/guerreiros-BRONCA-FAKE-18s-SEM-MUSICA.mp4`
- `entrega/guerreiros-BRONCA-FAKE-18s-COR.mp4` e `-COR-SEM-MUSICA.mp4` (sem o P&B)
