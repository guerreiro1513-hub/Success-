# Tour 3 unidades — reel cinematográfico (em andamento)

Sistema reutilizável em `projetos/tour3/`: `timeline.json` (ordem, clipes, cortes,
velocidades, cor por clipe, transições, textos, encerramento) + `render.py`
(`--preview` = 540x960; sem flag = final 1080x1920, 30 fps, H.264 + AAC). Gera
também `<saida>.cortes.json` com os tempos dos cortes (para sincronizar a música).

## Referências
- REF1 (`referencias/REF1_abertura_aerea.mp4`, GTA): mapa visto de cima, 3–4 saltos
  de zoom (cada nível segura ~1 s), depois a câmera inclina até o nível da rua. Só a
  mecânica será usada, com imagem real (gravação do Google Earth) — nada do jogo.
- REF2 (`referencias/REF2_efeito_fachada.mp4`): NÃO é um vídeo de cortes rápidos; é um
  tutorial de "efeito fachada" (logo 3D aplicado na fachada com a câmera andando),
  0–4 s de resultado e o resto tela de celular. A linguagem de transições (whip,
  rampa de velocidade, desfoque direcional) foi feita a partir do texto do briefing.

## Tropical Ville (4 clipes, iPhone 4K/60p, ~2,6 s cada)
| Arquivo | Conteúdo | Movimento (imagem na tela) | Nota |
|---|---|---|---|
| C128a fachada | fachada, árvore, churrasqueira, placa "frango no rolete" | avança (zoom +4%/0,25 s), sobe e vai pra direita no fim | céu lilás (export já tratado, 3066x2158) — corrigido |
| C128b frangos | grelha de frangos | avança no começo, depois abre forte pra esquerda-baixo (whip natural) | melhor clipe para transição |
| C130 grelha | grelha giratória de perto | imagem desce (câmera sobe), leve recuo | escura (luz 65) — clareada |
| C122 costela | costela no giro, fumaça | imagem corre pra direita, avança no fim | mais macia (fumaça) |

Sequência: fachada (título) → zoom para dentro da churrasqueira → frangos (rampa
2x no meio) → whip 150° → grelha (câmera lenta 0,6x e acelera 3x) → whip 55° →
costela → encerramento em câmera lenta 0,3x escurecendo. Prévia: 8,4 s.

## Entrada do GTA (pedido do cliente: usar a própria entrada da referência 1)
- `opening` no timeline: REF1 de 0,78 a 8,85 s (começa depois do personagem verde e
  corta antes dos personagens aparecerem), corte vertical no centro (fora das marcas do
  TikTok), saltos acelerados (1,5x / 2,2x / 2,5x / 1,2x) e som original da entrada
  acompanhando as rampas (`audio_speed`, atempo por trecho). Zoom para dentro da 1ª unidade.
- Fonte é 1024x576: o corte vertical usa 324 px de largura, ampliados 3,3x. Limpeza:
  `hqdn3d` antes de ampliar, lanczos, `unsharp` e grão fino.
- `python3 render.py --entrada` gera só a abertura + 1º clipe em 1080x1920:
  `entrega/teste-ENTRADA-GTA.mp4` (5,9 s).

# v2 — entrada nítida, todos os clipes, emenda 2→3, efeito fachada e reverse (12,0 s)
Feedback: cadê o resto do material; entrada com mais qualidade; transição antes de aparecer
o personagem; vídeos 2 e 3 são da mesma gravação; usar os efeitos da referência 2 (reverse etc.).
- **Entrada** (`prep_abertura.py` → `work/REF1_vertical.mp4`, rode antes do render):
  super-resolução local (EDSR, OpenCV) foi testada e não ajudou (fonte já vem borrada, 1 min
  por quadro). Solução: a imagem horizontal inteira, nítida (ampliação 1,5x), numa janela
  sobre fundo desfocado dela mesma, que abre até a tela cheia no último salto. Bordas com a
  marca do TikTok cortadas (x 175–880, y 48–498). Termina em 7,40 s, último quadro antes do
  salto para a rua — nenhum personagem aparece.
- **Vídeo 2 → 3 (mesma gravação C128)**: `match_zoom` — a câmera mergulha na janela da
  churrasqueira (cx 0,27, cy 0,80, 3x, decodificado em 2x para não perder nitidez) e dissolve
  dentro do borrão (3 quadros) no close dos frangos, que entra assentando de 1,25x.
