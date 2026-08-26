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


---

## Revisão do começo

Feedback do cliente: *"esse começo ficou ruim demais"*.

### O que estava errado

O hook original era o fogo num **recorte fechado** (594×1056) e em **slow-motion 1,62×**.
Dois erros somados:

1. **Ilegível.** O recorte apertado transformava a cena em mistura escura de tela de
   grelha e espeto. A chama ficava pequena no alto e não se entendia o que era.
   Brilho médio de 57 contra 66 do plano de comida.
2. **Slow-motion contradizia o formato.** Um clipe de batida abre no impacto. Começar
   devagar e acelerar depois derrubava a energia justo no primeiro segundo.

### A correção, em duas etapas

Primeiro abri o enquadramento do fogo e tirei o slow-motion. Melhorou, mas o
diagnóstico real era outro: **fogo é dramático e abstrato**. Num quadro de celular,
em meio segundo, comida óbvia vence drama abstrato.

Novo começo:

| TC | Dur | Cena | Fonte |
|----|-----|------|-------|
| 00,0 | 1,0s | **Tesoura rasgando o frango assado**, luva preta, logo do avental à vista | B @ 24,20 |
| 01,0 | 0,5s | **FOGO** — agora acento, em enquadramento aberto e velocidade normal | C @ 8,20 |
| 01,5 | 0,5s | Frango dourado em close + texto | A @ 2,10 |

O plano de abertura junta ação humana, comida reconhecível e a marca no avental —
os três em brilho 62, contra os 57 do fogo fechado.

O plano da tesoura que ocupava a posição 9 foi trocado pelo rack de frangos
(A @ 3,20) para não repetir a mesma cena no mesmo filme. O texto desceu para 1,5s,
acompanhando o novo ponto de entrada do frango. A grade de 120 BPM segue intacta:
12,00s cravados.


---

## Revisão da repetição

Feedback do cliente: *"essa parte do último vídeo está ruim, está se repetindo muito"*.

### O erro

Seis dos dezesseis cortes vinham do vídeo C. Pior: os seis são a **mesma imagem** —
grelha de arame vista de cima com carne glaceada. Ângulos parecidos, cor parecida,
textura parecida. Em doze segundos isso lê como repetição, mesmo com corte rápido.

### A correção

C caiu de **6 cortes para 2**, escolhidos por serem os dois mais diferentes entre si:
a labareda e os espetos. Os quatro que saíram foram substituídos por material de A e
B que estava sobrando sem uso.

**Distribuição final: A×6, B×8, C×2.**

| # | TC | Dur | Cena | Fonte |
|---|----|-----|------|-------|
| 01 | 00,0 | 1,0 | Tesoura rasgando o frango | B @ 24,20 |
| 02 | 01,0 | 0,5 | **FOGO** | C @ 8,20 |
| 03 | 01,5 | 0,5 | Frango dourado | A @ 2,10 |
| 04 | 02,0 | 0,5 | Grelha de costelas vista de cima | B @ 13,50 |
| 05 | 02,5 | 0,5 | Peça glaceada com bacon | A @ 7,10 |
| 06 | 03,0 | 1,0 | Corte da carne, luva preta | B @ 18,35 |
| 07 | 04,0 | 0,5 | Braço entrando no fogo | A @ 15,00 |
| 08 | 04,5 | 0,5 | **Maionese com o adesivo da marca** | B @ 11,30 |
| 09 | 05,0 | 1,0 | Equipe tirando peça da grelha | B @ 20,55 |
| 10 | 06,0 | 0,5 | Rack de frangos no defumador | A @ 3,20 |
| 11 | 06,5 | 0,5 | Espetos | C @ 11,25 |
| 12 | 07,0 | 1,0 | **O defumador na calçada, com fumaça** | B @ 3,40 |
| 13 | 08,0 | 0,5 | Frangos na brasa | A @ 10,50 |
| 14 | 08,5 | 0,5 | Fatias na tábua | B @ 19,30 |
| 15 | 09,0 | 0,5 | **Atendente de chapéu com a bandeja** | B @ 7,80 |
| 16 | 09,5 | 0,5 | Garfo trinchante na carne | A @ 0,40 |
| 17 | 10,0 | 2,0 | End card | — |

### Ajuste de exposição

Dois planos novos vinham muito mais claros que o resto — a peça glaceada (brilho 155)
e o atendente com a bandeja (129), contra uma média de 60 nos demais. Sem correção
piscariam no meio do clipe. Ambos receberam `brightness=-0,055` para casar com a
sequência.

A grade de 120 BPM segue intacta: 12,00s exatos.
