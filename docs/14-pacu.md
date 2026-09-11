# GUERREIRO'S GRILL — anúncio do PACU (20,4 s)

`entrega/guerreiros-PACU-20s.mp4` — 1080×1920 · 9:16 (SAR 1:1) · H.264 · 30 fps · AAC · 20,40 s · 21 MB

Exportado a 8,2 Mbps (CRF 22, preset slow). O primeiro export saiu com 32 MB e
estourava o limite de 30 MB do envio; o Instagram recomprime de qualquer forma.

## O material e a decisão central
Os três vídeos são a **mesma cena à noite**, sob luz amarela forte. As **duas fotos**
são de longe o melhor material: nítidas, o peixe glaceado, luz neutra, 1450×2576
(exatamente 9:16, escala sem corte).

Então: **as fotos carregam o gancho, a revelação e o tamanho**; os vídeos carregam o
movimento, a faca e a cena de gente servindo — que é o que vende "serve até 8".

| Fonte | Papel | Planos |
|---|---|---|
| FOTO A | macro do gancho (curiosidade) | 2 |
| FOTO B | revelação, tamanho, fecho | 3 |
| P1 / P2 / P3 | servir, cortar, gente em volta | 11 |
| Florais (F1/F3/F4) | o churrasco de sempre | 6 |

## Correção de cor — o problema mais sério
A luz de sódio da noite deixou os vídeos com **R/B de 2,90 a 3,46**. As fotos estão
em 1,52–1,59. Sem corrigir, o peixe fica amarelo doentio e o corte não fecha com o
material do churrasco.

Levantei muito o azul e puxei o vermelho:

| | antes | depois |
|---|---|---|
| P1 | 3,46 | **2,15** |
| P2 | 2,90 | **1,80** |
| P3 | 3,34 | **2,02** |
| fotos | 1,52–1,59 | 1,67–1,88 |
| Florais | — | 1,75 |

O vídeo inteiro agora fecha na mesma faixa.

## Estrutura (22 planos, tudo na grade de 100 BPM)
| Tempo | Bloco | Texto |
|---|---|---|
| 0,0–2,1 | macro na pele marcada — não dá pra saber o que é | **TEM NOVIDADE** |
| 2,1–5,1 | revelação do peixe inteiro | **AGORA TEM / PACU** |
| 5,1–8,1 | montagem: faca, servir, textura | — |
| 8,1–11,1 | o peixe com a galera em volta | **AOS SÁBADOS / E DOMINGOS** |
| 11,1–13,5 | peixe inteiro, plano aberto | **SERVE ATÉ / 8 PESSOAS** |
| 13,5–17,1 | frango no rolete, costela, fogo, carne | — |
| 17,1–18,6 | volta pro pacu | **MAIS UMA OPÇÃO PRO / SEU FIM DE SEMANA** |
| 18,6–20,4 | foto herói + marca | brasão · SÁB E DOM · @guerreirosgrill |

Tipografia com a mesma animação do reel do Florais: linha de apoio revela em wipe,
linha de impacto entra em overshoot saindo de desfoque, régua vermelha desenha.
Nenhuma informação aparece junto com outra.

## Áudio
Nenhuma trilha foi fornecida; nada baixado de fonte não oficial. Som natural:
áudio sincronizado plano a plano (faca, gente, grelha) sobre três camas de ambiente
— noite para a parte do pacu, grelha diurna para o churrasco, noite de novo no fecho.
Os planos de foto entram em silêncio e só a cama sustenta, o que dá um respiro
antes da revelação. Média −16,3 dB, pico −0,6 dB.

Cortes todos em múltiplos de 9 frames (meio tempo a 100 BPM) — dá pra jogar um áudio
em alta por cima sem reeditar.

## Sem exagero
Só o que sabemos: Pacu · sábados e domingos · serve até 8 pessoas.
Nenhuma alegação de "melhor", "maior" ou "imperdível".

