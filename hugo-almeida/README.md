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

**Cor.** Cada clipe tem o balanço de branco **medido e corrigido** pra um alvo
comum (meio-tom R−B +0,010) — os 7 estavam de −0,130 (fachada, céu azul) a
+0,130 (prateleira, tungstênio). Por isso parecem gravados no mesmo dia.
Por cima, um look leve: contraste 1,06, saturação 0,96, preto levantado em
0,030 e o topo da curva puxado pra 0,982 — é o que impede o jaleco e os dentes
de estourarem. Sombra levemente fria.

**Giro e enquadre.** Tudo descrito em `timeline.json` como `rotacao` + `zoom /
cx / cy` relativos. O render calcula sozinho o zoom mínimo pra não entrar canto
preto depois do giro, e prende o recorte dentro da área válida.

**Movimento.** Punch-in de 2–4% nos planos parados, no lugar de estabilizar.
Não usei `vidstab`: neste build ele deforma a imagem em pan de mão.

**Cortes.** Secos, sem transição. Como na referência de ritmo.

**Áudio.** B-roll com ambiente em −26 dB. Fala em −16 LUFS por bloco. Música
com ducking por sidechain, disparado **só pelas falas reais**. Master −14 LUFS.

---

## Ritmo

Da referência que você mandou (a de 16:9 da outra clínica), usei **só o ritmo**:
blocos de fala alternando com B-roll de 1,5–2,5s, corte seco, e a fala como
espinha. Medido lá: 20 planos, mediana 1,90s. Aqui o B-roll tem mediana 2,0s.
Nada da marca, da música, do visual ou do conteúdo dela foi usado.
