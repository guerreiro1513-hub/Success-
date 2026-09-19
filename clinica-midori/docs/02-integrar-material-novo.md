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

Mesma coisa no `P03`, com duas diferenças:

- **`dur` pode crescer**, mas só em múltiplos de **0,6s**: 3,6 → 4,2 → 4,8 → 5,4.
  Fora da grade a trilha sai de sincronia.
- A segunda metade do soundbite recebe B-roll por cima (L-cut). Isso vira dois
  blocos: o primeiro com a imagem da entrevista, o segundo com um plano de
  clínica enquanto o áudio continua. Me mande o arquivo que eu escolho o
  soundbite e monto.

## Caso 3 — quer trocar um plano que já existe

Mexa em `in` (onde começa na fonte). Não mexa em `dur` se não precisar.
Rode `build.py`.

## Caso 4 — chegou a referência

Aí o que muda é a gramática: duração dos planos, ordem das seções, onde entra
dissolve, e a cor (`show_look`). Continua sendo edição de `timeline.json`.
Os clipes, o grafismo, a trilha e os scripts continuam valendo.

## Regras que não podem quebrar

| Regra | Motivo |
|---|---|
| Duração múltipla de **0,6s** | sincronia com a trilha de 100 BPM |
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