## Controle de qualidade
612 frames: 0 frames pretos, 0 moles, 0 saltos de exposição fora de corte.
Brilho 61,7–107,1. Tinta do texto x=118..962, base y=1575 (zona segura do Reels).
SAR forçado para 1:1 — as fotos são 1450×2576 e geravam pixel não-quadrado.

---

# Revisão 1 — texto por letra, foto em movimento, variedade com o Video A

## 1. Tipografia — animação por letra
A referência que você mandou é um tutorial de presets de texto do CapCut
("Letras Aleatórias", "Subida aleatória", "Crescer", "Estremecer"). O que eu tinha
animava a **linha inteira**; agora cada **letra** anima sozinha.

Motor novo (`mkpktext2.py`), por caractere:
- **entrada em cascata** — cada letra entra com atraso de 2 frames em relação à anterior
- **letras aleatórias** — nos primeiros ~5 frames a letra mostra um caractere sorteado
  antes de assentar no certo ("RH" → "PACU")
- **subida com overshoot** — sobe 38 px e escala 1,55 → 1,00 com ease out-back
- **jitter horizontal** por letra (±9 px) que assenta em zero, com semente fixa
  (determinístico entre frames, não treme sozinho)
- **rastro fantasma** — duas cópias acima em 22% e 10% de alfa durante a entrada
- **saída em cascata invertida** — as letras caem e somem da última para a primeira

## 2. As fotos agora têm gesto, e entregam pro vídeo
Como você sugeriu: a foto **entra em zoom in**, e **na hora do texto dá o zoom out
e corta pro vídeo**.

| Plano | Movimento |
|---|---|
| 0,0–1,2 s | foto, escala 1,05 → 2,25 (**zoom in**) |
| 2,1–3,6 s | foto, escala 2,25 → 1,02 (**zoom out**) — assenta exatamente quando "PACU" para de embaralhar |
| 3,6 s | **corta pro vídeo** |

É um gesto só atravessando o corte. As outras duas aparições de foto viraram vídeo:
o plano do "SERVE ATÉ 8 PESSOAS" agora é o P2 com o peixe inteiro **e a galera em
volta**, que sustenta melhor a mensagem do que uma foto parada.

Sobraram 3 momentos de foto (era 5): abre, revela e fecha.

## 3. Variedade com o Video A
O bloco do churrasco agora é liderado pelo Video A (1080×1920 nativo, o de maior
resolução do acervo):

| Tempo | Plano |
|---|---|
| 13,5 | frango dourado, close |
| 14,1 | braço levantando a costela contra o céu |
| 14,7 | costela com bacon no espeto |
| 15,3 | fogo na brasa (Florais) |
| 15,9 | frangos na grelha com a rua atrás |
| 16,5 | carne na tábua (Florais) |

## Controle de qualidade
612 frames, 0 frames pretos, 0 moles, 0 saltos de exposição fora de corte.
Tinta do texto x=148..932, base y=1562. SAR 1:1. 22 MB.

---

# Revisão 2 — trilha, saturação e fim das fotos

## Fotos removidas
Os 22 planos agora são **só vídeo**. Os quatro que eram foto viraram:
gancho `P1@12,55` com zoom in 1,30→2,05 · revelação `P2@6,80` com zoom out 2,00→1,02
(assenta no "PACU") · tamanho `P3@17,10` · fecho `P1@17,50`.

## Trilha — original, feita aqui
Você pediu música viral. **Não tenho como usar uma faixa viral licenciada**, e não
vou baixar de fonte não oficial. O que fiz foi **sintetizar uma trilha original**
(`entrega/trilha-original-100bpm.wav`, gerada em `mkbeat.py`): 100 BPM, lá menor,
progressão Am–F–C–G, com kick, sub, clap, hi-hats, pluck e riser.

Ela é construída em cima da **mesma grade dos cortes**: drop em 2,1 s (onde entra a
revelação) e lift em 13,5 s (onde vira pro churrasco). Como todos os cortes já estão
em múltiplos de 9 frames a 100 BPM, se você trocar por um áudio em alta do Instagram
os cortes continuam batendo.