- **Efeito fachada (ref. 2)**: o logo chega voando (gira 38°, encolhe de 3,2x, com rastro),
  encaixa como letreiro em cima da fachada com um quique, ganha espessura 3D e sombra, e fica
  preso à fachada (rastreio OpenCV da faixa da fachada, sem a árvore); folhas passam na
  frente. Telefone do logo coberto.
- **Reverse**: grelha giratória em câmera lenta, volta em reverse 2x e acelera 3x até o whip;
  o encerramento faz câmera lenta 0,5x e volta em reverse.
- Final 1080x1920 30 fps: `entrega/guerreiros-TOUR-3-UNIDADES.mp4` (12,0 s, sem música,
  −21 LUFS só de ambiente/whoosh — a música entra depois).

# v3 — efeitos da referência 3 (tour da loja "T TECH", `referencias/REF3_efeitos.mp4`)
Efeitos da referência e o que foi aplicado:
- Logo montando na fachada (símbolo cai de cima, acende) → o brasão agora cai de cima,
  encolhendo, encaixa no telhado e **acende** (brilho que apaga em 10 quadros).
- Nomes de seção presos nas paredes/prateleiras em perspectiva, letra por letra →
  `labels`: **FRANGO NO ROLETE** na parede de inox da churrasqueira e **COSTELA** no
  fundo da churrasqueira, rastreados por homografia só nas partes paradas (a grelha que
  gira fica fora do rastreio), com sombra e brilho de letreiro.
- Texto grande saltando sobre o produto ("2200W") → `pop`: **NA BRASA** letra por letra
  sobre a grelha giratória, acompanhando 30% do movimento.
- Final em fundo claro com o logo → `ending.style = "white"`: o último plano clareia/desfoca
  até o fundo claro e o brasão entra com um quique, "3 UNIDADES · CUIABÁ" embaixo.
- Não aplicados (exigiriam elementos gerados/inventados): fogo acendendo no fogão, água
  estourando o vidro, produtos aparecendo na prateleira.

## Florais — material recebido (aguardando o Jardim Aclimação para editar)
| Arquivo | Conteúdo | Nota |
|---|---|---|
| FL_IMG_1429 (3,3 s, 4K 28p) | vista aberta: tendas com o banner, churrasqueiras na rua, céu | abertura da unidade (não é o IMG_1429 da ESCALA, arquivo diferente) |
| FL_C164 (2,4 s, 4K 60p) | câmera baixa ao lado da churrasqueira, fumaça, avança sobre a carne | forte para transição |
| FL_C177 (2,4 s, 4K 60p) | close dos frangos na grelha, avançando | bom |
| FL_copyB0FF (8 s, 1000x1210, HDR HLG 10 bits) | grelha de frangos girando, banner em cima, tronco na frente | resolução baixa; precisa converter HDR→SDR |

# v4 — as 3 unidades (23,4 s, formato Reels)
Jardim Aclimação recebido: JA_C143a (tenda/churrasqueiras, avança — estabelecimento),
JA_C139 (grelha com o banner, passa rápido), JA_IMG_1633 (espetos girando, iPhone 30p,
9,7 s — usado 4,4–5,7 s), JA_C143b (costela na grelha; não usado, repetia o C139).

Sequência: entrada GTA com gancho "POV: O GPS TE LEVOU PRO / GUERREIRO'S GRILL" →
zoom → **Jardim** (logo cai na tenda, título; grelha com reverse; "NO ESPETO") → whip →
**Tropical Ville** (logo na fachada, mergulho na churrasqueira, FRANGO NO ROLETE, NA BRASA
com reverse, COSTELA) → whip → **Florais** (vista aberta + título; câmera baixa na fumaça;
frangos com "NO CAPRICHO") → grelha girando (HDR convertido com tonemap hable) → whip →
**vinheta da marca** (take enviado pelo cliente = T07 da ESCALA), intacta, sem o look de cor.

Ajustes: nome de unidade comprido reduz só o tamanho do nome para caber (JARDIM ACLIMAÇÃO);
clipe pode ter `no_look`; final pode ter `final_clip`. Sem música (−24 LUFS de ambiente).
Entrega: `entrega/guerreiros-TOUR-3-UNIDADES.mp4` (1080x1920, 30 fps, 39 MB).

# v5 — todos os vídeos de cada unidade, vertical cheio, edição da ref. 3 (18,5 s)
Pedidos: usar os 4 vídeos de cada unidade; tudo na vertical (a entrada em janela horizontal
saiu: o GTA volta em tela cheia vertical, faixa central limpa e ampliada); usar a edição do
vídeo de inspiração (T TECH).
- Edição da ref. 3 medida: quase todo plano dura exatamente ~1,0 s (uma batida), com uma
  rajada de planos de 0,5 s, deslizes suaves e whip só no pico. Aplicado: 1 plano = 30
  quadros, títulos com 1,5 s, planos de 60p em câmera lenta 0,5x, rajada de 0,5 s na grelha
  giratória (câmera lenta + trecho em reverse), rótulo preso no cenário em quase todo plano.
