# Corte para Reels — 12s

`entrega/guerreiros-grill-REELS-12s.mp4` · 11,97s · 1080×1920 · 30fps · H.264 · com áudio

Feito com os **três** vídeos do cliente. Nenhum frame de IA, nenhum crédito gasto.

## A decisão que mudou o corte

O terceiro vídeo é o melhor material dos três: travelling contínuo sobre a grelha
lotada de carnes glaceadas, iluminação dramática — e **uma labareda real**.

O fogo virou o hook. Frame 1 é chama. É o que segura o dedo no Reels.

## Cortes

| # | TC | Dur | Cena | Fonte |
|---|----|-----|------|-------|
| 1 | 00,00 | 1,20s | **FOGO** — labareda, slow-motion 1,6× | C @ 8,10 |
| 2 | 01,20 | 1,10s | Grelha lotada, travelling | C @ 0,30 |
| 3 | 02,30 | 1,10s | Frango dourado em close | A @ 1,95 |
| 4 | 03,40 | 1,00s | Fileiras de carnes glaceadas | C @ 5,10 |
| 5 | 04,40 | 1,30s | Corte da carne, luva preta | B @ 18,30 |
| 6 | 05,70 | 1,10s | Espetos na grelha | C @ 11,20 |
| 7 | 06,80 | 1,17s | Tesoura no frango | B @ 23,85 |
| 8 | 07,97 | 1,20s | Equipe tirando peça da grelha | B @ 20,50 |
| 9 | 09,17 | 1,00s | Profundidade da grelha | C @ 12,40 |
| 10 | 10,17 | 1,80s | End card com o logo | — |

Ritmo de ~1,1s por corte nos nove primeiros. Reels premia corte rápido no início.

**Texto:** `CHURRASCO RAIZ` de 0,35 a 2,05s, sobre o fogo. Uma inserção só, e é a
assinatura real da marca, não frase de agência.

## Diferenças em relação ao corte anterior

- **Hook de fogo** no lugar do frango parado
- **Som contínuo**: um leito de ambiência de 12s tirado do vídeo B, com high-pass em
  90 Hz e normalização a −15 LUFS. O corte anterior usava o áudio de cada trecho,
  o que picotava a cada emenda.
- **Grade mais clara**: vinheta reduzida de PI/4,2 para PI/5,5, brilho +0,030.
  A versão anterior escurecia demais em tela de celular.
- **Ritmo quase o dobro**: ~1,1s por corte contra ~2,0s.

## Enquadramento do vídeo C

O terceiro vídeo é 1080×1582, que não é 9:16. Recorte central de 890×1582 e escala
para 1080×1920 — a proporção bate exatamente, sem distorcer. No hook, recorte mais
fechado (594×1056) para o fogo ocupar mais quadro.

## Defeitos corrigidos durante o render

1. **Fogo sumia no meio do hook.** O corte ia de 8,15 a 9,15 mas a labareda vive de
   8,10 a 8,80. Reajustado e esticado em slow-motion para preencher 1,2s com chama
   do primeiro ao último frame. Verificado por amostragem.
2. **Trecho escuro no plano da tesoura.** O corte em 24,10 + 1,30s pegava um rabo
   borrado e escuro em 25,4. Recuado para 23,85 + 1,15s.
3. **Slow-motion não aplicou.** `-t` antes do `-i` limitava a saída junto com a
   entrada, e o `setpts` não esticava. Resolvido separando `-t` de entrada e de saída.
4. **Duração escapou para 12,63s.** A imagem de texto em loop estendia o vídeo.
   Travado com `-t` na saída.