Mixagem: trilha na frente, som natural (faca, gente, grelha) a 0,42 por baixo como
textura. Média −16,6 dB, pico −0,3 dB.

## Saturação — e o erro que eu cometi no caminho
Primeira tentativa: saturação 1,32 + bloom nas altas. **Ficou roxo.** Medi e o desvio
magenta foi a **+37,9** (o grau anterior estava em −4,3).

Investiguei e a culpa **não era da saturação, era do bloom**: o brilho que eu somava
nas altas desequilibrava o verde. Tirei o bloom e busquei a mesma riqueza por **curva
em S** (que não mexe em matiz) mais unsharp mais forte, e compensei o azul de 0,735
para 0,830.

| | magenta | saturação | R/B |
|---|---|---|---|
| entregue antes | −4,3 | 92 | 1,66 |
| tentativa com bloom | **+37,9** ❌ | 160 | 1,55 |
| **agora** | **−0,4** ✅ | **153** | 1,97 |

Saturação subiu 66% sem nenhum desvio de cor.

## Controle de qualidade
610 frames, 0 pretos, 0 moles, 0 saltos de exposição fora de corte.
Brilho 42,3–104,0. SAR 1:1. 22 MB.

---

# Revisão 3 — texto legível, trilha gaúcha

## O texto estava "escrevendo errado"
Era o efeito de **letras aleatórias** que eu tinha posto (o preset "Letras
Aleatórias" da referência): nos primeiros frames cada letra mostrava um caractere
sorteado antes de assentar. Numa peça com informação real — data, "serve até 8
pessoas" — isso lê como **erro de digitação**, não como efeito. Removido.

Ficou a entrada em cascata por letra, que é o que dá vida sem comprometer a leitura.
E tudo mais devagar:

| | antes | agora |
|---|---|---|
| atraso entre letras | 2,0 frames | 2,6 |
| entrada | 13 frames | 16 |
| saída | 12 frames | 18 |

Tempo de leitura de cada mensagem:

| Mensagem | antes | agora |
|---|---|---|
| TEM NOVIDADE | 1,80 s | 1,90 s |
| AGORA TEM / PACU | 2,80 s | **3,43 s** |
| AOS SÁBADOS / E DOMINGOS | 2,80 s | **3,20 s** |
| SERVE ATÉ / 8 PESSOAS | 2,20 s | **2,60 s** |
| MAIS UMA OPÇÃO / FIM DE SEMANA | 2,10 s | **2,40 s** |

## Trilha gaúcha
`entrega/trilha-gaucha-100bpm.wav` — sintetizada aqui (`mkgaucha.py`), original.
Sol maior, progressão G–D–Em–C, baixo em oom-pah (baixo no 1 e 3, acorde no 2 e 4),
acordeão com vibrato de 5,2 Hz, rim e vassourinha.

Começa baixa e **sobe 3,7 dB quando entra o churrasco**, como você pediu:

| Trecho | Nível |
|---|---|
| 0–2 s intro | −24,7 dB |
| 2–13,5 s pacu | −21,0 dB |
| 13,5–20,4 s **churrasco** | **−17,3 dB** |

Continua a 100 BPM, na mesma grade dos cortes.

## Falta a narração
O áudio da voz do pai dele ainda não chegou. A mixagem já está montada para receber:
é só somar a faixa de voz e abaixar a trilha por baixo dela.

---

# Revisão 4 — narração do pai e informação real do produto

## A informação veio do card
O primeiro vídeo é o card oficial do Guerreiro's Grill. Li a informação direto dos
frames — é bem mais específica do que eu tinha:

**PACU ASSADO RECHEADO · DE 2,2 KG · FAROFA + TOMATE + CEBOLA · SÁBADO E DOMINGO ·
aceita encomenda**

O texto na tela agora carrega isso:

| Tempo | Mensagem |
|---|---|
| 0,3–2,2 | TEM NOVIDADE |
| 2,4–5,8 | AGORA TEM · **PACU** |
| 6,2–9,4 | ASSADO E · **RECHEADO** |
| 9,7–12,9 | PACU DE · **2,2 KG** |
| 13,3–15,9 | FAROFA, TOMATE E CEBOLA · **SÁBADO E DOMINGO** |
| 16,2–18,6 | MAIS UMA OPÇÃO PRO · **SEU FIM DE SEMANA** |

## Narração
A voz do pai (19,78 s) entra por cima dos 20,40 s de vídeo — encaixe quase exato.
Limpei com filtro passa-alta em 95 Hz, redução de ruído e compressor 3:1.

Mixagem em três estágios:

| Trecho | Trilha | Por quê |
|---|---|---|
| 0–13,5 s | 0,26 | por baixo da narração |
| 13,5–17,9 s | 0,46 | sobe no churrasco, mas ainda sob a voz |
| 17,9–20,4 s | 0,95 | a fala acaba, a trilha abre |

Média −15,2 dB, pico −1,0 dB.

## Limitação declarada
**Não consigo transcrever áudio** — não há reconhecimento de fala neste ambiente.
Consigo medir o envelope da fala (detectei 6 grupos de energia), mas não sei as
palavras. Por isso o texto na tela está ancorado nos **blocos do produto**, não
sincronizado com as frases dele.

Se o texto do que ele fala for enviado por escrito, dá para fazer a legenda palavra
por palavra da referência #3.

## Referências recebidas
- #2 (3435102c): tutorial de **texto atrás do sujeito** — mesmo efeito já feito no
  reel do Florais, com recorte por GrabCut.
- #3 (714e565b): **legenda palavra a palavra** sincronizada com a fala.
- #4 (a935f483): reenvio do material de churrasco (md5 diferente, mesmo conteúdo,
  14,38 s / 720×1280 / 60 fps) — já está no acervo.

