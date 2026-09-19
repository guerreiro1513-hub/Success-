# 00 · Blueprint de montagem

## Aviso de honestidade

**A referência não chegou.** Os 5 arquivos enviados são todos gravação da
clínica. Detalhe técnico que confirma: os cinco têm o mesmo perfil de export
(1080×1920, 30fps, HEVC, `Lavf57`), áudio só de room tone entre −31 e −43 LUFS
(reel editado teria trilha por volta de −14) e todos terminam com 2s de tarja
do CapCut. Nenhum é um vídeo montado por outra pessoa.

Então este blueprint **não** é a decupagem da sua referência — é a linguagem de
montagem padrão de reel institucional premium de clínica, que é o que dá pra
fazer com honestidade sem o arquivo. Quando a referência chegar, eu redecupo e
ajusto `timeline.json`. O que muda é duração de plano, ordem de seção e cor.
Os clipes, o grafismo, a trilha e os scripts continuam valendo.

---

## A gramática adotada

| Parâmetro | Decisão | Por quê |
|---|---|---|
| Duração | 29,4s (estrutura) · 19,8s (limpo) | Reel institucional respira; abaixo de 15s vira anúncio |
| Grade de corte | **0,6s** (1 tempo a 100 BPM) | Todo corte cai num tempo da trilha. É o que separa montagem intencional de corte aleatório |
| Plano médio | 1,8s (3 tempos) | Longo o bastante pra ler o espaço, curto pra não parar |
| Plano de aceleração | 1,2s (2 tempos) | Usado só em `S06` e `S07`, pra o ritmo subir entrando no bloco clínico |
| Assinatura | 3,0s (5 tempos) | O único plano que segura de verdade |
| Transições | corte seco por padrão | Dissolve só na borda de bloco e entrando na assinatura, nunca por enfeite. No corte LIMPO é **1 dissolve em 10 cortes**; no ESTRUTURA são 5, porque cada borda de placeholder ganha um — é o que faz o buraco ler como buraco |
| Speed ramp | **1 no filme inteiro** | `S09`, 1.0× → 0.7×, fechando no instrumental. Efeito a serviço da narrativa |
| Push in | 1,02× a 1,12×, nunca mais | Move sem parecer zoom de CapCut |
| Texto | 1 inserção, no fim | A placa física na parede já diz o nome. Texto por cima de texto é redundância |

## Progressão

```
CLÍNICA → AMBIENTE → [EQUIPE] → CLÍNICO → DETALHE → [PROCEDIMENTO]
        → [ENTREVISTA] → RESPIRO → [HUMANO] → MARCA
```

Os blocos entre colchetes são os 4 slots a gravar. **A clínica está estabelecida
no primeiro frame** — o corte abre com a câmera já chegando na placa da recepção,
não com um plano genérico.

## Lógica das transições

- **Corte casado por movimento (`S04→S05`).** Os dois lados são pan pra direita
  na mesma velocidade. O olho não registra o corte, registra a continuidade.
  Quase todo o material gravado tem pan pra direita — isso foi explorado de
  propósito, é o que amarra o corte.
- **Corte seco na batida.** Doze dos quinze pontos. Cai no tempo forte.
- **Dissolve de 6 frames** nas bordas de bloco (onde um placeholder começa ou
  termina) e de **8 frames** entrando na assinatura. No corte limpo sobra um só:
  o da assinatura. Quando o material novo entrar, a borda deixa de ser borda e
  o corte volta a ser seco — a não ser que o dissolve seja declarado de propósito.
- **Ambiência contínua por cima dos cortes** — o room tone real da clínica não
  corta junto com a imagem. É o J/L-cut da camada de som: o ouvido segue reto
  enquanto o olho corta.

## Cor

Correção por clipe primeiro (as 5 gravações têm temperatura diferente: recepção
em tungstênio amarelo, consultórios em fluorescente esverdeado, lounge escuro),
depois um look único por cima.

```
eq=contrast=1.04:saturation=1.12:gamma=1.03
curves=master='0/0.010 0.25/0.262 0.5/0.535 0.75/0.79 1/1'
unsharp=5:5:0.35   vignette=PI/5.4
```

Saturação em **+12%**, não mais. A riqueza vem do ganho de contraste no
meio-tom (a curva levanta o 0.25 pra 0.262 e o 0.5 pra 0.535) e da correção de
dominante por clipe — não de empurrar saturação. Verde da marca e azul das
cadeiras ganham; pele continua natural. Nada de cinza, nada de teal-and-orange.

## Estabilização: desligada, de propósito

O `vidstab` deste build deforma a imagem neste material — ele tenta remover o
**pan intencional** junto com o tremor e preenche a borda com conteúdo de frames
anteriores, o que derrete pedaços do quadro. O pan de mão das gravações já é
lento e regular o bastante. O código continua lá (`build.py --estab`), com
parâmetros conservadores, pro dia em que chegar material realmente trêmulo.

## Som

| Camada | Origem | Nível |
|---|---|---|
| Trilha | **scratch, sintetizada** — 100 BPM, Fmaj7/Am7/Dm7/Bbmaj7 | base |
| Ambiência | room tone **real** dos próprios clipes, limpo e rebaixado | −5 dB |
| Transições | 2 passagens de ruído filtrado (bloco clínico + assinatura) | discreto |
| Mix | loudnorm alvo −14 LUFS, TP −1,2 dB · **medido: −13,0 LUFS** | padrão Reels |

A trilha **não é a final** — leia `docs/03-trilha.md`.
