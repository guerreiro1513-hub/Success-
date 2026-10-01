# Bastidor Tranquilo — 18,1 s

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
| copy_231F… (novo) | 15,4 s | Exportação do CapCut, 1080p. O dono embalando a carne para os clientes, gente em volta, joinha. Logo do CapCut a partir de ~13 s | **Principal** (bastidor de verdade) |

**Fala:** nenhum take tem fala clara (medido por detecção de voz: só conversa
de fundo). Sem legenda.

**Texto:** uma linha só, "bastidores do Guerreiro's Grill", TikTok Sans
SemiBold 50 px, branca com sombra suave, no topo, de 0,27 a 3,2 s. Pedido do
cliente pensando no gancho dos 3 s (a maioria assiste sem som). Nada inventado:
dia, horário e lugar não foram confirmados, então não entram.

## Linha do tempo (30 fps, 543 quadros)

v2: o boné vira o gancho (pedido do cliente), entra o take novo, o soprador
(IMG_1471) sai.

| Quadro | Tempo | Dura | Take | O quê |
|---|---|---|---|---|
| 0 | 0,00 | 5,70 | IMG_1459, 2,30 | A mão molhando o boné na mangueira (curiosidade), ele põe o boné, olha e sorri |
| 171 | 5,70 | 3,00 | IMG_1455, 0,50 | Mãos virando a carne na grelha |
| 261 | 8,70 | 4,50 | Take novo, 0,50 | Embalando a carne para os clientes, joinha |
| 396 | 13,20 | 3,33 | IMG_1458, 1,40 | A peça de carne saindo da grelha |
| 496 | 16,53 | 1,57 | Vinheta | Logo |

O take novo usa o mapeamento quadro a quadro (exportação do CapCut); nenhum
quadro repetido.

## Cor
Documental: contraste 1,06, saturação 1,03, balanço levemente quente, altas
seguradas. Sem empurrar vermelho/laranja.

## Som
Som natural de cada take, nivelado entre si, emendas de 20 ms nos cortes, redução de ruído leve e compressão 2:1.
Versão com trilha: gaúcha (sintetizada no repositório) 16 dB abaixo do
ambiente, sobe um pouco no logo. Medido: −15,1 LUFS / −4,2 dBTP (com),
−14,9 LUFS / −4,1 dBTP (sem).

## Entrega
- `entrega/guerreiros-BASTIDOR-18s.mp4`
- `entrega/guerreiros-BASTIDOR-18s-SEM-MUSICA.mp4`