---

# Revisão 5 — quatro correções

## 1. Legendas cortadas ("SEMAN", "GR") — bug meu
Quando desacelerei o texto na revisão 3 (2,0 → 2,6 frames por letra), quebrei as
frases longas: o atraso era **fixo por letra**, então quanto mais letras, mais tempo
para entrar — e o bloco acabava antes.

Medido: **4 das 7 linhas nunca terminavam de aparecer.**

| Linha | letras | precisava | tinha |
|---|---|---|---|
| PACU | 4 | 23,8 fr | 103 fr (44 sobrando) |
| SEU FIM DE SEMANA | 17 | 57,6 fr | 72 fr (**faltavam 21**) |
| SÁBADO E DOMINGO | 16 | 55,0 fr | 80 fr (**faltavam 10**) |
| @GUERREIROSGRILL | 16 | 25,5 fr | 14 fr (**faltavam 11**) |

Agora o atraso é **adaptativo**: um orçamento fixo de entrada dividido pelo número de
letras. Toda linha entra na mesma janela, tenha 4 ou 27 caracteres. O build testa
isso antes de renderizar e falha se alguma não couber.

Tempo parado na tela, já verificado: 1,63 s / 1,33 s / 1,23 s / 1,63 s / 1,20 s.

## 2. O zoom da abertura não estava no peixe
O corte era **centralizado**. Só que nesses planos o peixe ocupa a faixa de 35% a 70%
da altura e **acima dele só tem pernas e rua** — então o zoom ampliava justamente as
pessoas.

Reescrevi o recorte para mirar um ponto: passo a posição do peixe (px, py) e o script
calcula o deslocamento do crop. Os 16 planos do pacu agora enquadram o peixe e a
tábua, sem transeuntes.

## 3. Texto no plano errado
"FAROFA, TOMATE E CEBOLA / SÁBADO E DOMINGO" caía em f398–478, e o bloco do churrasco
começa em f405 — a informação do peixe aparecia **em cima da costela com bacon**.

