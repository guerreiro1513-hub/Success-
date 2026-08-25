# Custos e pipeline de execução

Valores obtidos via `estimate_cost` do Kairogen no plano **free** em 25/08/2026.
São números reais da API, não estimativa minha.

---

## Situação da conta

| Item | Valor |
|------|-------|
| Plano | **FREE** |
| Créditos disponíveis | **0** |
| Gerações simultâneas | 1 (imagem: 1, vídeo: 1) |
| Valor do crédito | R$ 0,175 |

**Com 0 créditos nenhuma geração roda.** Este é o bloqueio nº 1 da produção.

---

## Custos verificados

### Keyframes (6 imagens, 9:16)

| Modelo | Créditos | ~R$ | Nota |
|--------|----------|-----|------|
| `nano-banana-pro` | **32** | 5,60 | Melhor fidelidade à referência |
| `seedream-v4-5` | **12** | 2,10 | Bom custo-benefício |
| `seedream-5-pro` | **10** | 1,75 | Mais barato dos bons |

### Clipes (5 vídeos)

| Modelo | Config | Créditos | ~R$ |
|--------|--------|----------|-----|
| `seedance-v1-5-pro` | 5s, 1080p | **3** | 0,53 |
| `kling-v3-0-pro` | 5s, 1080p | **23** | 4,03 |
| `veo-3-1` | 6s, áudio nativo | **45** | 7,88 |

### Áudio

| Item | Créditos |
|------|----------|
| Trilha (`music`, 20s) | **3** |
| SFX (5 efeitos, estimativa) | ~5 |

---

## Pacotes

### 🟢 Econômico — 21 créditos (~R$ 3,68)
`seedream-5-pro` (10) + `seedance-v1-5-pro` (3) + áudio (8)
Entrega um filme bom. Menos controle fino de movimento de câmera.

### 🟡 Recomendado — 43 créditos (~R$ 7,53)
`seedream-v4-5` (12) + `kling-v3-0-pro` (23) + áudio (8)
**Melhor relação qualidade/custo.** O Kling V3 Pro é o que entrega movimento de câmera
cinematográfico de verdade e mantém a forma do produto sem morphing.

### 🔴 Máximo — 85 créditos (~R$ 14,88)
`nano-banana-pro` (32) + `veo-3-1` com áudio nativo (45) + trilha (8)

---

## Orçamento com retakes

O briefing é explícito: *"Não aceite a primeira geração automaticamente."* Isso é direção
correta, e precisa estar no orçamento. Na prática, 1 em cada 2 clipes de comida precisa de
pelo menos um retake — normalmente por morphing da carne ou por mão deformada.

| Pacote | Base | +50% retakes | **Recomendado comprar** |
|--------|------|--------------|------------------------|
| Econômico | 21 | 32 | **35 créditos** |
| Recomendado | 43 | 65 | **70 créditos** |
| Máximo | 85 | 128 | **130 créditos** |

**Minha recomendação: 70 créditos**, pacote Recomendado com folga real para refazer
S3 e S4 quantas vezes for preciso — são as duas cenas que vendem o produto.

---

## Pipeline de execução

Limite de **1 geração simultânea** no plano free: tudo roda em série, sem paralelismo.

```
ETAPA 1 · ANÁLISE          [BLOQUEADA — falta o vídeo de referência]
  └─ assistir o vídeo, preencher o PRODUCT LOCK em docs/02

ETAPA 2 · PLANEJAMENTO     [CONCLUÍDA]
  └─ storyboard, prompts, som, grading, custos — este repositório

ETAPA 3 · GERAÇÃO          [BLOQUEADA — 0 créditos]
  ├─ 3a. 6 keyframes, um a um, com aprovação individual
  ├─ 3b. 5 clipes image-to-video a partir dos keyframes aprovados
  └─ 3c. trilha + 5 efeitos sonoros

ETAPA 4 · MONTAGEM         [depende da 3]
  └─ HyperFrames: timeline 9:16, cortes, speed ramp em S4

ETAPA 5 · REFINO           [depende da 4]
  └─ checklists de docs/02 e docs/03; regerar o que reprovar

ETAPA 6 · FINALIZAÇÃO      [depende da 5]
  └─ grading, mix −14 LUFS, tipografia, end card, render 16s + 12s
```

**Ponto de controle entre 3a e 3b:** nenhum clipe é gerado antes dos 6 keyframes estarem
aprovados. Gerar vídeo a partir de keyframe ruim é a forma mais rápida de queimar crédito.
