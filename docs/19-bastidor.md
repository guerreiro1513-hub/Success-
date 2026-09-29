# Bastidor Tranquilo — 16,9 s

Reel documental: a câmera chega e o dono já está trabalhando. Poucos cortes,
takes longos, som natural. O cliente pediu para renderizar direto (sem esperar
aprovação) e ajustar depois; ainda vão chegar mais takes.
Receita: `projetos/bastidor/project/build.sh` e `mix.py`.

## Inventário (9 takes, todos 4K vertical nativo)

| Take | Dura | O que acontece | Uso |
|---|---|---|---|
| IMG_1455 | 8,5 s | Grelha aberta, mãos virando a carne com pegador, fumaça | **Abertura** (ação já acontecendo) |
| IMG_1456 | 7,4 s | Mesa de potes com o adesivo da marca; a câmera sobe e mostra as churrasqueiras | Detalhe / transição |
| IMG_1457 | 4,7 s | Tirando pedaço de carne do espeto e colocando na embalagem | Detalhe |
| IMG_1458 | 4,8 s | A peça grande de carne saindo da grelha no garfo | **A carne (payoff)** |
| IMG_1459 | 8,0 s | Molha o boné na mangueira, põe na cabeça, olha para a câmera e sorri | **Principal**, o momento espontâneo |
| IMG_1466 | 2,3 s | Atendimento na tenda | Ambiente |
| IMG_1470 | 5,0 s | Tenda com clientes, movimento | Ambiente |
| IMG_1471 | 5,8 s | O dono com o soprador, movimento atrás; depois sai andando | Apoio |
| IMG_1473 | 1,8 s | Outro funcionário com o soprador | Pouco uso |

**Fala:** nenhum take tem fala clara (medido por detecção de voz: só conversa
de fundo). Sem legenda e sem texto de contexto (não há informação confirmada
de dia ou horário para escrever).

## Linha do tempo (30 fps, 507 quadros)

| Quadro | Tempo | Dura | Take | O quê |
|---|---|---|---|---|
| 0 | 0,00 | 3,50 | IMG_1455, 0,50 | Mãos virando a carne na grelha |
| 105 | 3,50 | 6,00 | IMG_1459, 2,00 | Boné na mangueira, põe na cabeça, olha e sorri. Take inteiro |
| 285 | 9,50 | 2,50 | IMG_1471, 0,30 | O soprador, o restaurante atrás |
| 360 | 12,00 | 3,33 | IMG_1458, 1,40 | A peça de carne saindo da grelha |
| 460 | 15,33 | 1,57 | Vinheta | Logo |

Aproximação no máximo 1,00→1,04, sem punch-in, sem transição de efeito.

## Cor
Documental: contraste 1,06, saturação 1,03, balanço levemente quente, altas
seguradas. Sem empurrar vermelho/laranja.

## Som
Som natural de cada take, nivelado entre si (o IMG_1459 veio ~10 dB mais
baixo), emendas de 20 ms nos cortes, redução de ruído leve e compressão 2:1.
Versão com trilha: gaúcha (sintetizada no repositório) 16 dB abaixo do
ambiente, sobe um pouco no logo. Medido: −15,2 LUFS / −3,8 dBTP (com),
−15,0 LUFS / −4,2 dBTP (sem).

## Entrega
- `entrega/guerreiros-BASTIDOR-17s.mp4`
- `entrega/guerreiros-BASTIDOR-17s-SEM-MUSICA.mp4`
