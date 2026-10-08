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
