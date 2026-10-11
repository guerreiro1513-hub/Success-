# Juntar 2 partes + música de fundo (+ legenda pendente)

- `source/PARTE1.mov`, `source/PARTE2.mov`: vídeo do assador em duas partes (1080x1920, ~24,6 s cada).
- Montagem (ffmpeg): ordem PARTE2 → PARTE1 (a parte 2 é o começo: corte da costela inteira; o fim dela é o
  mesmo quadro do início da parte 1, então os 3 primeiros quadros e 0,1 s de som da parte 1 saem). Depois: voz com passa-alta e loudnorm (−15 LUFS), música
  `../bastidor/assets/musica_C_groove.mp3` em loop a −21 dB com sidechain (abaixa quando ele fala), fade de 2 s.
  Saída: `work/juntado.mp4` (49,4 s, −14,8 LUFS).
- Legenda: pendente. Não há modelo de transcrição disponível (Hugging Face/OpenAI/Vosk bloqueados pelo proxy);
  aguardando o texto da fala do cliente.
