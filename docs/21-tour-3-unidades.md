# Tour 3 unidades — reel cinematográfico (em andamento)

Sistema reutilizável em `projetos/tour3/`: `timeline.json` (ordem, clipes, cortes,
velocidades, cor por clipe, transições, textos, encerramento) + `render.py`
(`--preview` = 540x960; sem flag = final 1080x1920, 30 fps, H.264 + AAC). Gera
também `<saida>.cortes.json` com os tempos dos cortes (para sincronizar a música).

## Referências
- REF1 (`referencias/REF1_abertura_aerea.mp4`, GTA): mapa visto de cima, 3–4 saltos
  de zoom (cada nível segura ~1 s), depois a câmera inclina até o nível da rua. Só a
  mecânica será usada, com imagem real (gravação do Google Earth) — nada do jogo.
- REF2 (`referencias/REF2_efeito_fachada.mp4`): NÃO é um vídeo de cortes rápidos; é um
  tutorial de "efeito fachada" (logo 3D aplicado na fachada com a câmera andando),
  0–4 s de resultado e o resto tela de celular. A linguagem de transições (whip,
  rampa de velocidade, desfoque direcional) foi feita a partir do texto do briefing.

## Tropical Ville (4 clipes, iPhone 4K/60p, ~2,6 s cada)
| Arquivo | Conteúdo | Movimento (imagem na tela) | Nota |
|---|---|---|---|
| C128a fachada | fachada, árvore, churrasqueira, placa "frango no rolete" | avança (zoom +4%/0,25 s), sobe e vai pra direita no fim | céu lilás (export já tratado, 3066x2158) — corrigido |
| C128b frangos | grelha de frangos | avança no começo, depois abre forte pra esquerda-baixo (whip natural) | melhor clipe para transição |
| C130 grelha | grelha giratória de perto | imagem desce (câmera sobe), leve recuo | escura (luz 65) — clareada |
| C122 costela | costela no giro, fumaça | imagem corre pra direita, avança no fim | mais macia (fumaça) |

Sequência: fachada (título) → zoom para dentro da churrasqueira → frangos (rampa
2x no meio) → whip 150° → grelha (câmera lenta 0,6x e acelera 3x) → whip 55° →
costela → encerramento em câmera lenta 0,3x escurecendo. Prévia: 8,4 s.

## Entrada do GTA (pedido do cliente: usar a própria entrada da referência 1)
- `opening` no timeline: REF1 de 0,78 a 8,85 s (começa depois do personagem verde e
  corta antes dos personagens aparecerem), corte vertical no centro (fora das marcas do
  TikTok), saltos acelerados (1,5x / 2,2x / 2,5x / 1,2x) e som original da entrada
  acompanhando as rampas (`audio_speed`, atempo por trecho). Zoom para dentro da 1ª unidade.
- Fonte é 1024x576: o corte vertical usa 324 px de largura, ampliados 3,3x. Limpeza:
  `hqdn3d` antes de ampliar, lanczos, `unsharp` e grão fino.
- `python3 render.py --entrada` gera só a abertura + 1º clipe em 1080x1920:
  `entrega/teste-ENTRADA-GTA.mp4` (5,9 s).
