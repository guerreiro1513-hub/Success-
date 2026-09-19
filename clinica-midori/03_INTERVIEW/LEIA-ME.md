# 03_INTERVIEW — vazio

Slot reservado no corte: **SLOT 03 — ENTREVISTA**, 3,6s (`P03` no `timeline.json`),
entre o bloco de procedimento e o respiro final.

## Como gravar pra encaixar sem retrabalho

- Vertical 1080×1920, 30fps (mesmo do resto — não misture 60fps).
- Plano médio, entrevistado levemente fora de eixo, olhando pro entrevistador.
- Grave **o dobro** do que precisa: o corte usa 3,6s, mas quero escolher o
  soundbite, não aceitar o único que existe.
- Microfone de lapela ou celular a menos de 40cm. Room tone da clínica é
  aceitável de fundo — está na camada de ambiência.
- Grave 10s de silêncio da sala no fim da tomada (serve de room tone limpo).

## O que acontece quando chegar

O bloco `P03` deixa de ser placeholder e vira um bloco com `fonte`/`in`. Se o
soundbite for mais longo que 3,6s, aumente `dur` em múltiplos de **0,6s**
(1,2 / 1,8 / 2,4 / 3,0 / 3,6 / 4,2 …) — a trilha continua sincronizada.
A segunda metade do soundbite recebe B-roll da clínica por cima (L-cut: o áudio
da entrevista continua enquanto a imagem já virou clínica).

Nada de falas inventadas: o texto sai do que a pessoa falar.
