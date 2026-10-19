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
