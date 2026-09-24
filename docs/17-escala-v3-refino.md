# A Escala — V3, passe de refinamento (21,3 s)

Base: `guerreiros-ESCALA-PAI-22s`. Mesmo conceito, mesma ordem até o reveal.
Refeito a partir dos brutos 4K para trocar a tipografia sem perder qualidade.
Receita: `projetos/escala/project/build_cut3.sh`, `mix3.py`, `mktx3.py`, `render3.sh`.

## O que mudou e por quê

| Ponto | V2 (PAI-22s) | V3 |
|---|---|---|
| Início | 0,6 s mortos antes da fala | Fala começa em 0,18 s. Take de 2,30 a 10,30 |
| Legenda da fala | Não existia | Legenda completa, Montserrat ExtraBold, palavras-chave em amarelo, em y=1180 (fora da área da interface do Reels) |
| "ISSO AQUI É SÓ 1 DE 6" | Título em cima da fala | Removido: a própria fala diz isso e a legenda mostra "SEIS CHURRASQUEIRAS" |
| Títulos do reveal | Fonte genérica, um some e o outro entra | Montserrat ExtraBold, "6" em amarelo, as duas linhas empilhadas e segurando juntas |
| Final | T01 → T04 → T01 → T03 → T01 → T01 congelado: o mesmo travelling 4 vezes | Reveal → recorte da operação (banner, fumaça, gente trabalhando) → frango → costela na fumaça → carne em bloco (T06, vídeo novo) → brasão com o take em movimento |
| Cor | unsharp 0,95 no aberto (serrilhava) | unsharp 0,62. Mais vibrance nos closes. Curva mais suave (não esmaga a sombra da grelha, segura o alto da brasa). T06 com grade leve própria (GN): ele já vem tratado pelo celular |
| Voz | Áudio cru | Grave cortado em 95 Hz, redução leve do ruído da feira, +3 dB em 3 kHz, compressor 3:1 |
| Reveal | Só a música | Sub de 48 Hz bem discreto no primeiro quadro do reveal |

## Linha do tempo (30 fps, 640 quadros)

| Quadro | Tempo | Dura | Take | Papel |
|---|---|---|---|---|
| 0 | 0,000 | 8,000 | T05 2,30 | A fala inteira, sem música |
| 240 | 8,000 | 1,33 | T04 | Corte seco, a música bate aqui |
| 280–370 | 9,33 | 3,00 | T03 T02 T03 T04 T02 | Gancho acelerando: 30, 20, 20, 10, 10 quadros |
| 370 | 12,333 | 3,33 | T01 0,30 | **REVEAL** |
| 470 | 15,667 | 1,33 | T01 6,30, zoom 1,80 | A operação |
| 510 | 17,000 | 0,67 | T06 2,80 | Frango |
| 530 | 17,667 | 0,67 | T06 7,10 | Costela na fumaça |
| 550 | 18,333 | 1,00 | T06 11,30 | Carne em bloco |
| 580 | 19,333 | 2,00 | T01 7,60 | Brasão + @GUERREIROSGRILL |

Todo corte depois da fala cai na grade de 90 BPM (20 quadros = 1 tempo).

## Legenda

Transcrição fornecida pelo cliente, grafia corrigida só no acento ("essa é"):

> Fala, gurizada! Essa é uma das seis churrasqueiras que temos no Florais.
> Vem pra cá, tem muita coisa boa. Um abraço, vem ser feliz!

Não há reconhecimento de fala no ambiente. Os tempos foram medidos no
espectrograma do take, sílaba por sílaba. Os blocos de duas linhas entram
linha a linha, então a segunda linha acompanha a fala mesmo onde a fronteira
exata entre palavras é incerta (trecho "tem muita coisa boa", falado rápido).

## Trilha

A trilha original não está no repositório. Ela foi recuperada do mix da V2
subtraindo a versão SEM-MUSICA, com ganho calculado por trecho. Cai 10 quadros
antes do que na V2 (a fala foi aparada) e desce nos últimos 0,9 s.

## Medições

- Com música: −15,0 LUFS, pico −2,4 dBTP
- Sem música: −17,9 LUFS, pico −2,4 dBTP
- Nenhum quadro preto. 1080x1920, H.264 CRF 18, AAC 192k, `+faststart`

## Entrega

- `entrega/guerreiros-ESCALA-V3-21s.mp4`
- `entrega/guerreiros-ESCALA-V3-21s-SEM-MUSICA.mp4`
