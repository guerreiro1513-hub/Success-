# 01 · Decupagem do corte v2

Grade de **0,3s** (meio tempo a 100 BPM). Toda duração é múltipla disso — é o
que mantém a trilha sincronizada quando um plano for trocado.
Corte seco em tudo, como a referência. Nenhum dissolve.

## Corte ESTRUTURA — 39,0s · 21 planos

| TC | # | Seção | Plano | Fonte | In | Dur | Tratamento |
|---|---|---|---|---|---|---|---|
| 0.0 | P00 | PLACEHOLDER | ⬛ FACHADA | — | — | 3.0 | — |
| 3.0 | S01 | ABERTURA | A PLACA | RECEPCAO | 2.4 | 2.1 | push 1.03× |
| 5.1 | S02 | ENTRADA | RECEPCAO | RECEPCAO | 0.15 | 1.8 | push 1.02× |
| 6.9 | S03 | PONTUACAO | DETALHE | LOUNGE_COPA | 12.2 | 0.6 | push 1.14× |
| 7.5 | P01 | ENTREVISTA | ⬛ ENTREVISTA / BLOCO 1 | — | — | 2.4 | — |
| 9.9 | S04 | AMBIENTE | ESPERA | LOUNGE_TV | 1.0 | 1.2 | push 1.03× |
| 11.1 | S05 | IDENTIDADE | A MARCA NA PAREDE | RECEPCAO | 4.8 | 1.8 | push 1.04× |
| 12.9 | P02 | ENTREVISTA | ⬛ ENTREVISTA / BLOCO 2 | — | — | 2.1 | — |
| 15.0 | P03 | PLACEHOLDER | ⬛ PROCEDIMENTO | — | — | 1.2 | — |
| 16.2 | P04 | ENTREVISTA | ⬛ ENTREVISTA / BLOCO 3 | — | — | 0.9 | — |
| 17.1 | S06 | AMBIENTE | CONFORTO | LOUNGE_TV | 4.6 | 0.9 | — |
| 18.0 | S07 | CLINICO | CONSULTORIO | CONSULTORIO1 | 0.15 | 3.0 | push 1.05× |
| 21.0 | P05 | ENTREVISTA | ⬛ ENTREVISTA / BLOCO 4 | — | — | 1.8 | — |
| 22.8 | P06 | PLACEHOLDER | ⬛ SORRISO / PACIENTE | — | — | 2.1 | — |
| 24.9 | P07 | PLACEHOLDER | ⬛ EQUIPE | — | — | 2.4 | — |
| 27.3 | S08 | PONTUACAO | PASSAGEM | CONSULTORIO2 | 0.6 | 0.9 | — |
| 28.2 | S09 | DETALHE | ORGANIZACAO | LOUNGE_COPA | 8.0 | 1.5 | push 1.06× |
| 29.7 | S10 | DETALHE | INSTRUMENTAL | CONSULTORIO1 | 5.0 | 1.8 | speed ramp 1.0×→0.7× |
| 31.5 | S11 | CLINICO | SALA | CONSULTORIO2 | 4.6 | 1.2 | push 1.03× |
| 32.7 | P08 | ENTREVISTA | ⬛ ENTREVISTA / BLOCO 5 | — | — | 3.3 | — |
| 36.0 | S12 | MARCA | ASSINATURA | RECEPCAO | 8.4 | 3.0 | slow 0.73× · push 1.03× · CTA |
⬛ = slot a gravar. São **9 de 21** — a referência é movida por entrevista e
gente trabalhando, e esse material ainda não existe.

## Corte LIMPO — 19,8s · 12 planos

Os mesmos planos reais, sem os slots. A assinatura sai de 36,0s para 16,8s, e
a trilha é remontada tirando 19,2s do miolo (exatos 8 compassos, de fronteira
a fronteira) — o impacto da marca continua caindo em cima do corte.

Ritmo medido no MP4 final:
`2,1 · 1,8 · 0,6 · 1,2 · 1,8 · 0,9 · 3,0 · 0,9 · 1,5 · 1,8 · 1,2 · 3,0`
mediana 1,65s · desvio 0,74 (referência: 1,90s · ~0,67)

## Por que cada plano está onde está

- **P00 abre com 3,0s de fachada.** A referência abre com 3,0s parados no
  plano externo. É o tempo longo e confiante que estabelece que o lugar existe.
  Sem fachada gravada, o corte limpo começa direto na placa.
- **S03 tem 0,6s.** Pontuação. A referência usa um plano de 0,47s exatamente
  nessa posição, antes de entrar na primeira fala.
- **P04 (entrevista bloco 3) tem 0,9s.** Retorno curto à entrevista pra quebrar
  o ritmo — a referência faz isso com 0,87s.
- **S07 tem 3,0s.** O plano longo do bloco clínico. Depois de seis cortes
  curtos, o filme precisa respirar.
- **S09 era a parede do logo e virou o armário de vidro da copa.** A marca
  aparecia 4 vezes em 20 segundos. Agora aparece 3: abertura, beat de marca,
  assinatura.
- **S10 é o único speed ramp** do filme, fechando no instrumental.
- **S12 em slow 0,73×** sobre a placa física. Sem logo digital sobreposta.

## O que foi descartado e por quê

- **0–1,0s do lounge TV:** a TV está trocando de imagem e o quadro fica rosa.
- **Miolo escuro do lounge copa (9,5–12s):** subexposto e com bagunça visível.
- **Últimos 2s de todos os 5 arquivos:** tarja do CapCut. Os clipes em
  `02_CLINIC_FOOTAGE/` já estão cortados sem ela.
