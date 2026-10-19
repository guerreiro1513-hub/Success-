# Cardápio — comerciais de produto (9:16)

Projeto `projetos/cardapio/` — `prep.py` (estabiliza com vidstab e desacelera com minterpolate), `render.py PRODUTO`
(lê `produtos/PRODUTO.json`), entregas `entrega/guerreiros-PRODUTO.mp4`.

Fontes (`source/`): REF_INSPIRACAO (vídeo de "foto única vira vídeo 360°" com IA), PALETA_CORDEIRO (IMG_1939),
MAMINHA (IMG_1938), FRANGO (IMG_1881), COSTELA (IMG_1825), FRALDINHA (IMG_1818). Todos 4K vertical (rotação −90).

Análise: o vídeo da COSTELA já tem uma órbita real de ~270° ao redor da peça na tábua → "360" de verdade, sem IA.
Paleta, maminha e frango têm meia-órbita/aproximação; fraldinha tem aproximação + lado com os ossos.

## Costela (piloto, 15,5 s)
- 0–2 s: macro da crosta e dos ossos (zoom 1,55 → 1,42), entra do preto.
- 2–13 s: a órbita real ao redor da peça (estabilizada, câmera lenta 0,65x com quadros intermediários, leve avanço).
- 13 s (drop da trilha): escurece, logo real, "Costela" em Playfair Display itálico, régua dourada e "GUERREIROS GRILL".
- Look: contraste fílmico, altas quentes / sombras levemente frias, halation suave, fundo de cima e bordas escurecidos e
  desfocados (lente aberta) para tirar a bagunça do fundo.
- Som: trilha "trailer" própria (Kairogen, já do cliente) com as batidas a cada 3 s e o drop no fecho, ambiente real
  baixo, impacto grave sintetizado no logo. −14,4 LUFS.
- Sem IA na comida.

## Fraldinha, Frango, Maminha, Paleta de cordeiro (só filmagem real)
O teste de 360° com IA (Kairogen, frango) não rodou: a API não aceita arquivo local e o widget de envio não aparece no
app do cliente. Nenhum crédito gasto. Os 4 foram feitos só com a filmagem real (prep.py: vidstab + câmera lenta 0,6x).
- Cor "sol": os 4 vídeos foram gravados no sol forte → saturação 0,90, sombras levemente frias, sem empurrar laranja
  (a cor da costela, gravada no nublado, deixava esses laranja demais).
- Fraldinha (14,3 s, trilha trailer): abre colado na capa de gordura e vai abrindo (1,5 → 1,15x), depois contorna a
  peça até o lado dos ossos; fecho no drop (12 s).
- Frango (10,1 s, trilha groove): macro da pele dourada avançando, dissolve de 8 quadros para a volta no frango inteiro.
- Maminha (9,3 s, trilha épica): detalhe da fibra e depois um plano contínuo chegando devagar na peça (1 → 1,18x).
- Paleta de cordeiro (14,5 s, trilha trailer): macro do osso e da carne, órbita ao redor da paleta reenquadrada para
  baixo (1,14–1,26x, topo bem escurecido) para tirar as pessoas em volta; fecho no drop.
- Todos com o mesmo fecho da marca (logo real + nome do corte em Playfair itálico + GUERREIROS GRILL). −14 LUFS.
