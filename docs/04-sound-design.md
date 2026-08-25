# Sound design e trilha

Tudo gerado via Kairogen `generate_audio`. Nenhum clipe de vídeo é gerado com áudio nativo
no fluxo recomendado (`sound: false`) — o som é construído em camadas na montagem, que é
como se controla mix de verdade.

---

## Camadas

| # | Camada | Tipo | TC | Função |
|---|--------|------|-----|--------|
| A1 | Leito de brasa | `sound-effect`, loop | 00.0 – 16.0 | Continuidade; nunca some |
| A2 | Sizzle da carne | `sound-effect` | 00.0 – 12.0 | Presença do produto |
| A3 | Labareda curta | `sound-effect` | 03.4 | Acento em S2 |
| A4 | Corte da faca | `sound-effect` | 09.2 | O clímax sensorial |
| A5 | Suco pingando | `sound-effect` | 12.6 | Detalhe de suculência |
| A6 | Trilha | `music` | 00.0 – 16.0 | Identidade da marca |
| A7 | Hit final | `sound-effect` | 14.4 | Assina o logo |

---

## Prompts

**A1 — leito de brasa** (`kind: sound-effect`, `duration_seconds: 20`, `loop: true`)
```
Continuous bed of glowing charcoal embers crackling softly, close-miked, warm and low,
no flames roaring, no music, no room reverb
```

**A2 — sizzle** (`kind: sound-effect`, `duration_seconds: 8`)
```
Meat sizzling on a hot charcoal grill, fat dripping and popping, close intimate microphone,
rich low-mid presence, no music
```

**A3 — labareda** (`kind: sound-effect`, `duration_seconds: 3`)
```
Short controlled flare-up as fat drips onto hot coals, a soft whoosh rising and settling
back down within two seconds, natural not explosive
```

**A4 — corte** (`kind: sound-effect`, `duration_seconds: 3`)
```
Sharp chef knife slicing cleanly through cooked meat on a wooden board, single decisive
stroke, crisp and close, ending with the blade touching the board
```

**A5 — suco** (`kind: sound-effect`, `duration_seconds: 3`)
```
Thick meat juices dripping slowly onto a wooden board, a few isolated heavy drops,
very close microphone, quiet background
```

**A6 — trilha** (`kind: music`, `duration_seconds: 20`, `instrumental: true`)
```
Cinematic Brazilian barbecue brand track, deep percussive low drums with a confident
mid-tempo groove, warm analog bass, sparse and muscular, building to a single decisive
hit at 14 seconds, leaves space in the mid frequencies for foley, instrumental, no vocals
```
*Custo confirmado: **3 créditos** (20s).*

**A7 — hit final** (`kind: sound-effect`, `duration_seconds: 3`)
```
Single deep percussive impact with a short warm tail, cinematic brand stinger, confident
and clean, no reverb wash
```

---

## Mixagem

A regra central do briefing: **a música não pode esconder os sons importantes.**

| Elemento | Nível alvo | Observação |
|----------|-----------|------------|
| Trilha (A6) | −20 LUFS | Leito, fica embaixo |
| Brasa (A1) | −24 LUFS | Sempre presente, nunca protagonista |
| Sizzle (A2) | −16 LUFS | Sobe 2 dB nos closes de produto |
| Corte (A4) | −10 dB pico | O som mais alto do filme |
| Master | −14 LUFS integrado | Padrão de Reels/TikTok |

**Ducking:** a trilha abaixa 4 dB por 0.6s a partir de 09.0s, devolvendo o espaço ao corte
da faca. É o único ducking do filme.

**Corte de frequência:** high-pass em 80 Hz na trilha para o sizzle e a brasa ocuparem
o grave-médio sem embolar.

**Primeiro segundo:** o som entra já a todo volume no frame 1, junto com a imagem.
Sem fade-in — fade-in no som mata a retenção tanto quanto fade-in na imagem.