- Jardim: C143a (título + logo na tenda) → C143b (COSTELA) → C139 (banner) → IMG_1633 (NO ESPETO).
- Tropical Ville: C128a (título + logo) → C128b (FRANGO NO ROLETE) → C130 (NA BRASA, rajada) → C122 (NO CARVÃO).
- Florais: IMG_1429 (título) → C164 (CHURRASCO RAIZ, o slogan do brasão) → C177 (NO CAPRICHO) →
  copyB0FF (a placa "CHURRASCO NA BRASA"; o giro vira o whip) → vinheta.

# v6 — correção pedida: edição da ref. 3 como molde, transições mais lentas, texto reposicionado (20,2 s)
Revisão da v5 contra a referência (T TECH, medida quadro a quadro):
- A ref. corta seco e cada plano ENTRA já em movimento rápido que desacelera (rampa), com borrão
  de movimento e um leve clarão; não usa whip entre planos. A v5 empilhava whip + borrão a cada
  corte, rápido demais para ler. Agora: `segments` aceita rampa `[a, b, v0, v1]` (ex.: 3x → 0,55x),
  o borrão vem da mistura dos quadros reais percorridos (fonte 60p), e o corte é `ramp_in`
  (clarão de 5 quadros). Whip removido.
- Duração: abertura de cada unidade ~2 s (logo montando devagar em 16 quadros, como a fachada da
  ref.), detalhes 32 quadros (~1,07 s), mergulho fachada→frangos em 12 quadros com dissolve de 4,
  vinheta entra com dissolve de 8.
- Tipografia num sistema só (Montserrat, como a ref.): título "UNIDADE" 500 espaçado + nome 800,
  alinhado à esquerda, margem 84 px à esquerda e 150 px à direita (botões do Reels), sombra só na
  faixa do texto; letreiros 600 presos no cenário (sem deslizar); destaque grande 800 por letra.
- Posições (zonas do Reels respeitadas: topo 220 px, base 420 px, coluna de botões à direita):
  JARDIM título y 1300 (chão), COSTELA na parede do fundo, NO ESPETO no toldo; TROPICAL VILLE título
  y 700 (sobre a árvore — embaixo ficam o homem e a churrasqueira), FRANGO NO ROLETE na parede de inox,
  NA BRASA no capô sobre a costela; FLORAIS título y 1300 (asfalto), NO CARVÃO na tampa com fumaça,
  NO CAPRICHO acima dos frangos. Saíram: CHURRASCO RAIZ e NA BRASA da grelha giratória (texto em cima
  da comida). Logos baixados para fora da faixa do topo.
- Todos os 4 vídeos de cada unidade continuam usados (12 clipes + entrada + vinheta).

# v7 — sem limite de 20 s: cada clipe usado quase inteiro (33,6 s)
Pedido: pode passar de 20 s, usar todo o material. Cada clipe agora vai do começo ao fim útil
(mesma rampa de entrada da ref. 3, terminando em câmera lenta 0,7–0,8x nos de 60p). IMG_1633
usa 0,4–2,0 s + 4,3–7,6 s (espetos e a mesa com os potes); FL_copyB0FF usa 1,6–5,2 s (frangos
e a placa CHURRASCO NA BRASA). Letreiros com duração limitada onde a câmera anda muito
(o rastreio se perde): FRANGO NO ROLETE 32 q, NO CARVÃO 26 q.

# v8 — ordem nova, abertura da Tropical Ville trocada, tipografia da REF4 (33,4 s)
- Ordem: **TROPICAL VILLE → FLORAIS → JARDIM ACLIMAÇÃO**.
- Tropical Ville: o take novo `source/TV_NOVO_abertura.mov` (copy_6B00…, 5 s, já editado em 3 partes)
  **substitui** a fachada antiga (C128a, que saiu junto com o logo voando, porque o take novo já tem
  o letreiro e o logo reais). Trecho usado: 3,20–4,97 s (vista de cima: fachada, banner, churrasqueiro
  na grelha com fumaça). Ficaram de fora 0–1,3 s (fachada, curta) e 1,4–3,0 s (grelha coberta com papel
  alumínio). O take traz o @GUERREIROSGRILL do próprio perfil no canto.
