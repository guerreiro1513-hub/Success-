# A Escala — V3, passe de refinamento (20,9 s)

Base: `guerreiros-ESCALA-PAI-22s`. Mesmo conceito, mesma ordem até o reveal.
Refeito a partir dos brutos 4K para trocar a tipografia sem perder qualidade.
Receita: `projetos/escala/project/build_cut3.sh`, `mix3.py`, `mktx3.py`, `render3.sh`.

## O que mudou e por quê

| Ponto | V2 (PAI-22s) | V3 |
|---|---|---|
| Início | 0,6 s mortos antes da fala | Abre em 1,6 s de close da churrasqueira, a câmera vira para o pai |
| Legenda da fala | Não existia | Legenda completa, Montserrat ExtraBold, palavras-chave em amarelo, em y=1180 (fora da área da interface do Reels) |
| "ISSO AQUI É SÓ 1 DE 6" | Título em cima da fala | Removido: a própria fala diz isso e a legenda mostra "SEIS CHURRASQUEIRAS" |
| Títulos do reveal | Fonte genérica, um some e o outro entra | Montserrat ExtraBold, "6" em amarelo, as duas linhas empilhadas e segurando juntas |
| Final | T01 → T04 → T01 → T03 → T01 → T01 congelado: o mesmo travelling 4 vezes | Reveal → recorte da operação → vinheta da marca |
| Gancho | T04 T03 T02 T03 T04 T02: cada churrasqueira duas vezes | T04 → T03 → frango → carne em bloco: cada uma uma vez |
| Cor | unsharp 0,95 no aberto (serrilhava) | unsharp 0,62. Mais vibrance nos closes. Curva mais suave (não esmaga a sombra da grelha, segura o alto da brasa). T06 com grade leve própria (GN): ele já vem tratado pelo celular |
| Voz | Áudio cru | Grave cortado em 95 Hz, redução leve do ruído da feira, +3 dB em 3 kHz, compressor 3:1 |
| Reveal | Só a música | Sub de 48 Hz bem discreto no primeiro quadro do reveal |

## Linha do tempo final (30 fps, 626 quadros, 20,9 s)

Pedidos depois da primeira V3: abrir na churrasqueira e só então entrar o pai;
nenhuma churrasqueira aparecer duas vezes; vinheta da marca no fim.

| Quadro | Tempo | Dura | Take | Churrasqueira / papel |
|---|---|---|---|---|
| 0 | 0,000 | 10,30 | T05 0,00 | Abre na costela em ripas, a câmera vira e o pai fala |
| 309 | 10,300 | 1,33 | T04 1,00 | Peças vermelhas. **A música bate aqui** |
| 349 | 11,633 | 1,00 | T03 3,30 | Panceta dourada |
| 379 | 12,633 | 1,33 | T06 2,60 | Frango |
| 419 | 13,967 | 0,67 | T06 11,30 | Carne em bloco |
| 439 | 14,633 | 3,33 | T01 0,30 | **REVEAL**, as seis de uma vez |
| 539 | 17,967 | 1,33 | T01 6,30, zoom 1,80 | A operação: banner, fumaça, gente trabalhando |
| 579 | 19,300 | 1,57 | T07 | Vinheta da marca, intacta, + @GUERREIROSGRILL |

Saíram para não repetir churrasqueira nem carne:
- **T02**: tem a mesma peça dourada do T03, é a mesma churrasqueira.
- **Costela na fumaça do T06**: repete a costela da abertura.
- **Brasão desenhado**: a vinheta já traz o logo, dois logos seguidos seria repetição.

O corte da panceta termina em 4,30 s do take porque logo depois a câmera vira
para peças vermelhas parecidas com as do T04.

Todo corte depois da fala cai na grade de 90 BPM (20 quadros = 1 tempo).

## Legenda

Transcrição fornecida pelo cliente, grafia corrigida só no acento ("essa é"):

> Fala, gurizada! Essa é uma das seis churrasqueiras que temos no Florais.
> Vem pra cá, tem muita coisa boa. Um abraço, vem ser feliz!

Não há reconhecimento de fala no ambiente. Os tempos foram medidos no
espectrograma do take, sílaba por sílaba. Os blocos de duas linhas entram
linha a linha, então a segunda linha acompanha a fala mesmo onde a fronteira
exata entre palavras é incerta (trecho "tem muita coisa boa", falado rápido).

