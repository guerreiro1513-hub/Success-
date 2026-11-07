# PHASE 1 — INVENTÁRIO

Pasta de brutos: `hugo-almeida/broll/` + `hugo-almeida/falas/`
(`{RAW_CLIPS_PATH}` não foi preenchido; usei a pasta do projeto.)

## 1.1 Ficha técnica

| arquivo | dur | resolução real | fps | codec | áudio |
|---|---|---|---|---|---|
| `broll/01_fachada.mov` | 00:05.50 | 2160x3840 (rot -90) | 29.97 | hevc | aac 48000Hz stereo |
| `broll/02_recepcao.mov` | 00:05.86 | 2160x3840 (rot -90) | 29.02 | hevc | aac 48000Hz stereo |
| `broll/03_tecnologia-scanner.mov` | 00:06.13 | 2160x3840 (rot -90) | 30 | hevc | aac 48000Hz stereo |
| `broll/04_tecnologia-alinhador.mov` | 00:04.40 | 2160x3840 (rot -90) | 30 | hevc | aac 48000Hz stereo |
| `broll/05_quadros.mov` | 00:04.22 | 2160x3840 (rot -90) | 59.98 | hevc | aac 48000Hz stereo |
| `broll/06_prateleira-premio.mov` | 00:03.25 | 2160x3840 (rot -90) | 59.97 | hevc | aac 48000Hz stereo |
| `broll/07_instrumentos.mov` | 00:04.07 | 2160x3840 (rot -90) | 29.98 | hevc | aac 48000Hz stereo |
| `falas/bloco1.mov` | 00:10.77 | 2160x3840 (rot -90) | 30 | hevc | aac 48000Hz stereo |
| `falas/bloco2.mov` | 00:06.68 | 2160x3840 (rot -90) | 30.10 | hevc | aac 48000Hz stereo |
| `falas/bloco3.mov` | 00:10.50 | 2160x3840 (rot -90) | 30 | hevc | aac 48000Hz stereo |
| `falas/tomadas-nao-usadas/bloco1_tomada2.mov` | 00:10.64 | 2160x3840 (rot -90) | 30.08 | hevc | aac 48000Hz stereo |
| `falas/tomadas-nao-usadas/bloco2_tomada2.mov` | 00:06.63 | 2160x3840 (rot -90) | 30 | hevc | aac 48000Hz stereo |
| `falas/tomadas-nao-usadas/bloco3_tomada2.mov` | 00:10.37 | 2160x3840 (rot -90) | 30.10 | hevc | aac 48000Hz stereo |

Todos os brutos são **4K vertical** (2160x3840 após a rotação de −90 do metadado)
e HEVC. **fps misto** — 29,02 / 29,97 / 29,98 / 30 / 30,08 / 30,10 / 59,97 / 59,98.
Conforme §5, tudo é reenquadrado em resolução de origem e só desce para 1080x1920
no fim; e tudo é normalizado para 30 fps CFR.

## 1.2 Classificação

| clipe | classe | conteúdo (5 palavras) |
|---|---|---|
| `falas/bloco1.mov` | **A-ROLL-STANDING** | Hugo em pé, corredor, jaleco |
| `falas/bloco1_tomada2.mov` | A-ROLL-STANDING | idem; termina saindo de quadro |
| `falas/bloco2.mov` | **A-ROLL-SEATED** | Hugo sentado, tela do escaneamento |
| `falas/bloco2_tomada2.mov` | A-ROLL-SEATED | idem; começa de costas |
| `falas/bloco3.mov` | **A-ROLL-SEATED** | Hugo sentado, prateleira ao fundo |
| `falas/bloco3_tomada2.mov` | A-ROLL-SEATED | idem; termina olhando pra baixo |
| `broll/01_fachada.mov` | B-ROLL | fachada, placa da clínica, céu |
| `broll/02_recepcao.mov` | B-ROLL | balcão, sofá, lustre, recepção |
| `broll/03_tecnologia-scanner.mov` | B-ROLL | notebook com escaneamento 3D |
| `broll/04_tecnologia-alinhador.mov` | B-ROLL | mãos enluvadas, alinhador, notebook |
| `broll/05_quadros.mov` | B-ROLL | quadros, orquídea, modelos coloridos |
| `broll/06_prateleira-premio.mov` | B-ROLL | prateleira, modelos de arcada, placa |
| `broll/07_instrumentos.mov` | B-ROLL | bandeja de instrumentos esterilizados |

## 1.3 Sinalizações de compliance

| # | clipe | problema | regra | ação |
|---|---|---|---|---|
| **C1** | `broll/06_prateleira-premio.mov` | A placa do prêmio está em quadro e legível: **"Top Doctor 2023 — invisalign · iTero · exocad"** | **H7** (nunca a palavra Invisalign) e **H9** (sem close em prêmio) | reenquadrar para fora, ou descartar o clipe |
| **C2** | `broll/05_quadros.mov` | Mesma placa, recortada no canto inferior esquerdo. A marca não fica legível, mas parte do prêmio aparece | H9 | subir o enquadramento e excluir de vez |
| C3 | `broll/03_tecnologia-scanner.mov` | cabeça de terceiro no canto inferior esquerdo | H8 | já fora pelo enquadramento (zoom 1,55 / cx 0,36) — reconferir |
| C4 | `broll/07_instrumentos.mov` | pessoa sentada no alto à esquerda | H8 | já fora pelo enquadramento (zoom 1,75 / cx 0,68) — reconferir |
| C5 | `IMG_1733`, `IMG_1744` | pacientes | H8 | **não estão no projeto**, nunca foram importados |
| C6 | `broll/01_fachada.mov` | placa "Clínica MIDORI 3052-6703" | — | é a marca do próprio cliente, permitido |

`06_prateleira-premio.mov` só é aproveitável no recorte fechado dos modelos de
arcada (o que o corte chamava de `S6b`), onde a placa fica fora de quadro.