- A grelha com a placa (FL_copyB0FF), que era o fecho, entrou no fim do Florais; o Jardim fecha o vídeo
  e dissolve na vinheta.
- Tipografia (REF4 = tutorial "Texto em perspectiva / Texto chamativo"; só a referência visual, nada
  dela entra no vídeo): bloco com linha pequena em itálico branco espaçado + palavra grande Montserrat
  Black Italic em degradê de brasa, contorno escuro fino + sombra; títulos deitados no chão em perspectiva;
  entrada linha a linha (sobe, foca e assenta), saída com clarão. Tudo travado na área segura
  (70/160/230/420 px) e o bloco encolhe em vez de cortar palavra (corrige "CO", "NO ESP…", "FRANGO N…").
- Textos (menos, mais fortes): abertura "POV: O GPS TE TROUXE / PRO LUGAR CERTO" → "GUERREIRO'S GRILL";
  títulos "UNIDADE …"; CHURRASCO NA BRASA (costela, TV), FEITO NO CARVÃO (fumaça, Florais),
  CARNE NO PONTO (costela, Jardim), SEM ATALHO. / SÓ BRASA. (espetos, Jardim); fim sob o brasão:
  "GUERREIRO'S GRILL / 3 UNIDADES · CUIABÁ". Sem texto em frango/carne de perto nem na grelha giratória.

# v9 — fachada antiga de volta, take novo no lugar da costela, mergulho no Jardim, fonte da REF4 (32,3 s)
- Tropical Ville: take novo (vista de cima, título) → **fachada antiga C128a de volta** com o logo
  acendendo e o mergulho na churrasqueira até os frangos (C128b) → **take novo `TV_NOVO_4.mov`**
  (copy_C2CE…, costela girando, 0–1,75 s; depois disso é a tela final do CapCut) **no lugar da costela
  C122**. A grelha giratória (C130) saiu, a pedido.
- Jardim: o mesmo mergulho da Tropical Ville — da tenda (C143a) a câmera entra na churrasqueira da
  direita (cx 0,74, cy 0,50) e sai no close da costela (C143b).
- Tipografia copiada da REF4 ("Texto chamativo para seus vídeos"): **Poppins Black** laranja com halo
  laranja + **Poppins SemiBold** branco pequeno encaixado no canto de cima da palavra grande, caixa mista
  (palavra grande com inicial maiúscula, apoio em minúsculas). Títulos deitados no chão em perspectiva.
  Frases: "churrasco na / Brasa", "feito no / Carvão", "carne no / Ponto", "sem atalho. / Só brasa.";
  abertura "POV: o GPS te trouxe / pro lugar certo" → "bem-vindo ao / Guerreiro's Grill"; fim
  "Guerreiro's Grill / 3 unidades · Cuiabá".
- Skills de design ("taste" etc.) instaladas aqui são para sites/interfaces, não para vídeo; a fonte e o
  estilo vieram direto do vídeo de inspiração, como pedido.

# v10 — fonte e estilo de texto copiados da ref. T TECH (REF3), não da REF4
O cliente esclareceu que a inspiração de fonte/edição é o vídeo da T TECH (REF3).
- Letreiros como os da loja: **Montserrat SemiBold branco**, caixa normal ("Churrasco na brasa"),
  brilho branco de LED, presos na parede/toldo/capô em perspectiva (rastreio parcial) e **acendendo
  letra a letra** (varredura da esquerda para a direita); apagam sem clarão.
- Destaque como o "2200W": **Unbounded ExtraBold** (letra larga) **cromado** com contorno escuro —
  "GUERREIRO'S GRILL" na abertura e no fim, "SÓ BRASA" nos espetos do Jardim.
- Textos: abertura "POV: o GPS te trouxe / pro lugar certo" → GUERREIRO'S GRILL; "Unidade Tropical Ville"
  (fachada do take novo), "Churrasco na brasa" (costela), "Unidade Florais" (céu), "Feito no carvão"
  (tampa com fumaça), "Unidade Jardim Aclimação" (toldo), "Carne no ponto" (parede), "Sem atalho." +
  SÓ BRASA (espetos); fim GUERREIRO'S GRILL + "3 unidades · Cuiabá" sob o brasão.
- Jardim sem o logo voando (na ref. o logo só monta na fachada principal; o título agora fica no toldo).