## Trilha

A trilha original não está no repositório. Ela foi recuperada do mix da V2
subtraindo a versão SEM-MUSICA, com ganho calculado por trecho. Cai
no corte que sai do pai (quadro 309) e desce junto com o escurecimento da vinheta.

## Medições

- Com música: −14,5 LUFS, pico −2,3 dBTP
- Sem música: −16,3 LUFS, pico −2,3 dBTP
- Nenhum quadro preto. 1080x1920, H.264 CRF 18, AAC 192k, `+faststart`

## Entrega

- `entrega/guerreiros-ESCALA-V3-FINAL-20s.mp4`
- `entrega/guerreiros-ESCALA-V3-FINAL-20s-SEM-MUSICA.mp4`

---

# V4 — ajustes de ritmo (21,5 s, 646 quadros)

Pedido: carnes mais tempo na tela, pai nos 3 primeiros segundos, legenda sem atraso.

| Quadro | Tempo | Dura | Take | Papel |
|---|---|---|---|---|
| 0 | 0,000 | 9,30 | T05 1,00 | 0,6 s de costela, a câmera vira. **O pai aparece em ~1,2 s** |
| 279 | 9,300 | 1,50 | T04 1,00 | Peças vermelhas. A música bate aqui |
| 324 | 10,800 | 1,00 | T03 3,30 | Panceta (não cresce: depois a câmera mostra peças iguais às do T04) |
| 354 | 11,800 | 2,00 | T06 2,40 | Frango |
| 414 | 13,800 | 1,50 | T06 11,15 | Carne em bloco |
| 459 | 15,300 | 3,33 | T01 0,30 | REVEAL |
| 559 | 18,633 | 1,33 | T01 6,30 | A operação |
| 599 | 19,967 | 1,57 | T07 | Vinheta |

As carnes somam 6,0 s, contra 4,3 s na versão anterior.

**Legenda:** cada frase entra 5 quadros (0,17 s) antes da voz e a animação caiu de
5 para 3 quadros. Entrando no mesmo quadro da sílaba, a legenda ainda estava
surgindo quando a palavra já tinha sido dita, e isso parece atraso.

Medido: com música −14,8 LUFS, sem música −16,8 LUFS, pico −2,1 dBTP.

Entrega: `entrega/guerreiros-ESCALA-V4-21s.mp4` e `-SEM-MUSICA`.

---

# V5 — carne fatiada e fundo musical na abertura (23,0 s, 691 quadros)

Pedido: usar um dos 5 vídeos novos (IMG_1452, 1454, 1455, 1460, 1475) antes da
cena das seis churrasqueiras, e música baixa por baixo da fala, com a fala mandando.

**Escolhido: IMG_1475 (T08), 1,60 a 3,10 s.** A carne pronta sendo fatiada na
tábua, com o miolo rosado. É o único plano de serviço do vídeo e não repete
churrasqueira. Os outros saíram: 1452 repete o rolete de peças vermelhas do T04;
1454 e 1455 são grelha aberta com o mesmo tipo de peça; 1460 é a tábua parada,
mais fraca que o 1475. Grade leve (GN): com a GA a tábua virava laranja.

| Quadro | Tempo | Dura | Take | Papel |
|---|---|---|---|---|
| 0 | 0,000 | 9,30 | T05 1,00 | Costela, a câmera vira, o pai fala. Fundo musical baixo |
| 279 | 9,300 | 1,50 | T04 | Peças vermelhas. Impacto da trilha |
| 324 | 10,800 | 1,00 | T03 | Panceta |
| 354 | 11,800 | 2,00 | T06 | Frango |
| 414 | 13,800 | 1,50 | T06 | Carne em bloco |
| 459 | 15,300 | 1,50 | T08 | **Carne sendo fatiada** |
| 504 | 16,800 | 3,33 | T01 | REVEAL |
| 604 | 20,133 | 1,33 | T01 | A operação |
| 644 | 21,467 | 1,57 | T07 | Vinheta |

## Fundo musical da abertura

Veio da mesma faixa, mas do trecho **anterior** ao impacto: a versão 25s
começava a trilha em 56,54 s da faixa, e o impacto das versões novas está em
70,605 s. Recuperado pela subtração 25s − 25s-SEM-MUSICA em janelas de 0,25 s.
A correlação com o trecho pós-impacto ficou abaixo de 0,17: é material
diferente, nada se repete.

