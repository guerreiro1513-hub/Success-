# Clipes — prompts de vídeo (Kairogen image-to-video)

Cada clipe parte do keyframe aprovado correspondente (`first_frame_url`).
Isso trava o produto: o modelo anima a imagem em vez de inventar carne nova.

**Modelo recomendado:** `kling-v3-0-pro` — 1080p, 9:16, image-to-video, aceita `end_image`
**Alternativa econômica:** `seedance-v1-5-pro` (bem mais barato, aceita first + last frame)
**Alternativa com áudio nativo:** `veo-3-1` (`generate_audio: true`) — mais caro, durações 4/6/8s

### Parâmetros fixos (`extra_params` no `generate_video`)

```json
{
  "aspect_ratio": "9:16",
  "quality": "1080p",
  "sound": false,
  "duration": 5
}
```

Gerar **sempre 5s** mesmo quando o storyboard pede 2.2s ou 3.4s — sobra material para
escolher o melhor trecho na montagem. O corte fino acontece na edição, não na geração.

> Nota: `kling-v3-0-pro` usa as chaves `first_frame` e `end_image` no schema. Passe-as via
> `extra_params` (ou use `first_frame_url` no argumento genérico) — não misture as duas formas.

---

## S1 — Hook
**first_frame:** KF1
```
Extremely slow push-in on the sizzling crust. Fat bubbles and renders in real time,
a bead of juice swells and catches the light. Thin steam drifts upward naturally.
Background embers pulse gently. Camera moves 5% closer over the shot. Nothing else moves.
```
`negative:` `fast camera movement, zoom burst, flickering, morphing texture, shape change`

## S2 — Brasa
**first_frame:** KF2
```
Slow lateral tracking move across the charcoal grill. Embers glow and breathe, one small
brief flare-up rises and settles. Thin smoke crosses the warm sidelight. The product rests
on the grate, unmoving except for gentle sizzling. Handheld-subtle, not shaky.
```
`negative:` `large flames, explosion, fireball, dense fog, smoke machine, flickering strobe`

## S3 — Hero produto
**first_frame:** KF3
```
Short 20-degree orbit around the resting piece on the wooden board. Steam rises steadily.
Surface glistens as the light rakes across it during the move. Product stays perfectly
still and keeps its exact shape throughout. Slow, controlled, tripod-smooth motion.
```
`negative:` `object morphing, shape drift, rotating food, melting texture, wobble`

## S4 — Corte
**first_frame:** KF4
```
A sharp knife slices cleanly down through the piece at natural speed. The cut face opens,
revealing the juicy interior. Juice beads along the cut. Camera follows the blade down
slightly. Hand and knife move naturally and stay anatomically correct.
```
`negative:` `extra fingers, deformed hand, knife bending, sawing motion, mush, blood`

## S5 — Serviço
**first_frame:** KF5
**end_image:** KF6 *(faz a transição natural para o end card)*
```
The slice is lifted smoothly from the board, a thread of juice running off it. Camera pulls
out slowly, revealing the board and the warm blurred embers behind. Motion is calm and
satisfying. Ends with the frame drifting out of focus into warm bokeh.
```
`negative:` `dropping food, jerky motion, deformed hand, shaking camera`

---

## Critério de aprovação de clipe

- [ ] **Consistência:** o produto tem a mesma forma do primeiro ao último frame — sem morphing
- [ ] **Física:** fumaça, vapor, gordura e suco se comportam como na vida real
- [ ] **Câmera:** o movimento é intencional; nada de deriva aleatória de IA
- [ ] **Mãos:** se houver mão, ela está correta em todos os frames
- [ ] **Estética:** não parece "vídeo de IA" — sem aquele brilho plástico e sem warping de fundo
- [ ] **Uso real:** existem pelo menos 3.5s aproveitáveis dentro do clipe

Reprovou → regerar. O briefing é explícito: **não aceitar a primeira geração automaticamente.**
Orçar ~50% de créditos extras para retakes (ver `06-custos-e-pipeline.md`).

### Ordem de prioridade em caso de crédito limitado
1. **S3** (hero) e **S4** (corte) — são as cenas que vendem
2. **S1** (hook) — define a retenção
3. **S5** (serviço)
4. **S2** (brasa) — a mais dispensável; a versão de 12s já vive sem ela
