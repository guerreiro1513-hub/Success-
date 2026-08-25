# ETAPA 1 — Análise do produto

Baseada em 4 fotos de referência enviadas pelo cliente (`referencias/`).

---

## O que o Guerreiros Grill vende

| Ref | O que mostra | Uso na peça |
|-----|--------------|-------------|
| `ref-1-grelha.png` | Grelha de arame carregada, peças glaceadas em vermelho-âmbar, espetos de madeira atravessando, brasa e chama por baixo, luz de sol lateral forte | **S2 — Brasa** |
| `ref-2-costela.jpg` | Costela bovina inteira na tábua, ossos expostos, crosta escura, noite, fogo ao fundo | Alternativa de hero / S2 |
| `ref-3-avental-logo.png` | Avental preto com o logo, faca e garfo trinchante, fatia com interior rosado | **Identidade visual** |
| `ref-4-picanha.jpg` | Picanha fatiada, capa de gordura íntegra, fatias rosadas, tábua envernizada, luvas pretas | **S3, S4, S5** |

## Identidade da marca (extraída de `ref-3`)

- **Logo:** brasão escuro, "CHURRASCO RAIZ" no topo em arco, **GUERREIROS** em branco condensado,
  **GRILL** em amarelo manuscrito, chama vermelha ao centro
- **Paleta:** preto · vermelho-chama · amarelo-ouro · branco
- **Instagram:** `@guerreirosgrill` · **WhatsApp:** (65) 9…917
- **Assinatura:** "CHURRASCO RAIZ" — vale mais que qualquer slogan inventado.
  Está sendo usada no end card no lugar de frases genéricas.

## Decisão de direção: a picanha é a protagonista

O negócio serve mais de um corte, mas um filme de 16s não comporta dois protagonistas.
Escolhi a **picanha** como produto principal, com a costela e as carnes da grelha aparecendo
como universo em S2.

Razões:
1. **Capa de gordura** — o elemento visual mais reconhecível e mais bonito na tela
2. **O corte** (S4) é o clímax do filme, e o interior rosado da picanha é imbatível
3. Aparece em 2 das 4 referências, é o que o cliente já fotografa como hero

> Se preferir a **costela** como protagonista, é trocar o PRODUCT LOCK em `docs/02` —
> o storyboard, o grading e o som seguem valendo sem mudança.

## Observações técnicas das referências

**A favor:**
- A luz real do negócio já é boa: brasa por baixo, fundo escuro, alto contraste — é
  exatamente a direção de fotografia do briefing, não precisa ser inventada
- A tábua de madeira envernizada avermelhada é um elemento de marca; entra em todas as cenas
- Luvas pretas resolvem o maior risco da geração por IA: mão deformada.
  **Todas as cenas com mão devem especificar luva preta de churrasco.**

**A vigiar na geração:**
- `ref-1` tem luz de sol dura; o filme é noturno/brasa. Usar só como referência de
  textura e glacê, nunca de iluminação
- Os espetos de madeira de `ref-1` confundem modelos de IA (viram palitos deformados).
  Ficam fora dos prompts
- O ponto da carne em `ref-4` é ao ponto para mal passado — o PRODUCT LOCK trava nesse ponto

## Ainda em falta

Um **macro real da crosta** (carne ocupando 100% do quadro) para o hook S1.
Guia de enquadramento em `referencias/guia-close.jpg`.

Não é bloqueante: dá para recortar `ref-4` e `ref-1` como referência de macro, e foi
exatamente isso que o guia demonstra. Uma foto macro dedicada deixaria o S1 mais forte.
