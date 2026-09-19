# A Escala Que Ninguém Vê — 25,5 s

Reel vertical sobre as seis churrasqueiras funcionando ao mesmo tempo.

## Material recebido

Cinco takes, todos **4K vertical nativo**. Vale registrar: os arquivos se
declaram 3840x2160 mas carregam `displaymatrix: rotation of -90`, então o
quadro real é 2160x3840. Quem ignorar a rotação extrai tudo deitado.

| Take | Dura | Conteúdo |
|---|---|---|
| IMG_1429 | 9,74 s | Travelling lateral pela fileira, do outro lado do pátio |
| IMG_1430 | 3,00 s | Close de costela. Termina apontando para a grama, aproveitável até 2,2 s |
| IMG_1431 | 4,87 s | Close na carne com fumaça, depois abre para peças grandes |
| IMG_1433 | 2,67 s | Parede de carne, grelha lotada. O melhor plano de comida |
| IMG_1436 | 10,34 s | O pai falando na frente do banner. Fala de 2,5 s a 10,2 s |

Não existe plano de cima da escada. O reveal é o movimento do travelling
abrindo, não uma tomada estática das seis.

## Montagem

| Entra | Dura | Take | Movimento |
|---|---|---|---|
| 0,0 | 2,8 | 1433 (0,05) | punch-in 1,00→1,09, a 0,911x |
| 2,8 | 1,5 | 1430 (0,20) | 1,06→1,00 |
| 4,3 | 1,2 | 1431 (2,60) | 1,00→1,07 |
| 5,5 | 0,8 | 1431 (0,10) | 1,08→1,00 |
| 6,3 | 4,5 | 1429 (0,30) | **punch-out 1,40→1,16**, janela em fy 0,92 |
| 10,8 | 4,0 | 1429 (5,00) | 1,18→1,26, fy 0,90 |
| 14,8 | 0,5 | 1436 (0,00) | emenda |
| 15,3 | 7,8 | 1436 (2,40) | 1,00→1,04, áudio original dele |
| 23,1 | 2,4 | fecho | quadro congelado + brasão |

Cortes secos, sem transição. O ritmo vai 2,8 → 1,5 → 1,2 → 0,8, acelerando até
o reveal, e abre de novo depois dele.

O gancho usa 2,55 s de fonte esticados para 2,80 s, porque o IMG_1433 tem só
2,67 s e eu precisava de 2,8.

### Enquadramento do reveal
Na primeira versão o punch-out ia até 1,02 e o quadro virava céu e asfalto com
uma faixa fina de churrasqueira no meio. As churrasqueiras ocupam de 55% a 78%
da altura do take original. A correção foi puxar a janela de corte para baixo
(`fy=0,92`) e parar o punch-out em 1,16, o que mata a maior parte do céu e
mantém a fileira grande no quadro. Por isso o texto do reveal subiu para o
terço superior: embaixo ele cairia em cima das churrasqueiras.

## Cor
`eq` contraste 1,12 e saturação 1,04, `vibrance` 0,22 para levantar só os tons
lavados, e `selectivecolor` puxando magenta e amarelo nos vermelhos e amarelos,
que é onde vive a brasa. Depois curva em S e `unsharp`.

## Áudio
Três camadas com envelope desenhado em numpy:

| Trecho | Ambiente | Voz tratada | Música |
|---|---|---|---|
| 0 – 6,1 s | 1,00 | — | 0 |
| 6,6 – 14,9 s | 0,40 | — | 0,85 |
| 15,3 – 23,0 s | 0 | 1,00 | 0,05 |
| 23,4 – 25,5 s | 0,25 | — | 0,75 |

O ambiente cru é cortado exatamente onde a voz tratada entra, senão a fala
soaria duas vezes somada. A voz leva a mesma cadeia do anúncio do pacu: −3 dB
em 200 Hz, +4 dB em 3,8 kHz, de-esser, compressor e excitador.

A música é a faixa de referência do Emilio, a partir de 56,54 s, que é cabeça
de compasso a 90 BPM.

## Pendências
- **Legenda da fala.** Não há reconhecimento de fala neste ambiente. Falta o
  texto do que ele diz para sincronizar em cima do áudio.
- **Direitos da música.** A faixa tem dono. Por isso a entrega tem duas
  versões, e a `SEM-MUSICA` é a que se posta somando áudio pelo aplicativo.

## Entrega
- `entrega/guerreiros-ESCALA-25s.mp4` — 25,5 s, 1080x1920, 30 fps, 27,2 MB
- `entrega/guerreiros-ESCALA-25s-SEM-MUSICA.mp4` — mesma imagem, 27,2 MB
