# Resultados — ETAPA 3a (keyframes)

3 keyframes gerados e aprovados. **10 créditos usados, 20 restantes.**

Modelo: `seedream-5-pro` · 9:16 · referência: `referencias/ref-4-picanha.jpg`

> Os arquivos ficam no CDN do Kairogen e na galeria da conta. A política de rede deste
> ambiente bloqueia `cdn.kairogen.ai`, então só as URLs estão registradas aqui.

---

## KF3 — Hero (cena S3) ✅
`https://cdn.kairogen.ai/gallery/images/6a8caaa9baf3b3e2d5d25379/da02f27c-e6fb-4610-b266-5a40ee854efb.jpg`

Picanha inteira na tábua, capa de gordura dourada na borda curva, brasa desfocada ao fundo,
vapor natural. Formato triangular correto.

## KF4 — Corte (cena S4) ✅ — a melhor das três
`https://cdn.kairogen.ai/gallery/images/6a8caaa9baf3b3e2d5d25379/e5d08cc0-0310-4861-96cd-5d855fcd6929.jpg`

Faca atravessando, interior rosado ponta a ponta com a faixa cinza fina só sob a crosta,
fatias já cortadas ao lado, luva preta sem deformação, fogo ao fundo.

## KF1 — Hook macro (cena S1) ✅
`https://cdn.kairogen.ai/gallery/images/6a8caaa9baf3b3e2d5d25379/ae77f931-7cbc-4020-a731-125e5578cff8.jpg`

Macro da crosta ocupando o quadro inteiro: sal grosso, gotas de gordura, marcas de char,
brasa alaranjada na base. Profundidade rasa.

---

## Reprovado

**KF3 v1** — `seedream-5-pro` 2K, **sem imagem de referência**. Custou 4 créditos.
Saiu um bife com capa de gordura, não uma picanha: produto errado, violando a regra
crítica do briefing. A API sinalizou a causa no `reference_warning`.

Correção aplicada nas gerações seguintes: anexar a referência e escrever
"A WHOLE uncut picanha, roughly 28cm long, NOT a small steak, NOT a portion cut".

---

## Uso imediato

Mesmo com o vídeo bloqueado, os 3 keyframes já servem como **posts estáticos**: são 9:16,
com a estética da campanha e o produto correto. O KF4 funciona bem como capa de Reels.

Para reaproveitar como post, vale regerar em 2K (4 créditos cada) — os 20 créditos restantes
cobrem os três com folga.

## Para retomar a ETAPA 3b

1. Fazer upgrade do plano Kairogen (o FREE não libera vídeo em nenhum modelo)
2. Reenviar a referência (a URL expira em ~30 min)
3. Animar cada keyframe com `seedance-v1-5-pro`, 4s, 9:16, 1080p — prompts em `docs/03`
4. Montar conforme `docs/05`
