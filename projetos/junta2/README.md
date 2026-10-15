# Auto Posto Florais — quinta a domingo e feriado (v2, 20,7 s)

`entrega/guerreiros-FLORAIS-QUI-A-DOM.mp4` — 1080×1920 · 30 fps · H.264 + AAC · −15,4 LUFS. `timeline.json` + `render.py`.

- Fala: o CapCut do cliente (`source/NOVO2.mov`, 720p) é IMG_1885 quadros 0–279 + NOVO_1885 quadros 54–138
  (mesma tomada, conferido quadro a quadro). Reconstruído dos originais 4K com esses mesmos cortes: emenda
  invisível e imagem nítida (4K → 1080 lanczos + nitidez cas 0,4).
- Transição (v3): a câmera avança devagar (18 quadros, zoom ~1,2x) até o enquadramento exato do início da churrasqueira
  (alinhamento automático pela tenda, SIFT + RANSAC) e mistura em 8 quadros; o zoom extra de cobertura se desfaz em
  20 quadros. Parece um plano só. A fala termina em NOVO_1885 4,10 s (melhor ponto de alinhamento).
  FLORAIS e os dias.
- Legenda (estilo atual): Poppins Black maiúscula, contorno escuro arredondado + sombra difusa, páginas de 1–3
  palavras; cada palavra entra quando é falada e a palavra falada fica dourada e maior (uma por vez).
  GUERREIRO'S GRILL / AUTO POSTO FLORAIS / TEM CHURRASCO em dourado. Tempos: texto do cliente + detector de voz
  + vales de energia entre palavras. Sempre dentro da área segura.
- Som: voz normalizada + trilha C (groove) a −22 dB com sidechain.
- v1 (duas tomadas com dissolve e pílulas dos dias) em `work/timeline_v1.json` e no histórico do git.
