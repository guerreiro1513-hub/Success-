# GUERREIROS GRILL 🔥 — Filme publicitário 9:16

Pré-produção completa de um filme publicitário gastronômico para o Guerreiros Grill,
para ser gerado com **Kairogen** (imagem, vídeo, áudio) e finalizado no **HyperFrames**
(montagem, tipografia, render).

**Formato:** 9:16 vertical · 1080×1920 · 30fps · 16s (+ corte alternativo de 12s)
**Destino:** Instagram Reels, Stories, TikTok

---

## Status

| Etapa | Estado |
|-------|--------|
| 1 · Análise do produto | ⛔ **Bloqueada** — vídeo de referência não chegou |
| 2 · Planejamento | ✅ **Concluída** — este repositório |
| 3 · Geração | ⛔ **Bloqueada** — conta Kairogen com 0 créditos |
| 4 · Montagem | ⏳ depende da 3 |
| 5 · Refino | ⏳ depende da 4 |
| 6 · Finalização | ⏳ depende da 5 |

### Bloqueio 1 — vídeo de referência ausente
O briefing menciona um vídeo anexado, mas ele não chegou nesta sessão: o diretório de
anexos (`/mnt/attach`) está vazio e não há arquivo de mídia acessível. O widget de upload
do Kairogen já foi aberto no chat — basta enviar o vídeo por lá.

Sem ele, os campos `{{ }}` do **PRODUCT LOCK** (`docs/02-keyframes-prompts.md`) não podem
ser preenchidos, e gerar sem eles violaria a regra do briefing de não transformar o produto
em outro produto.

### Bloqueio 2 — 0 créditos
A conta está no plano FREE com 0 créditos. Qualquer `generate_image` / `generate_video`
falha. Orçamento recomendado: **70 créditos** (~R$ 12,25) — detalhamento em
`docs/06-custos-e-pipeline.md`.

---

## Documentos

| Arquivo | Conteúdo |
|---------|----------|
| [`docs/01-storyboard.md`](docs/01-storyboard.md) | Shot list com timecodes, direção cena a cena, versão 12s |
| [`docs/02-keyframes-prompts.md`](docs/02-keyframes-prompts.md) | PRODUCT LOCK + 6 prompts de imagem + critério de aprovação |
| [`docs/03-video-prompts.md`](docs/03-video-prompts.md) | 5 prompts image-to-video, parâmetros de modelo, checklist |
| [`docs/04-sound-design.md`](docs/04-sound-design.md) | 7 camadas de áudio, prompts e especificação de mixagem |
| [`docs/05-montagem-grading.md`](docs/05-montagem-grading.md) | Montagem, color grading, tipografia, end card |
| [`docs/06-custos-e-pipeline.md`](docs/06-custos-e-pipeline.md) | Custos reais da API, pacotes, ordem de execução |

---

## Decisões de direção

**A carne é a protagonista absoluta.** Todas as escolhas abaixo derivam disso.

- **Consistência por keyframe.** Cada clipe nasce de uma imagem aprovada
  (`image-to-video`), nunca de texto puro. É o que impede a carne de mudar de forma
  entre as cenas.
- **PRODUCT LOCK.** Um bloco descritivo idêntico colado em todos os prompts, travando
  corte, espessura, crosta, gordura e ponto.
- **Um único speed ramp** no filme inteiro, em S4, cobrindo o instante em que o interior
  da carne se revela. Efeito a serviço da narrativa.
- **Laranja contido.** Saturação dos laranjas do fogo **reduzida** em −6 e vermelhos da
  carne elevados em +8. O excesso de laranja é o que faz um vídeo parecer feito por IA.
- **Áudio em camadas, não nativo.** Os clipes são gerados sem som (`sound: false`) para
  que a mixagem seja controlada — com ducking da trilha só no corte da faca.
- **Texto mínimo.** Duas inserções no filme todo. Preço, telefone e endereço vão na
  legenda do post, não na tela.

---

## Como retomar

1. Enviar o vídeo de referência pelo widget de upload do Kairogen
2. Preencher o PRODUCT LOCK em `docs/02-keyframes-prompts.md`
3. Adicionar créditos na conta Kairogen (recomendado: 70)
4. Executar a ETAPA 3 na ordem descrita em `docs/06-custos-e-pipeline.md`