- 8,2 s de fundo, entra em 1,1 s com fade de 1,2 s e termina no quadro do impacto.
- O trecho foi cortado numa batida e posicionado para que a grade de 90 BPM
  dele passe exatamente pelo impacto: o fundo desemboca na batida.
- 17 dB abaixo da voz, grave cortado em 150 Hz e −4 dB entre 1 e 4 kHz,
  a faixa da inteligibilidade da fala.
- A versão SEM-MUSICA não leva o fundo.

Medido: com música −15,0 LUFS, pico −3,5 dBTP. Sem música −17,4 LUFS, pico −4,1 dBTP.

Entrega: `entrega/guerreiros-ESCALA-V5-23s.mp4` e `-SEM-MUSICA`.

---

# V6 — sem a carne fatiada e sem o zoom da operação (20,2 s, 606 quadros)

Pedido: tirar o IMG_1475 (carne fatiada) e o recorte em zoom da operação.
O reveal agora vai direto para a vinheta. O fundo musical da abertura continua.

| Quadro | Tempo | Dura | Take | Papel |
|---|---|---|---|---|
| 0 | 0,000 | 9,30 | T05 1,00 | Costela, a câmera vira, o pai fala. Fundo musical baixo |
| 279 | 9,300 | 1,50 | T04 | Peças vermelhas. Impacto da trilha |
| 324 | 10,800 | 1,00 | T03 | Panceta |
| 354 | 11,800 | 2,00 | T06 | Frango |
| 414 | 13,800 | 1,50 | T06 | Carne em bloco |
| 459 | 15,300 | 3,33 | T01 | REVEAL |
| 559 | 18,633 | 1,57 | T07 | Vinheta |

Medido: com música −15,0 LUFS, pico −3,5 dBTP. Sem música −16,9 LUFS, pico −4,1 dBTP.

Entrega: `entrega/guerreiros-ESCALA-V6-20s.mp4` e `-SEM-MUSICA`.

**Correção da carne em bloco:** o IMG do T06 tem marcação de tempo irregular
perto de 11 s. O filtro `fps=30` duplicava um quadro e pulava outro a cada três
(16 quadros quase repetidos em 44), e isso travava a imagem. Nos clipes do T06
cada quadro da fonte agora vira um quadro da saída (`setpts=N/(30*TB)`). O corte
também recuou para 11,00 s, para não pegar o salto de câmera que existe em 12,52 s.

---

# V7 — mais churrasqueira (24,9 s, 746 quadros)

Pedido: o trecho das churrasqueiras estava curto. Entraram IMG_1448 (T11),
IMG_1454 (T10) e IMG_1452 (T09), intercalados com os cortes que já existiam.

| Quadro | Tempo | Dura | Take | Carne |
|---|---|---|---|---|
| 0 | 0,000 | 9,30 | T05 1,00 | Pai falando, fundo musical baixo |
| 279 | 9,300 | 1,50 | T04 | Peças vermelhas. Impacto da trilha |
| 324 | 10,800 | 1,00 | T03 | Panceta |
| 354 | 11,800 | 1,33 | **T11 0,20** | Cesto de peças grandes |
| 394 | 13,133 | 2,00 | T06 | Frango |
| 454 | 15,133 | 1,50 | **T10 0,60** | Grelha, peças no espeto (grade leve GN) |
| 499 | 16,633 | 1,50 | T06 | Carne em bloco |
| 544 | 18,133 | 1,83 | **T09 3,60** | Grade de carne com o céu |
| 599 | 19,967 | 3,33 | T01 | REVEAL, na cabeça do 4º compasso após o impacto |
| 699 | 23,300 | 1,57 | T07 | Vinheta |

As carnes somam 10,7 s, contra 6,0 s na V6. Nenhum clipe novo tem quadro repetido.

**Trilha:** o gancho passou do comprimento da trilha recuperada. O 2º compasso
depois do impacto (4 batidas) toca duas vezes, emendado na batida com
cruzamento de 10 ms.

Medido: com música −14,9 LUFS, pico −3,5 dBTP. Sem música −17,5 LUFS, pico −4,1 dBTP.

Entrega: `entrega/guerreiros-ESCALA-V7-25s.mp4` e `-SEM-MUSICA`.
