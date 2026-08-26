# Corte na batida — 120 BPM

`entrega/guerreiros-grill-REELS-BATIDA-12s.mp4` · 12,00s cravados · 1080×1920 · 30fps

Estilo escolhido pelo cliente: clipe energético, não documentário.

## A grade

120 BPM = **0,5s por batida**. 24 batidas = 12,00s exatos.
Todo corte cai numa batida. Qualquer áudio de 120 BPM encaixa sem ajuste.

| # | TC | Batidas | Cena | Fonte | Zoom |
|---|----|---------|------|-------|------|
| 01 | 00,0 | 2 | **FOGO** slow-motion 1,62× | C @ 8,10 | — |
| 02 | 01,0 | 1 | Grelha lotada | C @ 0,35 | — |
| 03 | 01,5 | 1 | Frango dourado | A @ 1,95 | ✓ |
| 04 | 02,0 | 1 | Fileiras glaceadas | C @ 5,15 | — |
| 05 | 02,5 | 1 | Grelha vista de cima | B @ 13,50 | ✓ |
| 06 | 03,0 | 2 | Corte da carne | B @ 18,35 | — |
| 07 | 04,0 | 1 | Espetos | C @ 11,25 | ✓ |
| 08 | 04,5 | 1 | Frangos na brasa | A @ 10,50 | — |
| 09 | 05,0 | 2 | Tesoura no frango | B @ 23,90 | ✓ |
| 10 | 06,0 | 1 | Glacê em close | C @ 6,40 | — |
| 11 | 06,5 | 1 | Peça glaceada | A @ 7,10 | ✓ |
| 12 | 07,0 | 2 | Equipe tirando peça | B @ 20,55 | — |
| 13 | 08,0 | 1 | Profundidade da grelha | C @ 2,75 | ✓ |
| 14 | 08,5 | 1 | Fatias na tábua | B @ 19,30 | — |
| 15 | 09,0 | 1 | Grelha | C @ 12,45 | ✓ |
| 16 | 09,5 | 1 | Frango em close | A @ 2,60 | — |
| 17 | 10,0 | 4 | End card | — | — |

**Zoom punch:** escala animada de 1,00 a 1,09 ao longo do corte, alternando sim/não
para criar pulso. Sete cortes têm, nove não.

**Texto:** `CHURRASCO RAIZ` de 0,5 a 2,02s, entrando na batida 2 com fade de 0,08s —
rápido o bastante para ler como "pop" no tempo.

**Áudio:** ambiência real a **−24 LUFS**, de propósito bem baixa. É leito, não trilha.
A música entra por cima no CapCut sem brigar.

## Como o cliente usa

1. Importa no CapCut
2. Adiciona um áudio em alta de ~120 BPM
3. Os cortes já caem na batida — não precisa ajustar nada

## Defeito corrigido durante o build

O zoom punch por `crop` animado gerava dimensões ímpares e o libx264 rejeitava com
`Invalid argument`, sem escrever nada no arquivo. Trocado por `scale` animado com
`trunc(...)*2` forçando dimensões pares, seguido de `crop` fixo em 1080×1920.
