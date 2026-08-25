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

> ⚠️ Os campos entre `{{ }}` só podem ser preenchidos depois de assistir ao vídeo de
> referência. Enquanto estiverem em branco, **nenhuma geração deve ser disparada** — gerar
> com o produto errado desperdiça crédito e quebra a regra "não transforme o produto em outro produto".

```
PRODUCT LOCK: {{CORTE}} — {{FORMATO_E_ESPESSURA}}.
Surface: {{DESCRICAO_CROSTA}}. Fat cap: {{GORDURA}}.
Interior when cut: {{PONTO_E_COR_INTERIOR}}.
Seasoning visible on surface: {{TEMPERO}}.
Serving vessel: {{APRESENTACAO}}.
This exact product must appear identical in every frame — same cut, same thickness,
same char pattern density, same fat distribution, same seasoning.
```

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
