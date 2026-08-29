# LOVE ME — versão vertical 9:16

`entrega/guerreiros-grill-LOVEME-15s.mp4` · 15,03s · **1080×1920** · 30fps · H.264 · **sem áudio**

Reprodução vertical do formato que o cliente montou no CapCut (vídeo 4), que era
horizontal e serviu apenas como referência.

## Estrutura decodificada da referência

O vídeo 4 foi analisado quadro a quadro a cada 0,25s. A letra troca **a cada 0,25s**,
e a palavra "ME" alterna entre duas fontes — sans bold e itálico — criando pulso.

| Trecho | Conteúdo |
|--------|----------|
| 0,00 – 0,50 | preto |
| 0,50 – 1,00 | **LOVE** vermelho sobre preto |
| 1,00 – 2,50 | **ME** vermelho, alternando bold e itálico |
| 2,50 – 2,75 | **OH** |
| 2,75 – 3,25 | **BA-** |
| 3,25 – 3,50 | **BABY** |
| 3,50 – 5,75 | comida + LOVE / ME em branco |
| 5,75 – 6,50 | preto |
| 6,50 – 8,75 | comida + LOVE / ME |
| 8,75 – 9,50 | preto |
| 9,50 – 11,75 | comida + LOVE / ME |
| 11,75 – 12,50 | preto |
| 12,50 – 15,02 | comida + LOVE / ME / OH / BA- / BABY |

A duração foi casada em 15,03s contra os 15,02s da referência, para o mesmo áudio
encaixar sem ajuste.

## Comida escolhida

| Bloco | TC | Cena | Fonte |
|-------|----|------|-------|
| 1 | 3,50 | Peça com queijo derretido na tábua | V2 @ 8,20 |
| 2 | 6,50 | Rack de frangos dourados no defumador | V2 @ 5,80 |
| 3 | 9,50 | Maionese com o adesivo da marca | B @ 10,40 |
| 4 | 12,50 | Fatiando na tábua | V2 @ 11,80 |

O bloco 3 usa maionese porque a referência do cliente também usava — mantém o
paralelo com o que ele já tinha aprovado.

## Formato

Todos os quatro vídeos novos são nativos 9:16, exceto o de referência. O tratamento
usa `scale=...:force_original_aspect_ratio=increase` seguido de `crop=1080:1920` —
cobre o quadro e recorta ao centro. **Nunca pillarbox, nunca barra preta, nunca
esticado.**

## O que ficou de fora

O vídeo 4 não entrou como material: tem marca d'água do CapCut no canto e a letra
gravada por cima. É edição pronta, não bruto. Usá-lo importaria a marca d'água de
outro aplicativo para o anúncio.

## Áudio

Entregue **mudo**, de propósito. A música é o que sincroniza o formato, e ela já está
no projeto CapCut do cliente. É importar o MP4, colar o mesmo áudio por cima e as
palavras caem no lugar.

## Defeito corrigido durante o render

A letra sumia entre 3,5s e 7s. Os PNGs estavam corretos — verificado contando pixels
opacos por quadro. A causa era o `concat` por cópia de fluxo, que produzia marcação
de tempo irregular e fazia o `overlay` descartar quadros da sequência de texto.
Reencodar a base a 30fps constante resolveu.

Uma tentativa intermediária com `setpts=N/30/TB` cortou o vídeo de 15,1s para 11,7s
e foi descartada.
