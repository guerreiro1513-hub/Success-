# Bronca Fake — 20,1 s

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
  2 a 3 palavras por vez numa linha só, a palavra falada em vermelho com um pop.
  Cada palavra acende proporcional às sílabas dentro do trecho medido.

Transcrição do cliente: "Rapaz tá macia mesmo hein (na legenda: "tá macia bicho", correção do cliente), vale até uma dancinha besta
de tão macia que tá, eita trem bom rapaz, eeeee". Ela cobre o trecho do vídeo 1
depois de 4,55 s. Posições no vídeo 1, medidas no espectrograma: rapaaaz
4,62–5,95 · tá macia mesmo hein 7,60–8,50 · vale até uma dancinha 9,50–11,45 ·
besta de tão macia que tá 11,60–13,40 · eita trem bom 13,45–14,65 · rapaz
14,85–15,55 · eeeee 16,15–16,75 (braços abertos). A bronca do vídeo 2 ainda
não tem transcrição.

## Linguagem do modelo aplicada
- Preto e branco no "problema" (a bronca) e **corte seco para a cor** quando a
  carne aparece.
- Punch-in seco no rosto quando ele levanta a cabeça para dar a bronca.
- Fala sem picotar, takes longos.
- Sem transição de efeito.

## Linha do tempo (30 fps, 603 quadros)

Cortes melhorados: o vídeo 2 vai até 8,20 (a última frase acaba em 7,96), então
há ~0,2 s de respiro antes da virada para a cor. Na troca de take dentro do
vídeo 1 o take B entra 10% mais fechado e abre até 1,02, disfarçando o salto
de posição.

Revisões: o vídeo 1 entra em 4,55 (na pausa antes do "rapaaaz", que o 4,70
cortava); o final (quadro parado com logo) saiu a pedido; o vídeo termina
depois do "eeeee".

| Quadro | Tempo | Dura | Fonte | O quê |
|---|---|---|---|---|
| 0 | 0,00 | 1,37 | Vídeo 2, 0,40–1,77 | Trabalhando calado e sério. P&B |
| 12 | 0,40 | — | — | Entra a frase da trend |
| 41 | 1,37 | 6,43 | Vídeo 2, 1,77–8,20 | **A bronca**. Punch-in seco para 1,22 → 1,15. P&B |
| 234 | 7,80 | 3,97 | Vídeo 1, 4,55–8,53 | **Corte seco para a cor.** "rapaaaz", "tá macia mesmo hein". A trilha entra baixa |
| 353 | 11,77 | 8,33 | Vídeo 1, 8,67–17,00 | "vale até uma dancinha besta de tão macia que tá", "eita trem bom", "rapaz", "eeeee" |

## Som
- Voz: passa-alta 90 Hz, redução de ruído leve, −2 dB em 250 Hz, +2,5 dB em
  3,2 kHz, compressão 2,5:1. As duas fontes ficaram no mesmo nível.
- Trilha gaúcha (`entrega/trilha-gaucha-100bpm.wav`, sintetizada no
  repositório, sem dono), a partir de 2,50 s. 11 dB abaixo da voz enquanto ele
  fala; sobe depois do "eeeee" e desce nos últimos 0,9 s.
- Medido: com trilha −14,6 LUFS, pico −2,1 dBTP. Sem trilha −14,6 LUFS, pico −2,3 dBTP.

## Música
O cliente vai colocar a música de fundo ele mesmo: a versão para postar é a
`-SEM-MUSICA` (voz e ambiente, −14,6 LUFS, pico −2,3 dBTP).

## Entrega
- `entrega/guerreiros-BRONCA-FAKE-20s.mp4`
- `entrega/guerreiros-BRONCA-FAKE-20s-SEM-MUSICA.mp4`