Agora cada mensagem está presa à sua seção:

| Mensagem | Frames | Sobre |
|---|---|---|
| TEM NOVIDADE | 6–96 | peixe |
| AGORA TEM · PACU | 102–192 | peixe |
| ASSADO E · RECHEADO | 198–290 | peixe |
| COM FAROFA, TOMATE E CEBOLA · 2,2 KG | 296–400 | peixe (acaba antes de f405) |
| E TEM MAIS · O CHURRASCO DE SEMPRE | 417–508 | churrasco |
| brasão · SÁBADO E DOMINGO · @guerreirosgrill | 552–612 | peixe |

## 4. Sem pessoas
Todos os enquadramentos do pacu foram refeitos com o alvo no peixe.

## Revisão 6 — desfoque graduado no fundo (entregue)

Pedido: *"não quero pessoas áreas, foca só no peixe"*.

Não dá para apagar as pessoas do vídeo original, mas dá para tirá-las de foco.
Foi criada uma máscara vertical (`mask_top.png`): desfoque total até 13% da
altura, transição, e nitidez total a partir de 37%. Ela entra num `maskedmerge`
entre a imagem nítida e uma cópia desfocada, então o topo do quadro (chão,
pernas, gente passando) vira fundo e o peixe fica sendo a única coisa em foco.

Arquivo: `entrega/guerreiros-PACU-20s.mp4` — 20,40 s, 1080x1920, 30 fps, 22,2 MB.

## Revisão 7 — peixe girando no preto (em andamento)

Pedido: *"colocar só a tábua e o peixe num ambiente todo preto com ele girando"*,
igual ao TikTok de referência (@stevenwommack): foto do produto → Nano Banana Pro
→ Kling image-to-video → produto flutuando e girando.

### Tentativa local (descartada)
Recortei a tábua da foto `ce0c183a` com um polígono (`iso2.py`) e montei um
"turntable" falso por homografia (`turn.py`): rotação de ±11° em torno do eixo
vertical, brilho especular varrendo, sombra de contato, vinheta.

Não funciona. A tábua sai do enquadramento da foto original em baixo e à
esquerda, então a silhueta recortada tem bordas retas. Ao girar, essas bordas
aparecem e a coisa lê como uma *fotografia girando*, não como um objeto
flutuando. Fica registrado como beco sem saída.

### Caminho por IA (o certo)
Duas imagens geradas no Nano Banana Pro, 9:16, 2K, 6 créditos cada:

| Take | generation_id | Resultado |
|---|---|---|
| 1 | `6aa28e42f1cceba1ca3d9a4b` | Iluminação e fundo ótimos, mas o modelo inventou outro peixe (corpo comprido tipo carpa). Descartado: anunciar com peixe que não é o nosso é propaganda enganosa. |
| 2 | `6aa28ff85999e91302a5349c` | Fiel. Corpo alto e arredondado, focinho curto, olho grande, cabeça escura, cortes verticais profundos com a carne dourada. Tábua de madeira, preto absoluto. |

O que fez diferença no take 2 foi descrever a *forma* do pacu no prompt, não só
pedir "peixe assado".

### Bloqueio de rede
`cdn.kairogen.ai` está barrado pela política de saída deste ambiente
(CONNECT 403). As imagens e vídeos ficam na CDN e não descem para cá, então o
plano de fundo (Kling v3.0 Pro, 23 créditos, 5 s) roda no servidor mas o arquivo
precisa ser baixado pelo Emilio e reenviado para entrar na montagem.

Créditos: 620 restantes.

### Giro gerado (Kling V3.0 Pro, 1080p, 5 s, 9:16, sem áudio)

O prompt do tutorial aparece na tela do vídeo de referência:
*"ultra realistic floating 3D ad of this matcha latte drink, add some elements
related to the product like, ice cubes."* Repeti a fórmula com o pacu.