# v11 — texto volta ao sistema da v7 (pedido: "cada frase uma fonte e uma posição diferente")
Mantidas as mudanças de montagem (ordem TV→Florais→Jardim, takes novos, mergulhos). Texto:
UMA fonte (Montserrat), UM lugar (embaixo à esquerda, x 84, y 1300, com faixa de sombra), UM formato
(linha pequena espaçada + linha grande ExtraBold + régua dourada) para títulos E frases:
UNIDADE/TROPICAL VILLE, CHURRASCO/NA BRASA, UNIDADE/FLORAIS, FEITO NO/CARVÃO, UNIDADE/JARDIM ACLIMAÇÃO,
CARNE NO/PONTO, SEM ATALHO./SÓ BRASA., 3 UNIDADES · CUIABÁ/GUERREIRO'S GRILL. Abertura como na v7
("POV: O GPS TE TROUXE / PRO LUGAR CERTO" + GUERREIRO'S GRILL, centralizado no topo). Logo do Jardim de volta.
`clip.block` desenha uma frase com o mesmo sistema do título.

# v12 — título mais chamativo, sai o C139, espetos corrigidos (28,2 s)
- Texto: mesmo lugar e formato da v11, mas a linha grande ficou maior (150), Montserrat Black (900) e em
  degradê dourado → brasa com brilho quente (`typography.hot`). Vale para títulos e frases (tudo igual).
- Saiu o JA_C139 (carnes penduradas na grelha amarela — print 1 do cliente).
- Espetos (print 2): IMG_1633 4,0–7,9 s estabilizado com vidstab
  (`vidstabdetect shakiness=8` + `vidstabtransform smoothing=20 zoom=8`) → `work/JA_1633_estab.mov`;
  usa só a parte de perto até o meio (0,1–2,5 s), sem a abertura torta do fim; leve zoom 1,08, mais
  contraste e menos névoa da fumaça. O trecho tremido 0,4–2,0 s saiu.

# v13 — frases de comida com estilo próprio, Florais 1 s menor (27,3 s)
- Frases de comida diferentes dos títulos: **Anton** (condensada), centralizadas no alto (cy 0,215), linha de
  cima branca + linha de baixo enorme em degradê de brasa, entram "batendo" (`punch`). Títulos das unidades
  continuam iguais (dourados, embaixo à esquerda).
  FRANGO/NA BRASA (frangos TV e Florais), COSTELA/NO PONTO (costela TV e Jardim), FEITO NO/CARVÃO (fumaça
  Florais), SEM ATALHO./SÓ BRASA. (espetos Jardim).
- Corrigido: a composição das camadas de texto somava as cores (a linha de baixo saía branca); agora é
  "over" ponderado pelo alfa (`_over`).
- Florais: primeiro plano começa 1 s depois (1,15 s).
- Agendadas 4 rodadas de melhoria a cada 30 min (pedido do cliente).

## Rodada automática 1/4 (cor entre unidades)
Medição por plano (luz média 0–255 e calor R−B): a abertura da Tropical Ville (take novo) era o plano mais
escuro do vídeo (54, sombras fechadas) e destoava dos frangos/costela seguintes (62–68). Sombras abertas com
curva + gama 1,12 e um toque quente → 69. Abertura do Florais levemente aquecida (o céu azul continua azul;
R−B −14 → −9) para casar com o laranja dos planos de brasa. Nenhum quadro repetido nos planos (só a vinheta,
que já vem assim). Nada de texto, ordem ou takes mudou.

# v14 — uma frase por unidade, frangos reenquadrados, abertura nova, 3 versões de texto
- Frases (além do nome da unidade): Tropical Ville FRANGO/NA BRASA, Florais FEITO NO/CARVÃO, Jardim
  SEM ATALHO./SÓ BRASA. Saíram as repetidas (costela TV, frango Florais, costela Jardim).
- Abertura: "O GTA LEVOU VOCÊ PRO / MELHOR CHURRASCO / DE CUIABÁ".
- Frangos (C128b): só 0,05–1,50 s (as duas fileiras), reenquadrado (zoom 1,06, x 0,62, y 0,62); saiu
  o fim em que a câmera desce e corta torto.
- 1º take da Tropical Ville com mais qualidade: hqdn3d → ampliação 2x lanczos → CAS + unsharp.
- `render.py --texto=fixo|movimento|sem`: "movimento" faz títulos e frases andarem com a câmera usando o
  deslocamento rastreado SUAVIZADO (gaussiana de ~0,1 s, 60 %, limite 90 px) — o rastreio bruto anterior
  tremia/saía do lugar. Saídas: guerreiros-TOUR-3-UNIDADES.mp4 (fixo), -TEXTO-EM-MOVIMENTO.mp4, -SEM-TEXTO.mp4.
- Florais copyB0FF: o cliente vai mandar substituto.
