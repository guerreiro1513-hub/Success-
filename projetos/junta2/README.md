# Auto Posto Florais — quinta a domingo e feriado (v2, 20,7 s)

`entrega/guerreiros-FLORAIS-QUI-A-DOM.mp4` — 1080×1920 · 30 fps · H.264 + AAC · −15,4 LUFS. `timeline.json` + `render.py`.

- Fala: o CapCut do cliente (`source/NOVO2.mov`, 720p) é IMG_1885 quadros 0–279 + NOVO_1885 quadros 54–138
  (mesma tomada, conferido quadro a quadro). Reconstruído dos originais 4K com esses mesmos cortes: emenda
  invisível e imagem nítida (4K → 1080 lanczos + nitidez cas 0,4).
- Transição (v4): sem a caminhada. A fala termina logo depois do "um abraço" (NOVO_1885 3,66 s); a câmera avança
  de leve (10 quadros, 1,07x), mistura em 5 quadros e entra direto na churrasqueira de perto (IMG_1878 a partir de
  2,2 s), que assenta do zoom 1,07 para 1 em 14 quadros. 17,7 s no total.
  FLORAIS e os dias.
- Legenda (v5, estilo da referência do cliente, `source/REF_LEGENDA.mp4`, app Captions): Inter Tight 600/700 (OFL),
  minúsculas (nomes próprios mantidos), letras apertadas (−3,5 %), palavra-chave grande (104) e as outras pequenas
  (64) na mesma linha de base, 1–2 linhas centralizadas, branca com sombra difusa e sem contorno. Cada palavra entra
  quando é falada: desfoque -> nítida com um halo branco rápido. Tempos: texto do cliente + detector de voz + vales
  de energia entre palavras. Sempre dentro da área segura.
- Som: voz normalizada + trilha C (groove) a −22 dB com sidechain.
- v1 (duas tomadas com dissolve e pílulas dos dias) em `work/timeline_v1.json` e no histórico do git.
