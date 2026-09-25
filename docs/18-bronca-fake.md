# Bronca Fake — 13,8 s

Vídeo de comédia com o pai. Referência de linguagem: `copy_7B80…` (o "queimou
tudo" em preto e branco, que vira cor quando a grelha abre, e fecha com a
pegadinha). Brutos: vídeo 1 (`copy_5283…`, exportação do CapCut, 1080p, dois
takes emendados em 8,5 s) e IMG_1442 (4K).
Receita: `projetos/bronca/project/build.sh` e `mix.py`.

**Sem legenda, a pedido:** o cliente coloca depois. Sem reconhecimento de fala
no ambiente, as falas não foram transcritas. Nenhuma palavra foi cortada ou
reordenada: os cortes caem nas pausas medidas na voz.

## O que veio da referência
- Preto e branco no "problema" e cor na virada. Lá a cor volta quando a grelha
  abre; aqui volta quando ele olha para a câmera e sorri.
- Takes longos enquanto ele fala, corte seco na virada, sem transição de efeito.
- Voz e ambiente reais no começo; trilha só quando a carne aparece.
- Não copiado: diálogo, peruca, pegadinha, texto, planos.

## Linha do tempo (30 fps, 413 quadros)

| Quadro | Tempo | Dura | Fonte | O quê |
|---|---|---|---|---|
| 0 | 0,00 | 7,40 | Vídeo 1, 0,95–8,35 | A bronca, P&B. Fala 1,0–2,5 e 3,5–5,9; 1,6 s calado virando a carne; uma palavra em 7,6. Aproximação 1,00→1,07 (fonte 1080p) |
| 222 | 7,40 | 2,70 | IMG_1442, 0,90–3,60 | Calado e sério 0,9 s, levanta os olhos, fala, **sorri**. A cor volta em 4 quadros no sorriso. Aproximação 1,08→1,16 (fonte 4K) |
| 303 | 10,10 | 2,10 | IMG_1452, 3,30–5,40 | A carne, grade com céu e fumaça. **A trilha entra seca no corte** |
| 366 | 12,20 | 1,57 | Vinheta | Logo, a trilha desce junto com o escurecimento |

## Som
- Voz: passa-alta 90 Hz, redução de ruído leve (6 dB), −2 dB em 250 Hz,
  +2,5 dB em 3,2 kHz, compressão 2,5:1. Sem excitador nem de-esser, para não
  soar processada.
- Trilha: `entrega/trilha-gaucha-100bpm.wav` (sintetizada no repositório,
  sem dono), a partir de 2,50 s, numa cabeça de compasso, 1,5 dB abaixo da voz.
- Chiado real do IMG_1452 por baixo da trilha.
- Medido: com trilha −14,7 LUFS, sem trilha −14,2 LUFS, pico −3,5 dBTP.

## Cor
Correção leve, sem filtro. P&B com contraste 1,14 e altas seguradas. Pele e
carne com vibrance baixo, sem empurrar o laranja.

## Entrega
- `entrega/guerreiros-BRONCA-FAKE-14s.mp4`
- `entrega/guerreiros-BRONCA-FAKE-14s-SEM-MUSICA.mp4`
