# 03 · Trilha — leia antes de postar

## A trilha do corte é SCRATCH

`04_MUSIC/trilha-scratch-100bpm.wav` foi **sintetizada por código** aqui mesmo
(`make_music.py`): pad Fmaj7 / Am7 / Dm7 / Bbmaj7, sininho, pulso grave e uma
subida entrando na assinatura, com reverb por convolução.

**Ela não é boa o bastante pra ser a trilha final.** É som sintetizado, sem
instrumento real e sem mixagem profissional. O que ela resolve — e resolve bem
— é travar o ritmo: cada corte cai num tempo dela. Serve pra você assistir o
corte com a batida certa, não pra publicar.

Vantagem colateral: é 100% original, então não tem risco de copyright enquanto
o corte circula internamente.

## Trocar pela definitiva

1. Pegue uma faixa de **100 BPM** (Epidemic Sound, Artlist, ou a biblioteca
   comercial do CapCut/Instagram). Categoria: *corporate calm*, *minimal piano*,
   *ambient uplifting*. Fuja de trilha de "vídeo médico" — é o clichê que o
   briefing pede pra evitar.
2. Salve como `04_MUSIC/trilha-scratch-100bpm.wav` (mesmo nome) e rode
   `python3 build.py`. Pronto, sincronizado.
3. **Se a faixa não for 100 BPM**, não force: me diga o BPM e eu re-grade o
   corte. Com BPM diferente todas as durações mudam (a grade deixa de ser 0,6s).

## Se for postar direto do Instagram

Se você for usar o áudio nativo do Instagram/Reels em cima, exporte o corte com
a ambiência mas sem a trilha:

```bash
# mixa só ambiência + transições, sem música
ffmpeg -i 08_FINAL/MIDORI_base-v1_LIMPO.mp4 \
       -i 05_SOUND_DESIGN/ambiencia.wav \
       -map 0:v -map 1:a -c:v copy -shortest \
       08_FINAL/MIDORI_base-v1_LIMPO_sem-trilha.mp4
```

## Mix atual

| Camada | Nível |
|---|---|
| Trilha | base |
| Ambiência real da clínica | −5 dB |
| 2 passagens de transição | discreto |
| Master | loudnorm alvo −14 LUFS · TP −1,2 dB · **medido −13,0 LUFS** |
