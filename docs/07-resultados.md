# Resultados da produção

Base das URLs de imagem:
`https://cdn.kairogen.ai/gallery/images/6a8caaa9baf3b3e2d5d25379/`

> A política de rede deste ambiente bloqueia `cdn.kairogen.ai`, então só as URLs ficam
> registradas aqui. Os arquivos estão na galeria da conta Kairogen.

---

## ETAPA 3a — Keyframes ✅ 6 de 6 aprovados

Modelo `seedream-5-pro`, 9:16, 1K. **12 créditos.**

| # | Cena | Arquivo | Referência usada |
|---|------|---------|------------------|
| KF1 | Hook macro | `ae77f931-7cbc-4020-a731-125e5578cff8.jpg` | foto do cliente |
| KF2 | Brasa | `8e62ba53-b181-454d-a11e-88ada43ccb36.jpg` | **KF3** |
| KF3 | Hero | `da02f27c-e6fb-4610-b266-5a40ee854efb.jpg` | foto do cliente |
| KF4 | Corte | `e5d08cc0-0310-4861-96cd-5d855fcd6929.jpg` | foto do cliente |
| KF5 | Serviço | `a518a9ff-9270-45c0-8c4d-3a7240456a24.jpg` | **KF4** |
| KF6 | Fundo do end card | `bb2f0dc5-60a4-41b0-9986-ca9173473f6e.jpg` | nenhuma (abstrato) |

**Decisão que melhorou a consistência:** KF2 e KF5 usaram como referência os keyframes
**já aprovados** em vez da foto original do cliente. Assim as cenas novas casam com o
produto validado, e não com a iluminação de sol duro da foto de celular.

**Mudança em relação ao storyboard original:** a cena da brasa (S2) mostra a **própria
picanha** na grelha, não a costela. Trocar de corte no meio do filme quebraria a
continuidade do produto — o universo do churrasco aparece pelas outras peças desfocadas
ao fundo.

### Reprovado
**KF3 v1** — `seedream-5-pro` 2K **sem referência**, 4 créditos. Entregou um bife com capa
de gordura em vez de picanha. A API sinalizou a causa (`reference_warning`). Corrigido
anexando a referência e escrevendo "A WHOLE uncut picanha, roughly 28cm long, NOT a small
steak, NOT a portion cut".

---

## ETAPA 3c — Áudio (parcial)

| Camada | Status | Créditos | Arquivo |
|--------|--------|----------|---------|
| A6 · Trilha (20s, instrumental) | ✅ | 3 | `audio-generations/…/6a8df21d3293516e6be5b52d/music.mp3` |
| A1 · Leito de brasa | pendente | ~1 | |
| A2 · Sizzle | pendente | ~1 | |
| A4 · Corte da faca | pendente | ~1 | |
| A5 · Suco pingando | pendente | ~1 | |
| A7 · Hit final | pendente | ~1 | |

---

## ETAPA 3b — Clipes (em geração)

Modelo `kling-v3-0-pro`, 1080p, 9:16, 5s, sem áudio. **23 créditos por clipe.**

Gerados 5s mesmo onde o storyboard pede 2.2–3.4s: sobra material para escolher o melhor
trecho na montagem.

| Clipe | Keyframe | Generation ID | Status |
|-------|----------|---------------|--------|
| S1 · Hook | KF1 | `6a8df20b1fe750b044f3ce4a` | em fila |
| S3 · Hero | KF3 | `6a8df20e3293516e6be5b4e2` | em fila |
| S4 · Corte | KF4 | `6a8df21139d40e2a9682c386` | em fila |
| S2 · Brasa | KF2 | — | a disparar |
| S5 · Serviço | KF5 → KF6 | — | a disparar (`end_image` = KF6) |

---

## Orçamento

| Etapa | Créditos |
|-------|----------|
| Keyframes (incl. 1 reprovado) | 16 |
| Trilha | 3 |
| 5 clipes previstos | 115 |
| SFX previstos | ~5 |
| **Total previsto** | **~139** |

Plano PRO: 950 créditos. Sobra confortável para retakes.
