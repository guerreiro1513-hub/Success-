# A Escala — V3, passe de refinamento (20,9 s)

Base: `guerreiros-ESCALA-PAI-22s`. Mesmo conceito, mesma ordem até o reveal.
Refeito a partir dos brutos 4K para trocar a tipografia sem perder qualidade.
Receita: `projetos/escala/project/build_cut3.sh`, `mix3.py`, `mktx3.py`, `render3.sh`.

## O que mudou e por quê

| Ponto | V2 (PAI-22s) | V3 |
|---|---|---|
| Início | 0,6 s mortos antes da fala | Abre em 1,6 s de close da churrasqueira, a câmera vira para o pai |
| Legenda da fala | Não existia | Legenda completa, Montserrat ExtraBold, palavras-chave em amarelo, em y=1180 (fora da área da interface do Reels) |
| "ISSO AQUI É SÓ 1 DE 6" | Título em cima da fala | Removido: a própria fala diz isso e a legenda mostra "SEIS CHURRASQUEIRAS" |
| Títulos do reveal | Fonte genérica, um some e o outro entra | Montserrat ExtraBold, "6" em amarelo, as duas linhas empilhadas e segurando juntas |
| Final | T01 → T04 → T01 → T03 → T01 → T01 congelado: o mesmo travelling 4 vezes | Reveal → recorte da operação → vinheta da marca |
| Gancho | T04 T03 T02 T03 T04 T02: cada churrasqueira duas vezes | T04 → T03 → frango → carne em bloco: cada uma uma vez |
| Cor | unsharp 0,95 no aberto (serrilhava) | unsharp 0,62. Mais vibrance nos closes. Curva mais suave (não esmaga a sombra da grelha, segura o alto da brasa). T06 com grade leve própria (GN): ele já vem tratado pelo celular |
| Voz | Áudio cru | Grave cortado em 95 Hz, redução leve do ruído da feira, +3 dB em 3 kHz, compressor 3:1 |
| Reveal | Só a música | Sub de 48 Hz bem discreto no primeiro quadro do reveal |

## Linha do tempo final (30 fps, 626 quadros, 20,9 s)

Pedidos depois da primeira V3: abrir na churrasqueira e só então entrar o pai;
nenhuma churrasqueira aparecer duas vezes; vinheta da marca no fim.

| Quadro | Tempo | Dura | Take | Churrasqueira / papel |
|---|---|---|---|---|
| 0 | 0,000 | 10,30 | T05 0,00 | Abre na costela em ripas, a câmera vira e o pai fala |
| 309 | 10,300 | 1,33 | T04 1,00 | Peças vermelhas. **A música bate aqui** |
| 349 | 11,633 | 1,00 | T03 3,30 | Panceta dourada |
| 379 | 12,633 | 1,33 | T06 2,60 | Frango |
| 419 | 13,967 | 0,67 | T06 11,30 | Carne em bloco |
| 439 | 14,633 | 3,33 | T01 0,30 | **REVEAL**, as seis de uma vez |
| 539 | 17,967 | 1,33 | T01 6,30, zoom 1,80 | A operação: banner, fumaça, gente trabalhando |
| 579 | 19,300 | 1,57 | T07 | Vinheta da marca, intacta, + @GUERREIROSGRILL |

Saíram para não repetir churrasqueira nem carne:
- **T02**: tem a mesma peça dourada do T03, é a mesma churrasqueira.
- **Costela na fumaça do T06**: repete a costela da abertura.
- **Brasão desenhado**: a vinheta já traz o logo, dois logos seguidos seria repetição.

O corte da panceta termina em 4,30 s do take porque logo depois a câmera vira
para peças vermelhas parecidas com as do T04.

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
subtraindo a versão SEM-MUSICA, com ganho calculado por trecho. Cai
no corte que sai do pai (quadro 309) e desce junto com o escurecimento da vinheta.

## Medições

- Com música: −14,5 LUFS, pico −2,3 dBTP
- Sem música: −16,3 LUFS, pico −2,3 dBTP
- Nenhum quadro preto. 1080x1920, H.264 CRF 18, AAC 192k, `+faststart`

## Entrega

- `entrega/guerreiros-ESCALA-V3-FINAL-20s.mp4`
- `entrega/guerreiros-ESCALA-V3-FINAL-20s-SEM-MUSICA.mp4`

---

# V4 — ajustes de ritmo (21,5 s, 646 quadros)

Pedido: carnes mais tempo na tela, pai nos 3 primeiros segundos, legenda sem atraso.

| Quadro | Tempo | Dura | Take | Papel |
|---|---|---|---|---|
| 0 | 0,000 | 9,30 | T05 1,00 | 0,6 s de costela, a câmera vira. **O pai aparece em ~1,2 s** |
| 279 | 9,300 | 1,50 | T04 1,00 | Peças vermelhas. A música bate aqui |
| 324 | 10,800 | 1,00 | T03 3,30 | Panceta (não cresce: depois a câmera mostra peças iguais às do T04) |
| 354 | 11,800 | 2,00 | T06 2,40 | Frango |
| 414 | 13,800 | 1,50 | T06 11,15 | Carne em bloco |
| 459 | 15,300 | 3,33 | T01 0,30 | REVEAL |
| 559 | 18,633 | 1,33 | T01 6,30 | A operação |
| 599 | 19,967 | 1,57 | T07 | Vinheta |

As carnes somam 6,0 s, contra 4,3 s na versão anterior.

**Legenda:** cada frase entra 5 quadros (0,17 s) antes da voz e a animação caiu de
5 para 3 quadros. Entrando no mesmo quadro da sílaba, a legenda ainda estava
surgindo quando a palavra já tinha sido dita, e isso parece atraso.

Medido: com música −14,8 LUFS, sem música −16,8 LUFS, pico −2,1 dBTP.

Entrega: `entrega/guerreiros-ESCALA-V4-21s.mp4` e `-SEM-MUSICA`.
