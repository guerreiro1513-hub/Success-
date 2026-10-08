# HUGO ALMEIDA · ortodontista · Cuiabá-MT — vídeo fixado do perfil

**1080×1920 · 30fps · H.264 · AAC · −14 LUFS** · duração atual **55,6s**

Montado com os placeholders no lugar das 4 falas. Quando os vídeos reais
entrarem em `falas/`, a linha do tempo se reacomoda sozinha.

---

## Estado agora

| | |
|---|---|
| `output/hugo-almeida_FINAL.mp4` | **1080×1920, CRF 18, pico 16 Mbps** — é este que vai pro Instagram |
| `output/hugo-almeida_PREVIEW.mp4` | 540×960, CRF 28 — só pra conferir ritmo rápido. Não julgue qualidade por ele |

```bash
python3 render.py             # final 1080×1920
python3 render.py --preview   # rascunho rápido
```

---

## Linha do tempo

| TC | Bloco | Fonte | Dur | Texto na tela |
|---|---|---|---|---|
| 0:00 | FACHADA | `broll/01_fachada.mov` | 2,14s | "Quem é o Hugo?" (últimos 1,5s) |
| 0:02 | **FALA 1** | `falas/bloco1` | 10s* | "Hugo Almeida / Ortodontista · Cuiabá" (3s iniciais) |
| 0:12 | RECEPÇÃO | `broll/02_recepcao.mov` | 2,5s | "O que ele faz de diferente?" |
| 0:15 | **FALA 2** | `falas/bloco2` | 12s* | — |
| 0:27 | TECNOLOGIA · scanner | `broll/03_…` | 1,5s | — |
| 0:28 | TECNOLOGIA · alinhador | `broll/04_…` | 2,0s | — |
| 0:30 | QUADROS | `broll/05_quadros.mov` | 2,5s | "Pra quem é o tratamento?" |
| 0:33 | **FALA 3** | `falas/bloco3` | 11s* | — |
| 0:44 | PRATELEIRA · prêmio | `broll/06_…` | 1,5s | — |
| 0:45 | INSTRUMENTOS | `broll/07_…` | 1,5s | "Como começar?" |
| 0:47 | **FALA 4** | `falas/bloco4` | 9s* | "Agende sua avaliação / WhatsApp" (últimos 2s) |

\* duração prevista — o arquivo real manda, e o resto desloca.

---

## Arquitetura

```
timeline.json   ← fonte da verdade: segmentos, trim, giro, enquadre, cor, texto
render.py       ← lê o JSON e monta, com cache por segmento
broll/          ← os 7 clipes 4K
falas/          ← vazio (LEIA-ME com os nomes exatos)
musica/         ← vazio, faixa já preparada no render (LEIA-ME)
graficos/       ← PNGs gerados automaticamente
output/         ← os MP4
_cache/         ← intermediários (não versionado)
```

**Trocar um B-roll:** mude `origem` no `timeline.json`. Só isso.
**Trocar uma fala:** ponha o arquivo em `falas/`. Só isso.

O cache é por segmento: trocar um bloco re-renderiza um bloco, não o vídeo.

```bash
python3 render.py --preview   # 540×960, rápido
python3 render.py             # 1080×1920 final
python3 render.py --do-zero   # ignora o cache
```

---

## Acabamento

**Cor — decupada da referência por medição.** Cada clipe tem o balanço de
branco corrigido pra um alvo comum (os 7 iam de −0,130 na fachada a +0,130 na
prateleira); por cima, um look que persegue os números da referência.

| | Referência | v1 | **v2** |
|---|---|---|---|
| luma média | 0,430 | 0,530 | **0,435** |
| contraste (p95−p5) | 0,716 | 0,667 | **0,709** |
| saturação | 0,235 | 0,158 | **0,257** |
| sombras R−B | −0,061 | −0,020 | **−0,055** |
| meios R−B | +0,039 | +0,019 | **+0,041** |
| altas R−B | +0,056 | −0,002 | **+0,038** |
| pixels estourados | 0,015% | 0,162% | **0,006%** |

A assinatura é o **split tone**: sombra fria, meio-tom neutro, alta quente.
O topo da curva em 0,950 e o ponto 0,92 em 0,890 são a proteção do jaleco e dos
dentes — o v2 estoura **menos** que a própria referência.
Preto em 0,005 na curva: 3,5% de pixels quase pretos contra 4,9% da referência —
fica com preto de verdade, mas ainda do lado levantado que você pediu.

**Giro e enquadre.** Tudo descrito em `timeline.json` como `rotacao` + `zoom /
cx / cy` relativos. O render calcula sozinho o zoom mínimo pra não entrar canto
preto depois do giro, e prende o recorte dentro da área válida.

**Movimento.** Punch-in de 2–4% nos planos parados, no lugar de estabilizar.
Não usei `vidstab`: neste build ele deforma a imagem em pan de mão.

**Tipografia.** Três papéis, e só três:

| Papel | Face | Uso |
|---|---|---|
| marcador | Instrument Sans Bold 34, caixa alta, teal, tracking 8 | `01`–`04`, numeração de capítulo |
| pergunta | **Instrument Serif 116** | a voz do vídeo — único papel grande |
| apoio | Instrument Sans 34, caixa alta, teal, tracking 4 | função e CTA |

Testei três tratamentos sobre o frame real antes de fixar: serifa editorial,
grotesk pesado (Work Sans) e condensada em caixa alta (Big Shoulders). Os dois
últimos ficaram genéricos e estouraram a margem segura. A serifa de alto
contraste é o que lê como premium em vídeo social e é o que combina com clínica.

Os marcadores são **numéricos de propósito** — não afirmam nada sobre a clínica,
só organizam.

**Entrada do texto:** fade de 0,30s + subida de 26px com ease-out cúbico em
0,5s. O véu não se move, só o texto. Véu de 960px no topo com alfa 195 e sombra
difusa de raio 22 — serifa de haste fina some em fundo movimentado sem isso.

**Cortes.** Secos, sem transição. Como na referência.

**Ritmo.** A referência tem 20 planos, mediana 1,90s, indo de **0,47s a 3,0s** —
o ritmo dela não é métrico, e é isso que separa montagem de template. O B-roll
aqui: `2,14 · 2,20 · 1,20 · 2,10 · 2,40 · 1,60 · 0,70 · 1,40` — mediana 1,85s,
desvio 0,55. O plano de **0,70s** (close do modelo de arcada) é o corte de
pontuação que quebra a regularidade.

**Áudio.** B-roll com ambiente em −26 dB. Fala em −16 LUFS por bloco. Música
com ducking por sidechain, disparado **só pelas falas reais**. Master −14 LUFS.

---

## Ritmo

Da referência que você mandou (a de 16:9 da outra clínica) vieram **o ritmo e a
cor**, os dois decupados por medição: blocos de fala alternando com B-roll curto,
corte seco, fala como espinha, durações irregulares, e o split tone de sombra
fria / alta quente. Os números estão na tabela acima.

**Nada da marca, da música, do visual de identidade ou do conteúdo dela foi
usado**, e nenhum trecho dela entra no vídeo.
