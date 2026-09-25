# Bronca Fake — 21,7 s

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

**Texto:** frase de trend no topo e legenda só na parte do vídeo 1 (a
transcrição do vídeo 2 ainda não veio). Nenhuma palavra foi cortada ou reordenada.

- **Frase da trend** (TikTok Sans Bold, a fonte das trends do TikTok, OFL):
  "quando o marketing pede pra / gravar mais um vídeo que / vai dar 0 curtidas".
  Entra em 1,27 s (não no primeiro quadro, a pedido), junto com o punch-in da
  bronca, e sai no corte para a cor. y = 318, acima da cabeça dele.
- **Legenda do vídeo 1** (Poppins ExtraBold, minúscula, contorno preto,
  palavra-chave em vermelho). Transcrição do cliente: "Rapaz tá macia mesmo hein,
  vale até uma dancinha besta de tão macia que tá, eita trem bom rapaz, eeeee".
  Posições no vídeo 1 medidas no espectrograma: "rapaz tá macia mesmo hein"
  1,1–2,7 e "vale até uma dancinha…" 3,5–5,95 (o corte em 4,70 entra no meio
  dela, só "macia que tá" fica); "eita trem bom" 7,6–8,3; "rapaz" 9,5–10,1;
  "eeeee" ~16,2, com os braços abertos. A fala de 10,7–15,5 não está na
  transcrição e fica sem legenda.

## Linguagem do modelo aplicada
- Preto e branco no "problema" (a bronca) e **corte seco para a cor** quando a
  carne aparece.
- Punch-in seco no rosto quando ele levanta a cabeça para dar a bronca.
- Fala sem picotar, takes longos.
- Logo grande por cima da imagem no fim, com o @ embaixo. Pop de 6 quadros.
- Sem transição de efeito.

## Linha do tempo (30 fps, 651 quadros)

| Quadro | Tempo | Dura | Fonte | O quê |
|---|---|---|---|---|
| 0 | 0,00 | 1,37 | Vídeo 2, 0,40–1,77 | Trabalhando calado e sério. P&B |
| 38 | 1,27 | — | — | Entra a frase da trend no topo |
| 41 | 1,37 | 6,23 | Vídeo 2, 1,77–8,00 | **A bronca**, até o fim da última frase. Punch-in seco para 1,22 → 1,15. P&B |
| 228 | 7,60 | 3,83 | Vídeo 1, 4,70–8,53 | **Corte seco para a cor.** Sai a frase. "macia que tá". A trilha entra baixa |
| 343 | 11,43 | 9,07 | Vídeo 1, 8,67–17,73 | "eita trem bom" / "rapaz" / "eeeee". Cestos, braços abertos |
| 609 | 20,30 | — | — | Logo por cima do céu, o @ 8 quadros depois. A trilha sobe |
| 615 | 20,50 | 1,20 | Último quadro do vídeo 1 | Parado, aproximação lenta |

## Som
- Voz: passa-alta 90 Hz, redução de ruído leve, −2 dB em 250 Hz, +2,5 dB em
  3,2 kHz, compressão 2,5:1. As duas fontes ficaram no mesmo nível.
- Trilha gaúcha (`entrega/trilha-gaucha-100bpm.wav`, sintetizada no
  repositório, sem dono), a partir de 2,50 s. 11 dB abaixo da voz enquanto ele
  fala; sobe para −1 dB no logo; desce nos últimos 0,9 s.
- Medido: com trilha −14,5 LUFS, pico −2,8 dBTP. Sem trilha −14,5 LUFS, pico −1,6 dBTP.

## Entrega
- `entrega/guerreiros-BRONCA-FAKE-22s.mp4`
- `entrega/guerreiros-BRONCA-FAKE-22s-SEM-MUSICA.mp4`