| Versão | Imagem base | Vídeo |
|---|---|---|
| Elementos flutuando | `6aa295c7936cd074743577d3` | `6aa2962e5999e91302a549a7` |
| Giro limpo | `6aa28ff85999e91302a5349c` | `6aa2959ff1cceba1ca3db317` |

Na versão com elementos, orbitam em volta do peixe: farofa, tomate em cubos,
cebola picada, salsinha, sal grosso, brasas e um fio de fumaça. É a que casa com
a referência.

Custo: 2 imagens x 6 + 2 vídeos x 23 = 58 créditos. Restam 568.

Os arquivos ficam na CDN da Kairogen, que está bloqueada pela política de saída
deste ambiente, então a montagem depende do Emilio baixar e reenviar.

### Versão final do giro — 4K, 10 s

Pedido: *"eu quero o melhor vídeo possível"*.

`generation_id` `6aa298931c568e82b1fcbaff`, Kling V3.0 Pro, 4K, 10 s, 9:16,
sem áudio, 202 créditos. Restam 366.

Por que 4K e 10 s: o reel sai em 1080, mas partir de 4K permite recortar e
aproximar sem perder nitidez e a redução para 1080 fica mais limpa. Com 10 s dá
para escolher os 3,6 s de melhor giro em vez de aceitar o que veio.

O prompt trava tomada única, sem corte, câmera fixa, velocidade constante, e
proíbe explicitamente o peixe de ganhar vida, que é o artefato clássico desses
modelos com animal.

### Montagem pronta para quando o arquivo chegar

`rot_swap.sh` troca os 108 primeiros quadros (3,60 s = k01+k02+k03) pelo giro,
em três movimentos: 36 quadros de aproximação lenta, 27 de sustentação, 45 de
afastamento. Como o total de quadros não muda, a linha do tempo dos textos e a
mixagem de áudio continuam idênticas. Uso: `bash rot_swap.sh <arquivo.mp4>`.

## Revisão 8 — abertura com o peixe girando (entregue)

O giro chegou pelas mãos do Emilio: o arquivo do Kairogen não descia para este
ambiente (CDN bloqueada, e o botão de download do celular só devolvia a página
de verificação do Vercel com 32 KB). Ele exportou pelo CapCut e mandou aqui.

Arquivo recebido: 10,07 s, 1074x1920, HEVC, 30 fps, 11,3 Mbps, 14 MB.

Os 108 primeiros quadros do anúncio (3,60 s) passam a ser o giro, em **uma
tomada só**. Antes eram três cortes (k01, k02, k03). Como o giro já tem
movimento próprio, cortar ali só atrapalhava, então os três blocos recebem
pedaços contínuos do mesmo clipe com um único push-in de 1,020 a 1,240 sem
reset entre eles. A contagem de quadros não muda, então os textos e a mixagem
continuam nos mesmos lugares.

O "TEM NOVIDADE" agora entra sobre o peixe flutuando no preto, e aos 3,60 s o
corte entrega o produto real com "AGORA TEM PACU".

Arquivo: `entrega/guerreiros-PACU-20s.mp4` — 20,40 s, 1080x1920, 30 fps,
yuv420p, 21,5 MB.

### Sobre 4K
Não dá. O 4K original ficou na CDN. O arquivo que chegou é 1074x1920, já
reencodado pelo CapCut, e ampliar isso para 3840 só interpola, não devolve
detalhe. O reel do Instagram e do TikTok é entregue em 1080x1920 de qualquer
jeito, então a entrega sai na resolução nativa.

## Revisão 9 — cor dos clipes reais do peixe

Reclamação: *"tá uma merda a cena do pacu"*, falando dos vídeos que ele mandou
primeiro, não do giro.

Medi o original. A luz da noite era laranja-sódio pesada:

| Faixa | R | G | B | amarelo |
|---|---|---|---|---|
| sombra | 37 | 34 | 21 | +14 |
| meio | 144 | 97 | 30 | +91 |
| alta | 214 | 175 | 85 | +110 |

