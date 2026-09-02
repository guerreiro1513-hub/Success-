# MONTAGEM NO CAPCUT — passo a passo

Projeto: **1920×1080 · 30fps**. Tudo abaixo é CapCut desktop.

## 1 · Preparar o projeto
1. `Criar projeto` → canto superior direito, `Proporção` → **16:9**.
2. Menu `Arquivo` → `Configurações do projeto` → taxa de quadros **30**.

## 2 · Importar
1. `Importar` → arraste o arquivo do documentário para a mídia.
2. Arraste para a timeline, na **trilha 1**.

## 3 · Recortar os 9 trechos
Com a tabela de `roteiro-analise.md` na mão, para cada bloco:
1. Leve o playhead ao timestamp inicial → tecla **B** (dividir).
2. Leve ao timestamp final → **B** de novo.
3. Selecione o que sobrou fora e **Delete**.

Faça os 9 antes de qualquer outra coisa. Só depois arraste para a ordem do roteiro.

## 4 · Criar cada freeze frame
Para cada bloco, no frame de pausa indicado na tabela:
1. Clique no clipe, posicione o playhead no frame exato.
2. Na barra acima da timeline, botão **Congelar** (ícone de floco de neve).
   O CapCut insere um still de 3s ali.
3. Arraste a borda direita do still até a duração da explicação (coluna da tabela).

## 5 · Zoom lento no freeze
Com o still selecionado, painel direito → aba `Vídeo` → `Básico`:
1. Playhead no início do still → clique no **losango** ao lado de `Escala` (cria keyframe) → deixe **100%**.
2. Playhead no fim do still → mude `Escala` para **106%**. O keyframe entra sozinho.

## 6 · Vinheta da pausa
Still selecionado → aba `Efeitos` → busque **Vinheta** → arraste sobre o still →
intensidade em torno de **15%**.

## 7 · Textos de tela
1. `Texto` → `Texto padrão` → arraste para a trilha acima do vídeo.
2. Fonte sem-serifa condensada, **caixa alta**, branco, sombra suave ligada.
3. Posicione no **terço inferior esquerdo**. Mesma posição nos 9 blocos.
4. Animação: `Entrada` → **Fade in**, 0,3s. Nada além disso.

## 8 · Narração
1. Grave os 9 blocos em arquivos separados (`b0.wav` … `b8.wav`) — facilita reajustar.
2. Importe e coloque na **trilha de áudio 2**, cada um sob o seu freeze.
3. Se a narração estourar a duração do still, estenda o still — não acelere a voz.

## 9 · Trilha e mixagem
1. Trilha de fundo na **trilha de áudio 3**, volume base **−22 dB**.
2. Clipe original selecionado → `Áudio` → `Volume`: **0 dB** durante a cena,
   **−18 dB** durante a explicação (use keyframes no volume, transição de 0,4s).
3. Impacto sonoro do freeze: um clipe curto de grave na trilha 4, no frame da pausa.

## 10 · Fade final
Último clipe → `Vídeo` → `Básico` → `Fade out` **4s**.
Trilha de fundo → `Áudio` → `Fade out` **4s**.

## 11 · Exportar
`Exportar` (canto superior direito):
- Resolução **1080p**
- Taxa de quadros **30**
- Qualidade **Alta** (bitrate ≥ 12 Mbps)
- Codificação **H.264**
- Formato **MP4**
- Nome: `idi_amin_analise_documentario_4_5min`
