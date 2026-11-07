# PHASE 2 — BLOQUEADA

## B1 · Transcrição local impossível (bloqueia H1, H4, Q5, Q6, Q7)

A PHASE 2 exige Whisper local, modelo "small" ou melhor. Os pacotes instalam
(PyPI é liberado), mas **todo host de peso de modelo é recusado pelo gateway**:

```
huggingface.co:443          403 no CONNECT   (faster-whisper)
openaipublic.azureedge.net  403 no CONNECT   (openai-whisper)
alphacephei.com:443         403 no CONNECT   (vosk)
```

Criei o ambiente pessoal **`hugo-almeida-video`** com os hosts do Hugging Face
liberados, mas esta sessão não pode migrar para ele. Destrava abrindo uma
**sessão nova e escolhendo esse ambiente** no menu.

## B2 · O áudio gravado não contém os roteiros (bloqueia H1)

Isto a transcrição não resolveria. Medi a janela de voz de cada tomada contra o
mínimo que cada roteiro exige num ritmo **rápido** para pt-BR (5,8 sílabas/s —
a estimativa mais generosa):

| roteiro | sílabas | mínimo | melhor tomada | voz | cobertura | síl/s exigido |
|---|---|---|---|---|---|---|
| S1 | 95 | 16,4s | `bloco1.mov` | 8,86s | **52%** | 10,7 |
| S2 | 121 | 20,9s | `bloco2.mov` | 5,32s | **25%** | **22,7** |
| S3 | 75 | 12,9s | `bloco3.mov` | 8,74s | **64%** | 8,6 |

Fala humana normal em pt-BR fica em 5–6 síl/s; 7–8 já é rápido. **22,7 síl/s é
fisicamente impossível.** As seis tomadas somam 22,9s de voz contra os 50,2s que
os roteiros pedem no mínimo.

Consequências diretas:
- **H1 falha** — faltam palavras, não é questão de montagem.
- **§5 alvo de 42–52s é inalcançável**: o teto com o áudio existente é ~38s.
- **F3 ("a fala parece truncada") não é defeito de edição**: é o que foi gravado.

## B3 · Fonte Inter indisponível (bloqueia §9)

§9 manda embutir a fonte e **nunca cair em serifa do sistema**. Inter e
Montserrat não existem neste ambiente e `fonts.google.com` responde 403.
Disponíveis: Instrument Sans, Work Sans, Outfit, Bricolage Grotesque.

## B4 · Campos da §15 em branco

| campo | estado | efeito |
|---|---|---|
| `{CRO_NUMBER}` | vazio | **H6** → só versão `hugo-almeida_v2_DRAFT_SEM_CRO.mp4` com "CRO-MT ______", não liberada para publicar |
| `{RAW_CLIPS_PATH}` | vazio | usei a pasta do projeto |
| `{MUSIC_FILE}` | vazio | sem música → **F10 e §11 não podem ser corrigidos** |
| `{PHOTO_BROLL}` | vazio | §7 Bloco 2 manda pular e ficar no Hugo |
| `{XRAY_BROLL}` | vazio | idem |
| `{FONT}` | "Inter" | ver B3 |

## B5 · Compliance encontrada na PHASE 1

A placa do prêmio diz **"Top Doctor 2023 — invisalign · iTero · exocad"** e está
legível em `broll/06_prateleira-premio.mov`. Viola **H7** e **H9**.
Resolvido por enquadramento (fica só o recorte dos modelos de arcada), não por
desfoque — mas precisa da sua ciência.

## O que eu preciso de você

1. **Regravar S1, S2 e S3 inteiros** — é o bloqueio principal. ~50s de fala.
   Alternativa: me mandar o texto do que ele **realmente diz** nas tomadas
   atuais, e aí eu legendo o que existe (§4 nota: "as legendas seguem o que ele
   realmente fala").
2. **O número do CRO.**
3. **Sessão nova no ambiente `hugo-almeida-video`**, para transcrever.
4. **Arquivo de música**, ou confirmação de seguir sem.
5. **OK para usar Instrument Sans** no lugar da Inter.
