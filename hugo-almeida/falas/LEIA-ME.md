# falas/ — os blocos de fala do Hugo

## O que chegou

Vieram **3 blocos, com 2 tomadas cada** (6 arquivos), não 4 blocos. Escolhi uma
tomada de cada; as outras três ficaram em `tomadas-nao-usadas/`.

| Arquivo | Origem | Cenário | Trecho usado | Por que esta tomada |
|---|---|---|---|---|
| `bloco1.mov` | IMG_2072 (tomada 2) | em pé, corredor | 0,15 → 10,60s | a tomada 1 termina com ele saindo de quadro |
| `bloco2.mov` | IMG_2115 (tomada 1) | sentado, ao lado da tela do escaneamento | 0,45 → 5,95s | a tomada 2 começa com ele de costas pra câmera |
| `bloco3.mov` | IMG_2086 (tomada 1) | sentado, consultório | 0,15 → 10,40s | a tomada 2 termina com ele olhando pra baixo |

## ⚠️ A ordem dos blocos é um palpite

**Não consigo transcrever o áudio aqui** — o proxy bloqueia o download do
modelo de reconhecimento de fala (`huggingface.co` responde 403). Então atribuí
os blocos **pelo cenário**, não pelo que você fala:

- `bloco1` (em pé, corredor) → responde **"Quem é o Hugo?"** — parece a chegada
- `bloco2` (ao lado da tela) → responde **"O que ele faz de diferente?"** —
  casa com o B-roll de tecnologia que vem logo depois
- `bloco3` (sentado, calmo) → responde **"Pra quem é o tratamento?"**

**Se a ordem estiver errada, é só renomear os arquivos** (`bloco1.mov` ↔
`bloco3.mov`, por exemplo) e rodar `python3 render.py`. Leva segundos: só os
blocos trocados são re-renderizados.

## O 4º bloco não existe

O roteiro previa 4 falas. Como vieram 3, o CTA deixou de ser fala e virou o
**fecho em B-roll**: um plano novo da recepção (`S8`) com "Agende sua avaliação
/ WhatsApp" por cima. Faz par com a fachada da abertura.

Se você gravar o 4º bloco, me manda que eu devolvo a fala e mantenho ou não o
fecho — o `timeline.json` aceita os dois.

## O que o render fez com o áudio

O áudio chegou a **−36 LUFS** (muito baixo — parece mic do celular, não lapela).
Subir 20 dB sobe o chiado junto, então: corte abaixo de 85 Hz, redução de ruído
`afftdn` em nr=16 e **loudnorm de duas passadas** em −16 LUFS por bloco.

Resultado: −16,7 / −16,3 / −16,2 LUFS. Antes, com loudnorm de uma passada, a
diferença entre blocos era de 1,2 LU — degrau audível no corte.

## O que o render fez com a cor

O balanço de branco foi resolvido **contra o tom de pele**, não contra a sala.
Corrigindo pela parede, o rosto saía **verde** (R−G de −0,06 nos blocos 2 e 3).
Agora: R−G de +0,083 a +0,098, dentro da faixa natural.

## Legenda

Se existir `bloco1.srt` (idem 2 e 3), é queimada sincronizada, branca com
contorno preto fino, dentro da margem segura.

Como eu não transcrevo aqui, o .srt sai do CapCut (legenda automática →
exportar SRT) ou você me manda o texto com os tempos que eu monto o arquivo.

## Pra gravar o que faltar

- Vertical, **30fps**, mesma roupa e mesma luz.
- **Mic de lapela de verdade, colado** — o nível atual está 20 dB baixo demais.
- 1s de silêncio antes e depois de cada take.
- Grave o dobro.