A correção antiga só mexia nos médios (`b` 0,5→0,830 com a curva voltando a
1/1 no branco), então a carne clara, que vive no topo da faixa, continuava
amarelo-mostarda.

A nova levanta o azul na faixa toda e **segura o verde** em vez de levantá-lo.
Levantar o verde junto com o azul aproximava R de G e dava aquele amarelo-limão.
Segurando o verde, sobra separação entre vermelho e verde (+42 nas altas) e o
peixe lê dourado. Saturação caiu de 1,22 para 0,98, porque com o desvio de cor
corrigido a 1,22 voltava a estourar o amarelo.

Entrou também `hqdn3d=4:3:6:4.5` antes das curvas. O levante de azul nas
sombras multiplica por quase 4 o ruído daquele canal, e sem o denoise a tábua
ficava suja de ruído colorido.

O desfoque de fundo passou a usar `mask_top2.png`, a versão rasa: desfoque
total só até 5% da altura e nitidez total a partir de 15,5%. A anterior pegava
o peixe, que começa por volta de 19% do quadro.

## Revisão 10 — reenquadramento do giro

O giro estava com o peixe pequeno no alto e um terço do quadro preto e morto
embaixo, e a legenda caía em cima da tábua.

Novo enquadramento: 2,80 s do clipe esticados para 3,60 s, ampliação de 1,12 e
recorte deslocado para cima (`crop=1080:1920:65:192` sobre 1210x2150). O peixe
passa a ocupar de 11% a 67% da altura, então a faixa da legenda, que começa por
volta de 70%, fica limpa. A janela de 2,80 s é o trecho em que o rabo ainda não
encosta na borda direita do quadro original.

Arquivo: `entrega/guerreiros-PACU-20s.mp4` — 20,40 s, 1080x1920, 21,3 MB.

## Revisão 11 — narração do pai (entregue)

Gravação recebida: 24,54 s, 9 frases, 18,26 s de fala e 5,18 s de pausa.

Ele improvisou, então o texto não bate frase a frase com o roteiro. Não há
reconhecimento de fala neste ambiente, então o encaixe não pode ser feito por
palavra. O que dá para medir é energia, e é por aí que o corte foi feito.

### Encaixe
As 9 frases foram detectadas por envelope de energia (janela de 20 ms, limiar a
34% entre o piso e o pico). As **pausas** foram reduzidas à metade e a fala foi
mantida intacta. Isso levou os 23,44 s originais para 20,91 s. Depois,
`atempo=1,056` fecha em 19,80 s, que é o espaço entre 0,35 s e 20,15 s do
anúncio. Os 5,6% de aceleração não mudam o timbre e dão um pouco mais de
energia à leitura, que é o que um anúncio pede.

Onde cada frase caiu:

| Frase | Na gravação dele | No anúncio |
|---|---|---|
| 1 | 0,00 – 3,72 | 0,35 – 3,99 |
| 2 | 4,32 – 8,12 | 4,16 – 7,87 |
| 3 | 9,00 – 10,24 | 8,17 – 9,46 |
| 4 | 10,76 – 12,84 | 9,59 – 11,67 |
| 5 | 13,34 – 15,90 | 11,80 – 14,34 |
| 6 | 16,50 – 17,16 | 14,51 – 15,25 |
| 7 | 17,50 – 18,38 | 15,29 – 16,24 |
| 8 | 19,52 – 22,02 | 16,67 – 19,15 |
| 9 | 22,62 – 23,44 | 19,32 – 20,21 |

### Tratamento da voz
Corte grave em 85 Hz, redução de ruído, de-esser, −2 dB em 180 Hz para tirar o
abafado do peito, +2,5 dB em 2,6 kHz para a dicção, compressor 3:1 e
normalização a −15 LUFS.

