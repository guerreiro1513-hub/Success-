# CLÍNICA MIDORI — Reel institucional 9:16 · CORTE v2 (decupado da referência)

**Formato:** 1080×1920 · 30fps · 100 BPM (grade de corte de 0,3s)
**Destino:** Instagram Reels / TikTok

---

## O que mudou da v1 pra v2

A referência chegou. Ela é um filme institucional de clínica odontológica,
**16:9 horizontal, 44,3s**, movido por entrevista. Análise completa em
[`01_REFERENCE/ANALISE.md`](01_REFERENCE/ANALISE.md).

Três coisas mudaram, todas medidas e não chutadas:

**1. Cor.** O look agora persegue os números da referência. Sombra fria,
meio-tom e alta quentes — split tone contido, que é a assinatura dela.

| | Referência | v1 | v2 |
|---|---|---|---|
| luma média | 0,430 | 0,329 | **0,415** |
| contraste | 0,716 | 0,643 | **0,703** |
| sombras R−B | −0,062 | +0,059 | **−0,063** |
| altas R−B | +0,055 | +0,034 | **+0,070** |
| pretos | 5,0% | 8,4% | **5,3%** |
| saturação | 0,235 | 0,461 | 0,286 |

A correção de cada sala não foi escolhida no olho: é a solução analítica que
leva o meio-tom daquela sala ao alvo da referência.

**2. Ritmo.** A v1 era metronômica — cinco planos seguidos de exatamente 1,8s.
A referência tem plano de 0,47s e de 3,0s no mesmo filme. A v2 varia
`2,1 · 1,8 · 0,6 · 1,2 · 1,8 · 0,9 · 3,0 · 0,9 · 1,5 · 1,8 · 1,2 · 3,0`,
com desvio de durações **0,74** contra **~0,67** da referência.

**3. A entrevista virou espinha.** Na referência ela volta ~6 vezes e todo o
B-roll é cutaway por cima da fala. A v1 tratava entrevista como um bloco único
de 3,6s. A v2 tem **5 blocos**, cada um com o briefing do que aquele soundbite
precisa cobrir.

Também: **todos os dissolves saíram.** A referência é corte seco em tudo.

---

## Três coisas pra você saber

**1. A referência é 16:9 horizontal, seu material é 9:16 vertical.** O corte
ficou em 9:16 — recortar vertical pra 16:9 jogaria fora 3/4 do quadro e
Reels/TikTok penalizam vídeo deitado. Foi importada a linguagem, não a
proporção.

**2. Metade da referência é gente, e você não tem nenhuma.** Dentista falando,
paciente na cadeira, mãos trabalhando. Nos seus 5 clipes não tem uma pessoa.
Por isso **9 dos 21 blocos são slot**. Não inventei nada pra preencher.

**3. A parte "cinematográfica" que não é montagem.** A referência tem
profundidade de campo rasa, luz controlada e movimento de gimbal — isso é
câmera, não edição. O corte reproduz ritmo, estrutura e cor. O resto depende
de como o próximo material for gravado.

**4. A trilha é scratch.** Sintetizada por código, original e sem risco de
copyright, mas não é qualidade de publicação. Leia [`docs/03-trilha.md`](docs/03-trilha.md).

---

## Os arquivos

| `08_FINAL/` | Duração | Pra quê |
|---|---|---|
| `MIDORI_ref-v2_LIMPO.mp4` | 19,8s | Só o que existe hoje. **Esse dá pra assistir e mostrar.** |
| `MIDORI_ref-v2_ESTRUTURA.mp4` | 39,0s | Documento de trabalho: mostra os 9 slots com o briefing de cada um. **Não é pra postar.** |
| `MIDORI_base-v1_*.mp4` | — | Versão anterior, guardada só pra comparação |

---

## Estrutura

```
[FACHADA] → PLACA → ENTRADA → pontuação → [ENTREVISTA 1] → B-roll
→ [ENTREVISTA 2] → [PROCEDIMENTO] → [ENTREVISTA 3] → clínico
→ [ENTREVISTA 4] → [SORRISO] → [EQUIPE] → detalhes → [ENTREVISTA 5] → MARCA
```

Decupagem plano a plano: [`docs/01-decupagem.md`](docs/01-decupagem.md).

---

## Como isso continua sendo uma base flexível

```
timeline.json   ← a fonte da verdade (planos, in/out, cor, ritmo)
build.py        ← monta os dois cortes, com cache por plano
```

Material novo entra editando o JSON. Só o plano alterado re-renderiza.
Passo a passo em [`docs/02-integrar-material-novo.md`](docs/02-integrar-material-novo.md).

---

## Pastas

| | |
|---|---|
| `01_REFERENCE/` | a referência + a análise medida dela |
| `02_CLINIC_FOOTAGE/` | os 5 clipes, renomeados e sem a tarja do CapCut |
| `03_INTERVIEW/` | vazio — instruções de gravação no LEIA-ME |
| `04_MUSIC/` | trilha scratch + o script que a gera |
| `05_SOUND_DESIGN/` | ambiência real da clínica + transições |
| `06_GRAPHICS/` | cartelas, etiquetas, CTA + o script que gera |
| `07_LOGO/` | vazio — o corte usa a placa física da parede |
| `08_FINAL/` | os MP4 |
| `_render/` | intermediários e cache (não versionado) |

---

## O que gravar na próxima ida

Em ordem de impacto no corte:

1. **Entrevista — 5 soundbites.** Vertical 1080×1920 30fps, plano médio,
   lapela. Os cinco briefings estão nas cartelas do corte ESTRUTURA e no
   `timeline.json`: abertura, diferencial, frase de impacto (1s), cuidado com
   o paciente, fechamento. Grave o dobro de cada um.
2. **Fachada** — a referência abre com 3,0s aqui. Fim de tarde, luz quente.
3. **Procedimento** — mãos com luva e instrumento em close, luz do refletor.
   Sem rosto identificável sem autorização assinada.
4. **Sorriso do paciente** — o elemento humano que fecha a promessa.
5. **Equipe** — profissional de jaleco trabalhando, concentrado. 2 tomadas.

Padrão obrigatório: **1080×1920, 30fps**, pan devagar e na mesma direção,
6 a 8 segundos por tomada.
