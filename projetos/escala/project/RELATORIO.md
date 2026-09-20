# A Escala Que Ninguém Vê — relatório técnico

Reel vertical, 21,333 s, 1080x1920, 30 fps.
Entrega: `entrega/guerreiros-ESCALA-21s.mp4` e a variante `-SEM-MUSICA`.

## Ferramentas disponíveis: o que existe e o que não existe

Procurei antes de começar. **Não há skill de edição de vídeo, FFmpeg, motion
design ou color grading instalada** nesta sessão. As que existem são de
documento (docx, pptx, xlsx, pdf), artifacts e afins.

**HyperFrames não serve para este trabalho**, e não é questão de preferência.
Ele monta projetos de vídeo em HTML/GSAP renderizados na nuvem da HeyGen, a
partir de texto e blocos. Ele não corta material bruto: não recebe estes `.mov`,
não reenquadra, não faz grade de cor em imagem filmada. Além disso, as próprias
instruções do servidor dizem que `compose` e `render_video` ficam **desativados**
em cliente com sistema de arquivos local, que é o caso aqui. Preferi dizer isso
a citá-lo no relatório fingindo uso.

O trabalho foi feito com FFmpeg para corte, reenquadramento e grade, e com
Python (numpy, PIL) para análise de material, detecção do impacto musical,
envelopes de mixagem e a tipografia quadro a quadro.

## Inventário medido

Medido a cada 0,25 s: nitidez (desvio padrão do detector de bordas), brilho,
movimento (diferença média entre quadros) e calor (R menos B).

| Take | Arquivo | Dura | Nitidez | Movimento | Calor | Conteúdo |
|---|---|---|---|---|---|---|
| T01 | IMG_1429 | 9,74 s | **45,1** | 14,97 | **−17,3** | Travelling lateral pela fileira |
| T02 | IMG_1430 | 2,97 s | 55,2 | 45,56 | +29,9 | Close de costela. Termina na grama |
| T03 | IMG_1431 | 4,87 s | 59,2 | 37,00 | **+36,4** | Fumaça e peças grandes |
| T04 | IMG_1433 | 2,67 s | **70,2** | 46,72 | +34,3 | Parede de carne |
| T05 | IMG_1436 | 10,34 s | 51,5 | 26,53 | +10,4 | O pai falando |

Três decisões saíram direto desses números:

1. **T04 abre o vídeo.** É a tomada mais nítida do lote por 11 pontos.
2. **T01 leva grade própria.** É 25 pontos menos nítida e 50 pontos mais fria
   que os closes. Cortar dos closes para ela sem tratamento lia como queda de
   qualidade justamente no reveal. Ela recebe `unsharp 7:7:0.95` contra 5:5:0.55
   dos closes, mais `colorbalance` empurrando quente, mais vibrance 0,30.
3. **T02 só em cortes curtos.** Movimento 45,6 é tremor de mão; em plano longo
   apareceria.

Também medi que **o trabalhador de camisa azul sai do quadro do T04 em 1,00 s**.
Todos os três usos do T04 entram depois disso.

Os arquivos se declaram 3840x2160 mas carregam `displaymatrix: rotation of -90`.
O quadro real é **2160x3840**. Quem ignorar a rotação extrai tudo deitado. Como
a fonte é 2160 de largura e a saída 1080, há folga de sobra: nenhum
reenquadramento ampliou pixel.

## Linha do tempo

O andamento da música é **90 BPM**, medido por autocorrelação do envelope de
ataques. Um tempo de 90 BPM é 0,66667 s, que a 30 fps dá **exatamente 20
quadros**. A grade de corte é a grade musical, sem esticar nada.

| Quadro | Tempo | Dura | Take | Entrada | Zoom | Janela | Papel |
|---|---|---|---|---|---|---|---|
| 0 | 0,000 | 1,50 | T04 | 1,00 | 1,02→1,12 | centro | Gancho |
| 45 | 1,500 | 1,33 | T03 | 3,40 | 1,12→1,02 | centro | |
| 85 | 2,833 | 1,17 | T02 | 0,20 | 1,02→1,11 | centro | |
| 120 | 4,000 | 0,83 | T03 | 2,20 | 1,11→1,02 | centro | |
| 145 | 4,833 | 0,67 | T04 | 1,85 | 1,10→1,22 | centro | |
| 165 | 5,500 | 0,50 | T02 | 1,45 | 1,16→1,30 | centro | Antecipação |
| **180** | **6,000** | 4,00 | T01 | 0,30 | 1,62→1,26 | 0,92 | **REVEAL** |
| 300 | 10,000 | 2,00 | T01 | 4,60 | 1,20→1,34 | 0,92 | Escala |
| 360 | 12,000 | 0,67 | T04 | 1,20 | 1,06→1,16 | centro | |
| 380 | 12,667 | 1,33 | T01 | 6,70 | 1,45→1,30 | 0,86 | |
| 420 | 14,000 | 0,67 | T03 | 0,30 | 1,04→1,12 | centro | |
| 440 | 14,667 | 1,33 | T01 | 8,10 | 1,28→1,44 | 0,94 | |
| 480 | 16,000 | 2,67 | T05 | 2,40 | 1,00→1,05 | centro | A fala dele |
| 560 | 18,667 | 2,67 | T01 | 9,55 | 1,00→1,04 | 0,88 | Fecho congelado |