### Mixagem
A trilha gaúcha entra a 0,42 e sobe para 0,72 a partir de 13,5 s. Ela é abaixada
automaticamente pela voz com `sidechaincompress` (limiar 0,035, razão 9, ataque
10 ms, soltura 320 ms), então a música cai sozinha quando ele fala e volta nas
respiradas e no fim. O mix fecha em −14 LUFS com limitador em −1 dBTP.

Medido: o mix inteiro fica só 1,3 a 2,5 dB acima da voz sozinha, ou seja, a voz
manda no áudio.

Arquivos: `entrega/guerreiros-PACU-20s.mp4` e `entrega/mix-pacu-com-narracao.wav`.

## Revisão 12 — trilha só na carne, voz com presença

Reclamações: a trilha rodando por trás o tempo todo soava estranha, o gaúcho
tinha que entrar quando começa a carne, e a voz estava sem graça.

### Trilha (`mkgaucha2.py`)
Duas seções em vez de um loop contínuo:

- **0 a 13,90 s** — só um bordão grave em Sol (49 Hz + 98 Hz + 196 Hz) a 0,055
  de amplitude e uma nota de baixo a cada 2,4 s. Praticamente inaudível. A
  primeira metade do anúncio passa a ser a voz e o som do churrasco.
- **13,90 s em diante** — vanerão de verdade: baixo em oom-pah, acordeão nos
  contratempos, melodia por cima, aro e vassoura marcando. Entra com uma
  vassourada 0,62 s antes do corte, para a banda chegar junto com a carne.

O oom-pah anda em 200 BPM (0,30 s por tempo) sobre a grade de corte de 100 BPM.
Dobrar o tempo dá energia de vanerão sem sair do compasso dos cortes.

O acordeão foi refeito com **três palhetas por nota**, desafinadas em ±7 cents.
O batimento entre elas é o som de musette. A versão anterior empilhava harmônicos
de um oscilador só e por isso soava a órgão, que era a "música estranha".

### Voz
As pausas foram cortadas a 62% em vez de 50%, o que deixou espaço para acelerar
8,75% em vez de 5,6%. Fala mais rápida, pausa mais viva.

Cadeia: −3 dB em 200 Hz, +1,5 dB em 900 Hz, **+4 dB em 3,8 kHz** para a presença,
+2,5 dB de brilho acima de 9 kHz, de-esser, compressor 4:1, `aexciter` gerando
harmônicos acima de 3,8 kHz, um segundo compressor suave, e um eco curtíssimo de
26 ms a 11% para tirar o som de gravação seca de celular. Fecha em −13,5 LUFS.

### Medição
Até 13 s o mix fica 0,5 a 0,7 dB acima da voz sozinha, ou seja, não há música
audível competindo. De 14 s em diante sobe para 1,4 a 2,6 dB, que é a banda
entrando e crescendo até o fim.

## Revisão 13 — música do Emilio na parte da carne

Ele mandou uma música de referência e pediu para tirar a voz do pai quando
começa a carne e pôr a música no lugar.

- Voz: nível cheio até 13,60 s, esvanece em 0,30 s e fica muda de 13,90 s até o
  fim.
- Bordão grave: some em 13,40 s.
- Música dele: entra em 13,55 s com 0,35 s de abertura, cheia a partir de 14,0 s,
  fecha com 0,45 s de saída no fim.

O trecho usado começa em **64,54 s** da gravação dele. Medi o andamento por
autocorrelação do envelope de ataques: **90 BPM**, tempo de 0,667 s, e os
ataques em 56,54 / 57,21 / 57,87 / 58,55 confirmam. 64,54 é uma cabeça de
compasso contada a partir dali, e cai dentro do trecho de maior energia da
música, entre 60 e 72 s.

Os cortes da carne andam em 100 BPM, 18 quadros por clipe. A música anda em 90.
Não estiquei para encaixar: os 11% de aceleração que fariam bater são audíveis
numa música cantada, e são só 6,5 s de vídeo. Se ele quiser travado, dá para
recortar aqueles clipes para 20 quadros, mas isso mexe na linha do tempo dos
textos.
