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

---

# v3 — montagem no ritmo, música gerada no Kairogen (16,9 s, 507 quadros)

O cliente reprovou a v2 (texto e edição) e pediu algo diferente, com música
de fundo boa, usando os conectores.

## Música (Kairogen, 3 créditos cada)
Duas trilhas instrumentais de 22 s geradas: **A** sertanejo-funk (viola caipira,
bateria moderna, 808) e **B** hip-hop. A CDN do Kairogen está bloqueada no
proxy deste ambiente; os arquivos vieram pela função de download do próprio
conector e estão em `projetos/bastidor/assets/`. Escolhida a **A**: ~133 BPM
(batida 0,45 s, 1ª batida em 0,03 s), ganha energia em ~7 s e acaba sozinha
perto de 17 s. IDs: A `6abebcf07a12b76894c08db7`, B `6abebcfdbf204872071cbfd2`.

## Montagem (todo corte numa batida)

| Quadro | Tempo | Take | O quê |
|---|---|---|---|
| 0 | 0,00 | IMG_1459, 3,30 | Gancho: a mão molha o boné, ele põe e sorri. "POR TRÁS DA BRASA" |
| 109 | 3,63 | IMG_1455 | Virando a carne (2 batidas) |
| 136 | 4,53 | IMG_1456 | Potes com a marca |
| 163 | 5,43 | IMG_1457 | Carne indo pro saco |
| 190 | 6,33 | IMG_1471 | O soprador |
| 217 | 7,23 | Take novo | **Na virada da música**: embalando para os clientes, joinha (8 batidas) |
| 325 | 10,83 | IMG_1470 | Tenda cheia |
| 352 | 11,73 | IMG_1466 | Atendimento |
| 379 | 12,63 | IMG_1458 | A peça saindo da grelha. "O RESULTADO" |
| 460 | 15,33 | Vinheta | Logo |

## Texto
Anton (Google Fonts, OFL), maiúscula, branca com sombra dura, palavra-chave em
vermelho, entrada com pop. "POR TRÁS DA BRASA" no gancho, embaixo do rosto
(y 1250); "O RESULTADO" no topo, acima da carne (y 300).

## Cor
Documental cinematográfica: saturação −8 % com o vermelho da carne preservado,
amarelo da guia e verdes contidos, sombras levemente frias, altas quentes,
pretos foscos, vinheta sutil e grão fino.

## Som
A trilha manda; o som natural fica 9 dB abaixo, nivelado entre os takes.
Medido: −13,9 LUFS / −2,8 dBTP (com), −14,0 / −3,3 (sem música, só ambiente).

Entrega: `entrega/guerreiros-BASTIDOR-17s.mp4` e `-SEM-MUSICA`.
