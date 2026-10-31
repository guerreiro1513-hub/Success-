# Churrasqueira 4K, sem a música com direitos autorais (27,1 s)

`entrega/guerreiros-CHURRASQUEIRA-4K.mp4` — 2160×3840 · 30 fps · HEVC (hvc1) ~7,6 Mbps · AAC · −16,7 LUFS.
`fazer.py` refaz tudo (o master de 113 MB fica em `work/MASTER-4K.mp4`, fora do git).

- Fonte: vídeo do cliente (CapCut, 720×1280) com uma música com direitos autorais misturada ao som da churrasqueira.
  A música domina o áudio inteiro (espectro tonal em todos os trechos); separar sem modelo de IA não fica limpo e os
  modelos (demucs/Hugging Face) estão bloqueados pela rede. Então o áudio foi TROCADO pelo chiado real da churrasqueira
  do Guerreiro's Grill, recortado do vídeo do Florais (11,6–21,0 s, sem voz e sem música), emendado em voltas que
  começam em pontos diferentes com cruzamentos de 1,2 s.
- 4K: redução leve de ruído (hqdn3d), ampliação lanczos 3x e nitidez adaptativa (cas 0,45). A resolução é 4K, mas o
  detalhe é o do arquivo de 720p que veio (não dá para criar detalhe real que a câmera não gravou).
