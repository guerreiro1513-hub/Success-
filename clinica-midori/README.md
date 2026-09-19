# CLÍNICA MIDORI — Reel institucional 9:16 · CORTE BASE v1

**Formato:** 1080×1920 · 30fps · 100 BPM (grade de corte de 0,6s)
**Destino:** Instagram Reels / TikTok

---

## Leia isto primeiro

**1. A referência não chegou.** Os 5 arquivos enviados são todos gravação da
clínica. Os cinco têm o mesmo perfil de export, áudio só de room tone
(−31 a −43 LUFS, sem trilha) e 2s de tarja do CapCut no fim — nenhum é um reel
montado por outra pessoa. O corte foi construído sobre o blueprint documentado
em `docs/00-blueprint.md`, não sobre a referência. Mande o arquivo em
`01_REFERENCE/` que eu redecupo e reajusto — sem remontar do zero.

**2. Metade da estrutura é buraco, e é buraco de material que não existe.**
Não tem **nenhuma pessoa** nos 5 clipes: nem dentista, nem equipe, nem paciente,
nem mão, nem sorriso, nem procedimento, nem fachada. Os 4 slots
(`EQUIPE`, `PROCEDIMENTO`, `ENTREVISTA`, `SORRISO`) estão marcados como cartela
no corte ESTRUTURA. Não inventei nada pra preencher.

**3. A trilha é scratch.** Sintetizada aqui por código, original e sem risco de
copyright, mas não é qualidade de publicação. Serve pra travar o ritmo.
Leia `docs/03-trilha.md`.

---

## Os dois arquivos

| `08_FINAL/` | Duração | Pra quê |
|---|---|---|
| `MIDORI_base-v1_ESTRUTURA.mp4` | 29,4s | Documento de trabalho. Mostra a estrutura inteira com os 4 buracos explícitos e uma etiqueta de leitura em cada plano. **Não é pra postar.** |
| `MIDORI_base-v1_LIMPO.mp4` | 19,8s | Só o que existe hoje. Sem cartela, sem etiqueta. **Esse dá pra assistir e mostrar.** |

---

## Estrutura

```
CLÍNICA → AMBIENTE → [EQUIPE] → CLÍNICO → DETALHE → [PROCEDIMENTO]
        → [ENTREVISTA] → RESPIRO → [HUMANO] → MARCA
```

Decupagem plano a plano: `docs/01-decupagem.md`.

---

## Como isso é uma base flexível

O corte **não** é um MP4 pra alguém reabrir e remontar. É:

```
timeline.json   ← a fonte da verdade (planos, in/out, cor, transição)
build.py        ← monta os dois cortes a partir dele, com cache por plano
```

Material novo entra editando o JSON. Só o plano alterado re-renderiza — o resto
sai do cache. Passo a passo em `docs/02-integrar-material-novo.md`.

---

## Pastas

| | |
|---|---|
| `01_REFERENCE/` | vazio — a referência não chegou |
| `02_CLINIC_FOOTAGE/` | os 5 clipes, renomeados e **sem a tarja do CapCut** |
| `03_INTERVIEW/` | vazio — instruções de gravação no LEIA-ME |
| `04_MUSIC/` | trilha scratch + o script que a gera |
| `05_SOUND_DESIGN/` | ambiência real da clínica + transições |
| `06_GRAPHICS/` | cartelas, etiquetas, CTA + o script que gera |
| `07_LOGO/` | vazio — o corte usa a placa física da parede |
| `08_FINAL/` | os dois MP4 |
| `_render/` | intermediários e cache (não versionado) |

---

## O que gravar na próxima ida

Em ordem de impacto no corte:

1. **Entrevista** (SLOT 03, 3,6s no corte) — vertical, plano médio, lapela,
   grave o dobro do que precisa + 10s de sala em silêncio no fim.
2. **Equipe** (SLOT 01, 1,8s) — 2 tomadas: recepção atendendo alguém e
   profissional de jaleco caminhando.
3. **Procedimento** (SLOT 02, 2,4s) — mãos e instrumento em close, luz do
   refletor. Sem rosto identificável sem autorização assinada.
4. **Sorriso/paciente** (SLOT 04, 1,8s) — o elemento humano que fecha.
5. **Fachada** — não tem plano externo nenhum. Fim de tarde, luz quente.

Padrão obrigatório: **1080×1920, 30fps**, pan na mesma direção (pra direita) e
devagar, 6 a 8 segundos por tomada.