Duração dos cortes do gancho: **1,50 → 1,33 → 1,17 → 0,83 → 0,67 → 0,50**.
Acelera de verdade, não por template.

## O reveal

Acontece no **quadro 180, em 6,000 s exatos**.

O corte é seco e o contraste é o efeito: sai de um close escuro e fumacento
(T02 apertado a 1,30) direto para o aberto a 1,62. O punch-out de 1,62 para
1,26 dá a sensação de a câmera abrindo, em quatro segundos de respiro.

A janela de corte vertical do T01 fica em `fy=0,92`. As churrasqueiras ocupam
de 55% a 78% da altura do quadro original; com a janela centrada, o reveal
virava céu e asfalto com uma faixa fina de churrasqueira no meio. Puxando para
baixo, a fileira ocupa o quadro.

## O impacto musical

Varri a faixa com janela de 5 ms e ranqueei cada ataque pelo produto entre a
força do transiente e a energia dos 2 s seguintes. O vencedor foi **70,605 s**,
ataque 0,586.

A música entra nesse ponto exato, colada no **quadro 180**, sem fade de
entrada, para o transiente chegar inteiro.

Medido no mix final:

| Janela | Nível |
|---|---|
| quadros 177–180 | −34,8 dB |
| quadros 180–183 | −8,4 dB |
| **salto** | **+26,4 dB** |

Antes disso, o ambiente mergulha de 1,00 para 0,30 entre 5,55 s e 5,97 s. É o
recuo que faz o impacto parecer maior do que ele é.

## Som

| Trecho | Ambiente | Voz tratada | Música |
|---|---|---|---|
| 0 – 5,55 s | 1,00 | — | 0 |
| 5,55 – 6,00 s | 1,00 → 0,30 | — | 0 |
| 6,000 s | 0,28 | — | **1,00, degrau seco** |
| 16,0 – 18,6 s | 0 | 1,00 | 0,07 |
| 18,7 – 21,3 s | 0,24 | — | 0,88 |

O ambiente cru é zerado onde a voz tratada entra, senão a fala somaria duas
vezes. A voz leva corte grave em 95 Hz, −3 dB em 200 Hz, +4 dB em 3,8 kHz,
de-esser, compressor 4:1 e excitador acima de 3,8 kHz. Mix a −14 LUFS, pico
−1 dBTP.

## Cor

Três grades, não uma:

- **GA, closes** — contraste 1,14, saturação 1,04, vibrance 0,22, `unsharp 5:5:0.55`
- **GB, o aberto** — contraste 1,16, saturação 1,09, vibrance 0,30, `colorbalance`
  quente, `unsharp 7:7:0.95`
- **GC, o pai** — saturação 1,00 e vibrance 0,16, para a pele não virar laranja

Todas passam por `selectivecolor` puxando magenta e amarelo **só nos vermelhos
e amarelos**, que é onde vive a brasa, e por uma curva em S suave. Saturação
global fica em 1,04 justamente para não virar comercial de IA: quem levanta a
brasa é o selectivecolor, não a saturação.

## Controle de qualidade

O preview saiu em 540x960 antes de qualquer render final. Nele encontrei e
corrigi:

1. Trabalhador de camisa azul no quadro em 5,0 s → entrada do T04 movida de
   0,05 para 1,85.
2. Antecipação fraca → trocada por T02 em 1,45 com punch de 1,16 para 1,30.
3. Punch-out do reveal terminando largo demais em 1,12 → parado em 1,26.
4. As três passadas pela fileira quase idênticas → zooms e janelas separados
   (1,20→1,34 em 0,92 / 1,45→1,30 em 0,86 / 1,28→1,44 em 0,94).

Varredura automática do render final a 5 amostras por segundo: **nenhum quadro
escuro ou mole** em 107 amostras.

## Saída

H.264 High 4.1, 1080x1920, 30 fps, CRF 20 com teto de 10 Mbit/s, GOP 60,
2 quadros B, `+faststart`. Áudio AAC 192 kbit/s a 48 kHz. 27,6 MB.

Fonte 4K → 1080 em passo único com lanczos. Não há recompressão em cadeia: os
clipes saem da fonte direto para CRF 15, e só o render final comprime para
entrega.

## Pendência

A legenda da fala do pai não foi feita. Não há reconhecimento de fala neste
ambiente. A fala foi posicionada e cortada por envelope de energia, na pausa
natural de 5,07 s do take, sem picar palavra.
