# falas/ — os 4 blocos de fala do Hugo

Enquanto esta pasta estiver vazia, cada bloco vira uma **cartela de placeholder**
com a duração prevista. Assim que o arquivo aparecer, ele entra no lugar com a
**duração real** e o resto da linha do tempo se reacomoda sozinho.

## Nomes exatos

| Arquivo | Bloco | Duração prevista | Entra em |
|---|---|---|---|
| `bloco1.mov` ou `.mp4` | FALA 1 | 10s | ~0:02 |
| `bloco2.mov` ou `.mp4` | FALA 2 | 12s | ~0:14 |
| `bloco3.mov` ou `.mp4` | FALA 3 | 11s | ~0:32 |
| `bloco4.mov` ou `.mp4` | FALA 4 | 9s | ~0:46 |

Põe os arquivos aqui e roda:

```bash
python3 render.py            # final
python3 render.py --preview  # rápido, pra conferir
```

Só o bloco que mudou é re-renderizado — o resto sai do cache.

## O que o render faz sozinho com a fala real

- Reenquadra pra 1080×1920 sem distorcer (lê o metadado de rotação do iPhone).
- Mesmo balanço de branco e mesmo look dos B-roll.
- Áudio: corta grave abaixo de 85 Hz, redução de ruído leve (`afftdn`, sem
  robotizar) e **normaliza em −16 LUFS** — é o que faz os 4 blocos ficarem no
  mesmo volume mesmo se você gravar em dias diferentes.
- A música abaixa sozinha embaixo da fala (ducking por sidechain).

## Como gravar pra encaixar

- Vertical **1080×1920 ou 4K vertical**, **30fps** (não misture 60fps).
- Hugo levemente fora de eixo, olhando pro entrevistador ou pra câmera — mas
  **o mesmo** nos 4 blocos.
- Microfone de lapela ou celular a menos de 40 cm.
- **Grave o dobro** de cada bloco. É melhor escolher do que aceitar.
- Deixe 1s de silêncio antes e depois de cada take (o corte precisa de ar).
- Mesma roupa, mesma luz, mesmo fundo nos 4 — eles vão aparecer intercalados,
  qualquer diferença salta.

## Legenda

Se existir `bloco1.srt` (idem 2, 3, 4), a legenda é queimada sincronizada,
branca com contorno preto fino, máx. 2 linhas, dentro da margem segura.

**Eu não consigo transcrever o áudio aqui** — não tenho reconhecimento de fala
neste ambiente. O .srt você gera no CapCut (legenda automática → exportar SRT)
ou escreve na mão. Se me mandar o texto com os tempos, eu monto o arquivo.
