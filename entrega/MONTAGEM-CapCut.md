# Guerreiros Grill — folha de montagem

Para gerar o MP4 final no CapCut, Premiere, DaVinci ou CapCut PC.
Todos os arquivos estão na sua galeria do Kairogen (baixe por lá ou pelos links abaixo).

**Projeto:** 1080 × 1920 · 30 fps · 16 s · master em −14 LUFS

---

## Vídeo — 5 cortes secos

| # | Entra em | Sai em | Dur | Usar do clipe | Arquivo |
|---|----------|--------|-----|---------------|---------|
| 1 | 00,0 | 02,2 | 2,2s | 0,0 → 2,2 | `44b70eef-…mp4` (hook macro) |
| 2 | 02,2 | 05,2 | 3,0s | 0,0 → 3,0 | `34e0b010-…mp4` (brasa) |
| 3 | 05,2 | 08,6 | 3,4s | 0,0 → 3,4 | `8d07fe04-…mp4` (hero) |
| 4 | 08,6 | 12,0 | 3,4s | 0,0 → 3,4 | `ef2bd0e4-…mp4` (corte) |
| 5 | 12,0 | 14,4 | 2,4s | 0,0 → 2,4 | `6237c044-…mp4` (serviço) |
| 6 | 14,4 | 16,0 | 1,6s | imagem parada | `bb2f0dc5-…jpg` (fundo do end card) |

Cada clipe tem 5s — sobra material. Se um trecho não ficou bom, escolha outro pedaço
dentro do mesmo clipe em vez de regerar.

**Único efeito de velocidade do filme:** em 09,1 → 09,7 (dentro do corte 4), rampa
100% → 50% → 100%. Cobre exatamente o instante em que o interior da carne aparece.
Nenhuma outra rampa, nenhuma transição além de corte seco.

---

## Áudio — 6 camadas

| Camada | Entra | Volume | Arquivo |
|--------|-------|--------|---------|
| Trilha | 00,0 | −20 LUFS (fundo) | `…6a8df21d…/music.mp3` |
| Leito de brasa (loop) | 00,0 | −24 LUFS | `…6a8e18f9…/sound-effect.mp3` |
| Sizzle (loop, corta em 12,0) | 00,0 | −16 LUFS | `…6a8e190f…/sound-effect.mp3` |
| Labareda | 03,4 | −14 LUFS | `…6a8e191c…/sound-effect.mp3` |
| **Corte da faca** | 09,15 | **−10 dB pico — o som mais alto** | `…6a8e190a…/sound-effect.mp3` |
| Hit da marca | 14,4 | −12 LUFS | `…6a8e1919…/sound-effect.mp3` |

**Ducking — o único do filme:** abaixe a trilha 4 dB de 09,0 a 09,7 e devolva.
É o que faz o corte da faca ser ouvido.

**High-pass em 80 Hz na trilha**, para o sizzle e a brasa ocuparem o grave-médio.

O som entra a todo volume no frame 1 — sem fade-in. Fade-in no áudio mata retenção
igual a fade-in na imagem.

---

## Texto — só dois momentos

**05,6 → 06,9** · terço inferior
`CHURRASCO DE VERDADE.`
Anton ou Archivo Black · caixa alta · tracking +90 · `#F5EFE6`
Sombra 0 4px 24px rgba(0,0,0,.75)
Entra: fade 0,25s subindo 12px · Sai: fade 0,2s

**14,4 → 16,0** · end card sobre `bb2f0dc5-…jpg`
```
        GUERREIROS GRILL
       ──────────────────
     CHURRASCO RAIZ · SÁB & DOM
```
- Título: no máximo **38% da largura**, 8% acima do centro óptico
- Filete: 1px, `#C9752A` a 60%, largura 60% do título
- Subtítulo: tracking +140, `#E8DCC8`
- Entra: fade + escala 1,02 → 1,00 em 0,4s

**Zona segura:** tudo dentro de 12% de margem lateral e 240px acima do rodapé —
a UI do Reels come essa faixa.

---

## Color grading

| Ajuste | Valor |
|--------|-------|
| Sombras (lift) | `#12100E` — preto profundo, levemente quente |
| Gamma | +0,03 quente |
| Altas | rolloff suave, nunca clipar o brilho da gordura |
| Contraste | curva S ~1,15 |
| Saturação global | 105% |
| **Vermelhos da carne** (hue 5–15°) | saturação **+8**, luminância +3 |
| **Laranjas do fogo** (hue 25–45°) | saturação **−6** |
| Amarelos | −4 |
| Grão | 35mm fino, 2–3% |
| Vinheta | −10 nas bordas |

O teste: se você dessaturar mentalmente e a carne sumir no fundo, o grade está errado.

---

## Exportar

| Arquivo | Formato |
|---------|---------|
| `guerreiros-grill-16s.mp4` | 1080×1920 · H.264 · ~12 Mbps · áudio −14 LUFS |
| `guerreiros-grill-12s.mp4` | mesmo, sem o corte 2, com o corte 5 em 1,6s |
| Capa do Reels | frame do **corte 3** (hero), não do hook |

A capa sai do hero: no grid do perfil, é ele que segura o clique.
