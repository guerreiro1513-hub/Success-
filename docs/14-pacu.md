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
