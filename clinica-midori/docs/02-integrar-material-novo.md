# 02 · Como integrar o material novo (sem refazer nada)

O corte não é um MP4 que alguém vai reabrir e remontar. Ele é
**`timeline.json` + `build.py`**. Material novo entra editando o JSON.

## Caso 1 — chegou footage pra um slot placeholder

Exemplo: gravaram a equipe (SLOT 01).

1. Jogue o arquivo em `02_CLINIC_FOOTAGE/` com nome descritivo:
   `06_equipe-recepcao.mov`
2. Em `timeline.json`, adicione a fonte:

```json
"EQUIPE": {
  "arquivo": "02_CLINIC_FOOTAGE/06_equipe-recepcao.mov",
  "dur_util": 9.4,
  "grade": "colorbalance=rm=-0.03:bm=0.04,eq=brightness=0.02"
}
```

3. Troque o bloco `P01` por um bloco de plano real — **mantendo o `dur`**:

```json
{ "id": "S06b", "secao": "EQUIPE", "rotulo": "EQUIPE", "fonte": "EQUIPE",
  "in": 2.30, "dur": 1.8, "estab": true, "push": 1.03 }
```

4. `python3 build.py`

Só esse plano re-renderiza (o resto sai do cache). Segundos, não minutos.

## Caso 2 — chegou a entrevista

A entrevista **não é um bloco só**: são 5 (`P01`, `P02`, `P04`, `P05`, `P08`).
Foi assim que a referência foi montada — a fala é a espinha e o B-roll entra
por cima dela. Cada slot tem no `timeline.json` o briefing do que aquele
soundbite precisa cobrir.

Mesma mecânica do caso 1, com duas diferenças:

- **`dur` pode crescer**, mas só em múltiplos de **0,3s**: 2,4 → 2,7 → 3,0 → 3,3.
  Fora da grade a trilha sai de sincronia.
- Parte de cada soundbite recebe B-roll por cima (L-cut): a imagem já virou
  clínica enquanto o áudio da fala continua. Isso vira dois blocos no JSON.
  Me mande os arquivos que eu escolho os soundbites e monto.

## Caso 3 — quer trocar um plano que já existe

Mexa em `in` (onde começa na fonte). Não mexa em `dur` se não precisar.
Rode `build.py`.

## Caso 4 — quer ajustar a cor

Os números que o corte persegue estão em `docs/00-blueprint.md`, medidos na
referência. Dois botões diretos no `show_look` do `timeline.json`:

- **mais/menos vibrante:** `saturation=0.70`. Baixar pra `0.62` fecha o número
  da referência; subir pra `0.80` deixa mais vivo que ela.
- **mais/menos quente:** os pares `rs/bs` (sombras) e `rh/bh` (altas) do
  `colorbalance`. Sombra fria + alta quente é a assinatura do look.

Para mexer numa sala só, mexa no `colorchannelmixer` daquela fonte. Cuidado
com a recepção: ganho de azul acima de ~1,40 faz o verde do logo virar azul.

## Regras que não podem quebrar

| Regra | Motivo |
|---|---|
| Duração múltipla de **0,3s** | sincronia com a trilha de 100 BPM |
| Gravar tudo **1080×1920 · 30fps** | 60fps misturado dá judder no concat |
| `push` no máximo **1,12×** | acima disso parece zoom de template |
| **1** speed ramp no filme | já está usado no `S09` |
| Nada de texto com número, prazo, preço ou promessa clínica | não tem respaldo e é risco com CFO/CRO |

## Comandos

Os `.wav` não vão pro git (são gerados por script). O `build.py` refaz sozinho
o que estiver faltando — basta rodar.

```bash
python3 build.py                       # monta os dois cortes
python3 06_GRAPHICS/make_graphics.py   # refaz as cartelas (só se mudar texto)
python3 05_SOUND_DESIGN/make_sound.py  # refaz ambiência/transições
python3 04_MUSIC/make_music.py         # refaz a trilha scratch
python3 build.py --versao limpo        # só o assistível
python3 build.py --estab              # liga a estabilização (leia o aviso no blueprint)
python3 build.py --do-zero             # ignora o cache
```
