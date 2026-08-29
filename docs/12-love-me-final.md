# LOVE ME — corte final (23,8s)

`entrega/guerreiros-grill-LOVEME-24s.mp4` — 1080×1920 · 9:16 · H.264 · 30 fps · AAC 48 kHz · 23,83 s

## Fontes
| Vídeo | Uso |
|---|---|
| VIDEO 1 | abertura falada (1,50 s) |
| **VIDEO A** (20,4 s, 1080×1920) | **principal fonte de DIA** — 10 planos, maior resolução do acervo |
| VIDEO 2 (14,4 s) | closes de comida, fogo, corte — 13 planos |
| VIDEO 3 (4,8 s) | rolete de dia — 2 planos (só 1,7 s sem texto queimado) |
| VIDEO 5 | fecho com logo + frase falada |
| VIDEO 4 | referência apenas — nenhum frame usado |
| VIDEO B (28,7 s) | **descartado**: @GUERREIROSGRILL queimado e em movimento no quadro |

**13 dos 27 planos são de dia** (antes eram 2 de 26).

## A trilha, reestruturada
O vocal "love me… oh ba-baby" mora em **0,50–3,50 s** da música. Antes ele caía
embaixo da voz do VIDEO 1, abafado. Agora toca **em cheio, com o texto em cima**.

| Pedaço | Trecho da música | Tempo do vídeo | O que é |
|---|---|---|---|
| P1 | 2,00 → 3,50 | 0,00 → 1,50 | embaixo da fala, volume 0,26 |
| P2 | 0,50 → 12,00 | 1,50 → 13,00 | **o vocal cantado**, depois o drop |
| P3 | 6,00 → 15,02 | 13,00 → 22,02 | segue |

Só **uma** emenda real (13,00 s), feita dentro de um silêncio de −50 dB. Inaudível.
P2 é contínuo: o vocal emenda no drop sem corte nenhum.

## Linha do tempo
| Tempo | Bloco |
|---|---|
| 0,00–1,50 | VÍDEO 1 — voz na frente, música baixa |
| **1,50** | corte seco · música em cheio |
| 1,50–4,50 | **LOVE / ME / OH / BA- / BABY sincronizados com o vocal cantado** (6 cortes) |
| **4,50** | O DROP |
| 4,50–19,00 | montagem — 5 blocos de 4 cortes, 5 cartelas pretas nos silêncios |
| 19,00–23,83 | VÍDEO 5 — logo, música em 0,40, frase final no silêncio |

Cortes de 0,23 s a 0,83 s. As cartelas pretas caem exatamente onde a música cala.

## Mixagem
| Trecho | Nível medido |
|---|---|
| 0,00–1,40 voz + música por baixo | −15,1 dB |
| 1,50–2,60 "LOVE ME" cantado | −19,2 dB |
| 2,60–3,80 seguindo | −17,3 dB |
| 4,50–6,50 o drop | −14,5 dB |
| 19,6–21,3 cama sob a fala do fecho | **−14,8 dB** (antes −28,5) |
| 22,1–22,5 respiro | silêncio digital |
| 22,55–23,45 **a frase** | −11,3 dB |

O trecho cantado leva ganho 2,0 → 1,0 ao longo de 1,50–4,50: fica audível sem
achatar o crescendo natural da música até o drop.

## Controle de qualidade
- 712 frames medidos: **0** frames pretos indevidos, **0** moles, **0** saltos de exposição.
- Brilho por plano **36,6 – 77,8** (b04 vinha estourando em 108,8; regradeado com rolloff de altas).
- Cartelas pretas em janelas de −38 a −44 dB.
- Pico −0,4 dB, sem clipe.

---

# Revisão 3 — 25,6 s

`entrega/guerreiros-grill-LOVEME-25s.mp4` — 1080×1920 · 30 fps · 25,60 s

## 1. Legenda grande na frase de abertura, atrás do sujeito
A frase entra em 4 linhas ocupando quase toda a largura (97%), revelando linha a
linha nos frames 0 / 7 / 15 / 23, com deriva de escala acompanhando o zoom do plano:

```
EU TÔ
SABENDO
QUE CÊ TÁ
COM FOME
```

O texto fica **atrás dele de verdade**, não por transparência. O recorte do sujeito
sai de GrabCut (OpenCV) rodando nos 45 frames: o primeiro frame parte de um
retângulo, os seguintes herdam um trimap do frame anterior (erode = certeza de
frente, dilate = certeza de fundo), o que dá coerência temporal. Depois, média
móvel de 5 frames + blur de 31 px na borda.

Resultado medido: cobertura do recorte 34–42%, **maior salto entre frames vizinhos
0,33 ponto** — sem tremer. Composição: vídeo → frase → recorte do sujeito por cima.

## 2. Ritmo do texto
O problema não eram as viradas fora do tempo — elas já estavam a menos de 75 ms dos
ataques reais. Era o **tempo parado**: uma palavra chegava a ficar 1,57 s na tela
enquanto a música pulsa a cada 0,19 s.

Reescrito para virar no tempo (0,75 s) e **gaguejar OH / BA- / BABY nos últimos
0,4 s antes de cada silêncio**, que é onde a música entrega o "oh ba-baby".

| | antes | agora |
|---|---|---|
| palavras na tela | 21 | **39** |
| desvio máximo do ataque | 75 ms | **75 ms** (nenhuma acima de 80) |
| maior tempo parado | 1,57 s | 1,50 s (só o "ME" cantado, que a voz segura mesmo) |

## 3. Final — a música volta no talo
A tela do Instagram ganhou mais tempo (outro do VIDEO 5 de 145 → 198 frames) e a
música **volta em cheio assim que a frase termina**, com o trecho 1,85–4,00 s da
faixa: o "oh ba-baby" subindo e **estourando no drop** em 25,10 s, que fecha o vídeo.

| Trecho | Nível |
|---|---|
| 22,55–23,45 a frase | −11,3 dB |
| 23,50–25,10 música de volta | −16,0 dB |
| 25,10–25,55 o drop final | −13,1 dB |

## Controle de qualidade
768 frames: **0** frames pretos indevidos, **0** moles, **0** saltos de exposição.
Abertura 40,5–55,4 de brilho, maior salto 5,1. Pico −0,4 dB, sem clipe.
