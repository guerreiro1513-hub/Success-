# Keyframes — prompts de imagem (Kairogen)

Os keyframes são a espinha dorsal da consistência. Cada clipe de vídeo nasce de um
keyframe aprovado — assim o produto não muda de forma entre as cenas.

**Modelo recomendado:** `nano-banana-pro` (melhor fidelidade a imagem de referência)
**Alternativa econômica:** `seedream-5-pro` ou `seedream-v4-5`
**Aspect ratio:** `9:16` em todos
**Referência:** frames extraídos do vídeo do cliente, passados em `reference_image_urls`

---

## PRODUCT LOCK — bloco obrigatório

Este parágrafo é **colado em todos os prompts, sem alteração**. É ele que impede a
carne de virar outro produto entre as cenas.

✅ **Preenchido** a partir de `referencias/ref-4-picanha.jpg` — ver `docs/00-analise-produto.md`.

```
PRODUCT LOCK: Whole Brazilian picanha (top sirloin cap), 4-5cm thick, natural triangular
shape, fat cap left fully intact.
Surface: dark mahogany-brown seared crust, coarse rock salt visible on it, irregular char
marks from an open charcoal grill, glossy with rendered fat.
Fat cap: continuous 1-1.5cm white-to-golden layer along the curved outer edge, crisped and
lightly blistered outside, never trimmed off.
Interior when cut: medium-rare, warm rose-pink from edge to edge, thin brown-grey band only
directly under the crust, visible muscle grain, juices beading on the cut face.
Seasoning visible: coarse sea salt only. No herbs, no marinade, no sauce, no pepper crust.
Serving vessel: thick varnished reddish-brown hardwood carving board with a wide bevelled edge.
Tools when in frame: long carving knife and two-prong carving fork, dark wooden handles.
Hands when in frame: black food-service gloves, dark apron.
This exact product must appear identical in every frame — same cut, same thickness, same
char density, same fat cap, same seasoning.
```

### PRODUCT LOCK B — cena da brasa (só S2)
Baseado em `referencias/ref-1-grelha.png` e `ref-2-costela.jpg`.

```
SECONDARY PRODUCT: beef ribs and glazed cuts resting on a large steel wire-mesh grill frame,
deep amber-red glossy glazed surface, dark char in places, live embers and small flames below.
Same charcoal universe, same warm light source. No wooden skewers in frame.
```

> **Luvas pretas são obrigatórias** em toda cena com mão. É o que o cliente já usa, e é a
> defesa mais eficaz contra o erro clássico de mão deformada na geração por IA.

---

## Base style (colado em todos os prompts)

```
Professional food advertising photography, shot on ARRI Alexa with 100mm macro lens,
shallow depth of field, motivated warm key light from glowing charcoal below,
soft negative fill on the shadow side, deep rich blacks, natural colour,
photorealistic, commercial food campaign quality, no CGI look, no plastic sheen,
fine 35mm grain, vertical 9:16 composition.
```

**Negative prompt (todos):**
```
oversaturated orange, neon fire, cartoon flames, plastic texture, waxy meat,
raw undercooked grey meat, artificial smoke machine haze, glossy CGI render,
extra fingers, deformed hands, watermark, text, logo, oversharpened, HDR halo
```

---

## KF1 — Hook (macro)
```
[PRODUCT LOCK]
Extreme macro close-up of the caramelised crust, fat rendering and bubbling on the
surface, tiny beads of juice catching the light. Glowing orange charcoal completely
out of focus in the background. Only 2cm of the frame is in focus. Thin natural steam.
[BASE STYLE]
```

## KF2 — Brasa
```
[PRODUCT LOCK]
Low three-quarter angle across a charcoal grill grate, the product resting on the bars
with visible sear marks. Live red-orange embers glowing beneath. Thin wisps of real
smoke crossing a warm sidelight beam. Dark surroundings, the fire is the only light source.
[BASE STYLE]
```

## KF3 — Hero produto
```
[PRODUCT LOCK]
Hero shot of the whole piece just off the fire, resting on a dark aged wooden board.
Crisp dark crust, glistening rendered fat, natural steam rising. Three-quarter front
angle, product fills 70% of the frame height, centred for vertical composition.
Blurred warm embers far in the background.
[BASE STYLE]
```

## KF4 — Corte
```
[PRODUCT LOCK]
Close-up of a sharp chef knife blade mid-slice through the piece, the cut face opening
to reveal the juicy interior. Sharp contrast between the dark crust and the tender
interior. Juice welling at the cut surface. Hand holding the knife is natural and
anatomically correct, sleeve dark, out of focus.
[BASE STYLE]
```

## KF5 — Serviço
```
[PRODUCT LOCK]
A single slice lifted from the board, a thin thread of juice running off it. Board and
warm blurred embers visible behind. Slightly wider framing than the previous shot,
product still dominant. Natural human hand, correct anatomy, no jewellery.
[BASE STYLE]
```

## KF6 — Placa de branding (fundo do end card)
```
Extremely defocused glowing charcoal embers filling the frame, deep orange and red bokeh
on near-black background, no recognisable objects, no food, no flames. Soft vignette,
darkest area in the centre of the frame to leave room for a logo. Cinematic, vertical 9:16.
[BASE STYLE, sem PRODUCT LOCK]
```

---

## Critério de aprovação de keyframe

Um keyframe só passa para a etapa de vídeo se cumprir **todos**:

- [ ] O corte é o mesmo do vídeo de referência (forma, espessura, proporção)
- [ ] A carne parece comestível, não plástica nem encerada
- [ ] O laranja não invadiu tudo — ainda há neutros e pretos reais na imagem
- [ ] Nenhuma mão/dedo deformado
- [ ] O produto ocupa o peso visual dominante do frame
- [ ] Nenhuma marca d'água ou texto gerado acidentalmente

Reprovou em qualquer item → regerar com o mesmo prompt e seed diferente antes de seguir.
