# O corte real — a virada do projeto

Depois de ver os dois vídeos reais do cliente, ficou claro que a direção
anterior estava errada. Este documento registra o quê e por quê.

---

## O erro

Eu construí a campanha inteira em cima de **4 fotos**, e as fotos me deram uma
leitura errada do negócio. Assumi:

| Assumi | É de verdade |
|--------|--------------|
| Picanha como protagonista | **Frango assado inteiro** é o carro-chefe, junto de costela e espetos |
| Estúdio noturno, fundo preto | **Rua, luz do dia**, sol forte, árvores, carros passando |
| Peça única sobre tábua escura | **Fartura** — grelha gigante lotada, dezenas de peças |
| Silêncio cinematográfico | Operação movimentada, equipe trabalhando, cliente na calçada |

Os clipes gerados por IA ficaram com "cara de IA" não só por acabamento —
ficaram porque **não eram o negócio dele**. Nenhuma quantidade de refinamento
de prompt corrigiria isso.

## O que o material real mostra

- Estrutura de rua: reboque/defumador preto grande na calçada, toldo
  "Espetos e Churrasco", banner da marca
- Luz do dia, sol duro, verde das árvores, rua ao fundo
- Frangos inteiros dourados, costela, espetos, carnes glaceadas
- **Acompanhamentos**: potes de maionese empilhados
- Equipe de avental com o logo e luva preta
- Marca d'água `@GUERREIROSGRILL` no material dele

## Correção de marca

O nome é **GUERREIRO'S GRILL**, com apóstrofo — extraído do logo em
`referencias/logo-guerreiros-grill.jpg`, tirado do frame aos 19,8s do vídeo A.
Toda a documentação anterior escrevia "GUERREIROS GRILL".

Assinatura oficial: **CHURRASCO RAIZ** · WhatsApp 99818.8917

---

## O filme entregue

`entrega/guerreiros-grill-REAL-14s.mp4` — 14,13s · 1080×1920 · 30fps · H.264 · com áudio

100% filmagem real do cliente. Nenhum frame de IA.

| # | TC | Dur | Cena | Fonte |
|---|----|-----|------|-------|
| 1 | 00,0 | 1,7s | Hook — frango dourado em close | A @ 1,90 |
| 2 | 01,7 | 2,0s | A operação — defumador, fumaça, calçada | B @ 3,20 |
| 3 | 03,7 | 2,0s | Fartura — a grelha lotada vista de cima | B @ 13,40 |
| 4 | 05,7 | 1,8s | Brasa — frangos na grelha, espetos | A @ 10,40 |
| 5 | 07,5 | 2,2s | Corte — carne fatiada na tábua | B @ 18,20 |
| 6 | 09,7 | 2,2s | Serviço — tesoura no frango | B @ 24,00 |
| 7 | 11,9 | 2,2s | End card com o logo real | — |

**Legenda:** `CHURRASCO DE VERDADE.` de 05,9 a 07,4 · fade 0,25s

**Áudio:** som original das filmagens, normalizado a −16 LUFS por segmento,
com fades de 0,06s nas emendas. É ambiência real de churrasco — vale mais que
efeito sintético.

## Color grading aplicado

```
eq=contrast=1.11:brightness=0.005:saturation=1.06
curves=r='0/0 0.5/0.545 1/1':b='0/0 0.5/0.462 1/1'
vignette=PI/4.5
unsharp=5:5:0.5
```

Vermelho levantado e azul rebaixado nos meios-tons: calor sem virar banho de
laranja. Vinheta leve e leve nitidez.

## Defeitos corrigidos durante o render

1. **End card preto.** O filtro `zoompan` colapsava o quadro (brilho médio 2,0
   contra 17,5 do PNG original). Removido — o fade simples já basta e respeita
   o "não exagere nos efeitos" do briefing.
2. **Legenda invisível.** O PNG entrava como quadro único, então o `fade` com
   `st=5.9` nunca disparava. Corrigido com `-loop 1 -framerate 30`.

Ambos verificados por amostragem de frames no arquivo final.

---

## Versões adicionais (custo zero de crédito)

Montadas só com ffmpeg em cima da filmagem do cliente. Nenhuma geração nova.

### `entrega/guerreiros-grill-REAL-22s.mp4` — 21,7s
Versão longa, com o material que ficou de fora do corte de 14s.

| # | TC | Dur | Cena | Fonte |
|---|----|-----|------|-------|
| 1 | 00,0 | 1,7s | Hook — frango dourado | A @ 1,90 |
| 2 | 01,7 | 1,8s | Fachada — toldo "Espetos e Churrasco" | B @ 0,30 |
| 3 | 03,5 | 2,0s | O defumador com fumaça | B @ 3,20 |
| 4 | 05,5 | 2,0s | Equipe tirando a peça da grelha | B @ 20,40 |
| 5 | 07,5 | 2,2s | Fartura — a grelha lotada de cima | B @ 13,40 |
| 6 | 09,7 | 1,8s | Peça glaceada nos espetos **+ legenda** | A @ 7,00 |
| 7 | 11,5 | 1,8s | Frangos na brasa | A @ 10,40 |
| 8 | 13,3 | 1,6s | Maionese com o adesivo da marca | B @ 11,00 |
| 9 | 14,9 | 2,2s | Corte — carne fatiada na tábua | B @ 18,20 |
| 10 | 17,1 | 2,2s | Serviço — tesoura no frango | B @ 24,00 |
| 11 | 19,3 | 2,4s | End card | — |

**Legenda:** `CHURRASCO DE VERDADE.` de 09,9 a 11,4.

### `entrega/guerreiros-grill-REAL-14s-sem-texto.mp4` — 14,13s
O corte de 14s sem nenhuma legenda. Só imagem, som e end card.

### Defeito corrigido nesta rodada
O corte da "equipe" (B @ 7,60) derivava, dentro dos 2 segundos, para os potes de
maionese — repetindo o assunto do corte 8. Trocado por B @ 20,40, onde a equipe
levanta uma peça da grelha com vapor subindo. Verificado por amostragem de frame.

### Ainda não incorporado
A trilha instrumental gerada no Kairogen **não entrou** nestas versões: o arquivo
está no CDN, que a política de rede deste ambiente bloqueia. O áudio destes cortes
é o som original das filmagens. Para somar a trilha por baixo, é montar no CapCut
com o `music.mp3` da galeria.
