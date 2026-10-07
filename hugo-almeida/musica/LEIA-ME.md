# musica/ — faixa de trilha

A faixa está **preparada e vazia**, como combinado. O render já tem o barramento
de música com ducking automático sob as falas; falta só o arquivo.

## Como usar

Ponha a faixa aqui com o nome **`trilha.wav`** (ou `.mp3`/`.m4a` e aponte o
caminho em `timeline.json` → `audio.musica`) e rode `python3 render.py`.

Enquanto não existir, o render avisa `trilha ausente` e a faixa fica em silêncio
— o vídeo sai normal, só sem música.

## O que já está configurado

| | |
|---|---|
| Nível da música | −21 dB |
| Ducking | sidechain, ratio 8:1, threshold 0,045, attack 20 ms, release 400 ms |
| Chave do ducking | **só as falas reais** — B-roll e cartela não abaixam a música |
| Fade | 1,2s na entrada, 1,6s na saída |
| Master | −14 LUFS, true peak −1,3 dBTP |

A faixa é loopada e cortada automaticamente no tamanho do vídeo, então não
precisa ter a duração certa.

## Escolha

Instrumental suave, sem vocal, sem batida forte. Categoria: *corporate calm*,
*minimal piano*, *ambient*. Fuja de trilha de "vídeo médico" — é o clichê.
Fontes com licença comercial: Epidemic Sound, Artlist, ou a biblioteca do
próprio Instagram/CapCut.

Se a faixa tiver um crescendo, alinhe o pico com o começo do bloco 4 (a parte do
convite). Me avisa que eu ajusto o corte da trilha pra isso.
