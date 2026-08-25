# Custos e pipeline de execução

⚠️ **Tabela corrigida em 25/08/2026.** A primeira versão deste documento usava
`estimate_cost` com `quantity`, e o estimador **não multiplica pelo quantity** — os números
saíram muito abaixo do real. Os valores abaixo são por geração, medidos um a um e
confirmados contra o saldo real da conta.

---

## Bloqueio de plano: vídeo não roda no FREE

Testado com dois modelos diferentes (`seedance-v1-5-pro` e `grok-imagine-video-v1-5`).
Ambos retornam:

```
403 [PLAN_UPGRADE_REQUIRED]
Este modelo de vídeo não está disponível no seu plano.
```

**Não é falta de crédito** — é restrição do plano FREE. Com créditos e plano FREE dá para
gerar imagem e áudio, mas **nenhum vídeo**. Liberar a ETAPA 3b exige plano pago.

---

## Custos reais medidos (plano FREE)

### Imagem
| Modelo | Config | Créditos |
|--------|--------|----------|
| `seedream-5-pro` | 1K, 9:16 | **2** |
| `seedream-5-pro` | 2K, 9:16 | **4** |

O 2K dobra o preço. Para keyframe que vira vídeo, **1K basta** — o modelo de vídeo
reamostra mesmo. Vale o 2K só para imagem que vai virar post estático.

### Vídeo (indisponível no FREE — preços para quando houver upgrade)
| Modelo | Config | Créditos **por vídeo** |
|--------|--------|------------------------|
| `seedance-v1-5-pro` | 4s | **5** |
| `seedance-v1-5-pro` | 5s | **7** |
| `kling-v3-0-pro` | 5s, 1080p | **23** |
| `wan-2-6` | 5s | **23** |
| `veo-3-1` | 6s, áudio nativo | **45** |

### Áudio
| Item | Créditos |
|------|----------|
| Trilha (`music`, 20s) | **3** |

---

## Orçamento real do filme

**Filme de 5 cenas** (storyboard completo, `docs/01`):

| Pacote | Keyframes | Clipes | Áudio | Total | +50% retakes |
|--------|-----------|--------|-------|-------|--------------|
| Econômico | 6×2 = 12 | 5×5 = 25 | 8 | 45 | **~68** |
| Premium | 6×2 = 12 | 5×23 = 115 | 8 | 135 | **~200** |

**Filme de 3 cenas** (hook + hero + corte, ~10s):

| Pacote | Keyframes | Clipes | Áudio | Total | +retakes |
|--------|-----------|--------|-------|-------|----------|
| Econômico | 3×2 = 6 | 3×5 = 15 | 3 | 24 | **~35** |

O pacote de **280 créditos** cobre o filme completo no econômico com muita folga
(~68 usados, ~210 sobrando), ou o premium com retakes (~200).

---

## Pipeline

Limite de **1 geração simultânea** no FREE: tudo em série.

```
ETAPA 1 · ANÁLISE          [CONCLUÍDA]  4 fotos do cliente, PRODUCT LOCK fechado
ETAPA 2 · PLANEJAMENTO     [CONCLUÍDA]  storyboard, prompts, som, grading
ETAPA 3a · KEYFRAMES       [CONCLUÍDA]  3 de 3 aprovados — ver docs/07-resultados.md
ETAPA 3b · CLIPES          [BLOQUEADA]  plano FREE não libera vídeo
ETAPA 3c · ÁUDIO           [disponível] trilha e SFX rodam no FREE
ETAPA 4 · MONTAGEM         [depende de 3b]
ETAPA 5 · REFINO           [depende de 4]
ETAPA 6 · FINALIZAÇÃO      [depende de 5]
```

## Aprendizados operacionais

- **`estimate_cost` com `quantity` não é confiável.** Estimar sempre com `quantity: 1`
  e multiplicar na mão.
- **`seedream-5-pro` não aceita `negative_prompt`.** Só `aspect_ratio` e `resolution`;
  mandar negative derruba a chamada com `VALIDATION_ERROR`. As negativas têm que estar
  redigidas dentro do prompt positivo.
- **Chamada bloqueante não funciona:** o canal MCP corta em 60s, então
  `wait_for_completion: true` sempre estoura. O certo é disparar assíncrono e depois
  chamar `get_generation` (que também corta em 60s, mas a segunda chamada já pega pronto).
- **Referência de imagem é decisiva.** A primeira geração, sem referência, entregou um bife
  genérico em vez de picanha, e a própria API avisou (`reference_warning`). Com a referência
  anexada, o produto saiu certo de primeira.
- **A URL de referência expira em ~30 minutos.** Reenviar antes de cada lote de gerações.
