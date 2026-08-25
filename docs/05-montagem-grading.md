# Montagem, color grading e tipografia

Etapa executada no **HyperFrames** (composição 9:16, tipografia, logo, end card, render final).

---

## Montagem

**Timeline 1080×1920 · 30fps · 16s**

Cortes secos em todas as emendas, com duas exceções:
- **S2 → S3:** match cut no movimento — a lateral de S2 termina onde o orbit de S3 começa
- **S5 → S6:** o desfoque final de S5 (gerado via `end_image: KF6`) entra direto no fundo
  do end card. Transição feita na geração, não em plugin.

**Speed ramp — apenas um no filme inteiro:**
S4, entre 09.1s e 09.7s: 100% → 50% → 100%. Cobre exatamente o momento em que o interior
da carne se revela. Qualquer ramp além deste é excesso.

**Motion blur:** só o nativo dos clipes. Nada de plugin de blur direcional.

**O que ficou de fora, de propósito:** transições de luz, whip pans, glitch, flash frames,
zoom por keyframe, partículas de fagulha adicionadas em pós. O briefing pede efeitos a
serviço da narrativa, e nenhum destes serve à carne.

---

## Color grading

Objetivo: cinematográfico e quente **sem virar banho de laranja**. A carne tem que continuar
parecendo carne — este é o critério que decide qualquer dúvida no grade.

**Base**
| Parâmetro | Valor | Razão |
|-----------|-------|-------|
| Lift (sombras) | `#12100E` | Preto profundo com leve calor, não puro |
| Gamma | +0.03 quente | Meio-tom com temperatura da brasa |
| Ganho (altas) | rolloff suave | Nunca clipar o brilho da gordura |
| Contraste | curva S ~1.15 | Densidade sem esmagar detalhe |
| Saturação global | 105% | Contenção deliberada |

**Ajustes seletivos — é aqui que o grade se salva**
- **Vermelhos da carne** (hue 5–15°): saturação +8, luminância +3 → mantém o vermelho vivo e real
- **Laranjas do fogo** (hue 25–45°): saturação **−6** → impede o neon que denuncia IA
- **Amarelos**: −4 saturação → tira o tom "filtro de aplicativo"
- **Azuis/ciano**: praticamente ausentes; deixar as sombras cair para neutro-frio ancora
  o quente por contraste. Sem isso, a imagem inteira vira laranja.

**Acabamento**
- Grão 35mm fino, 2–3%
- Vinheta −10 nas bordas
- Halation sutil só nas altas da brasa (opcional, no máximo 15%)

**Teste de sanidade:** dessature a imagem mentalmente. Se a carne some no fundo, o grade
está errado — o produto precisa se sustentar por luminância, não só por cor.

---

## Tipografia

**Fonte:** grotesca condensada bold — Anton, Archivo Black ou Oswald Bold.
Peso alto, tracking aberto em caixa alta. Nada de serifa, script ou fonte "rústica de churrascaria".

| Elemento | Especificação |
|----------|---------------|
| `CHURRASCO DE VERDADE.` | 72px, caixa alta, tracking +80, `#F5EFE6`, terço inferior |
| Entrada | Fade 0.25s + subida de 12px |
| Saída | Fade 0.2s aos 06.9s |
| Sombra | Drop shadow 0 4px 24px rgba(0,0,0,.55) para garantir leitura sobre a brasa |

**Zona segura:** todo texto dentro de 12% de margem lateral e acima de 240px do rodapé —
a UI do Reels/TikTok come essa faixa.

---

## End card (S6)

```
        [fundo: brasa desfocada, KF6]

           GUERREIROS GRILL 🔥
          ────────────────────
          SÁB & DOM · NA BRASA
```

- Logo em no **máximo 38% da largura** do frame, centralizado, 8% acima do centro óptico
- Filete de 1px, largura 60% da do logo, `#C9752A` a 60% de opacidade
- Subtítulo 32px, tracking +140, `#E8DCC8`
- Entrada: fade + scale 1.02 → 1.00 em 0.4s, easing `cubic-bezier(.2,.7,.3,1)`
- **Duração em tela: 1.6s** — tempo de ler, não de cansar

O logo nunca cobre a carne, nunca pisca, nunca tem fogo atravessando. O briefing foi
explícito quanto a isso.

---

## Entregas finais

| Arquivo | Formato | Uso |
|---------|---------|-----|
| `guerreiros-grill-16s.mp4` | 1080×1920, H.264, −14 LUFS | Reels / Stories |
| `guerreiros-grill-12s.mp4` | 1080×1920, H.264 | TikTok / teste A/B |
| `guerreiros-grill-capa.jpg` | 1080×1920 | Capa do Reels (frame de S3) |

A capa sai do hero shot (S3), não do hook — no grid do perfil, o hero é que segura o clique.
