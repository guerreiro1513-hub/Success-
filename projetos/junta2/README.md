# Auto Posto Florais — quinta a domingo e feriado (v2, 20,7 s)

`entrega/guerreiros-FLORAIS-QUI-A-DOM.mp4` — 1080×1920 · 30 fps · H.264 + AAC · −15,4 LUFS. `timeline.json` + `render.py`.

- Fala: o CapCut do cliente (`source/NOVO2.mov`, 720p) é IMG_1885 quadros 0–279 + NOVO_1885 quadros 54–138
  (mesma tomada, conferido quadro a quadro). Reconstruído dos originais 4K com esses mesmos cortes: emenda
  invisível e imagem nítida (4K → 1080 lanczos + nitidez cas 0,4).
- Transição (v8): avanço mais suave e longo (16 quadros, 1 -> 1,22x, puxando 25 % para a churrasqueira), mistura de
  9 quadros e a churrasqueira continua avançando e freia (1 -> 1,10x em 1,5 s).
- Churrasqueira mais longa (v8): IMG_1878 2,2–7,4 s + dissolve de 12 quadros + CHURRAS2 (close das carnes na fumaça,
  enviado depois) 0,1–9,2 s. Total 24,8 s.
- Legenda adiantada 0,18 s em relação à voz (lead).
  FLORAIS e os dias.
- Legenda (v5, estilo da referência do cliente, `source/REF_LEGENDA.mp4`, app Captions): Inter Tight 600/700 (OFL),
  minúsculas (nomes próprios mantidos), letras apertadas (−3,5 %), palavra-chave grande (104) e as outras pequenas
  (64) na mesma linha de base, 1–2 linhas centralizadas, branca com sombra difusa e sem contorno. Cada palavra entra
  quando é falada: desfoque -> nítida com um halo branco rápido. Tempos: texto do cliente + detector de voz + vales
  de energia entre palavras. Sempre dentro da área segura.
- Som (v8): voz normalizada; chiado da churrasqueira realçado (ganho 2,4x, passa-alta 150 Hz, +6 dB em 6 kHz);
  trilha gaúcha original (do projeto PACU; `assets/trilha-gaucha-loop.wav` repete só a parte com percussão, 15,0–20,4 s: o loop antigo voltava ao fade de entrada em 20,4 s e o final soava "bugado") baixa e constante (~−23 LUFS), sem subir
  na churrasqueira. Total −14 LUFS.
- v1 (duas tomadas com dissolve e pílulas dos dias) em `work/timeline_v1.json` e no histórico do git.

## v10 (22,0 s)
- Sem música (pedido do cliente): só a voz e o chiado realçado. Fade de 0,8 s no fim.
- 22 s cravados: CHURRAS2 vai até 6,4 s (o trecho final dele tinha o barulho estranho); fecho a partir de 19,4 s.
- Mais qualidade: nitidez cas 0,55, contraste/saturação um pouco maiores, master em CRF 14 (máx. 20 Mbps);
  arquivo de envio a 10,3 Mbps (preset slower).
