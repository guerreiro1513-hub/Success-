# Troca de carne — match cut com a tábua girando (21,0 s)

Projeto `projetos/troca/`: `build.sh` (chama `build.py`) refaz tudo com um comando; coloque `fachada.mov` na pasta e
rode de novo. Saídas: `entrega/guerreiros-grill-troca-de-carne-v1.mp4` (sem música, −20 LUFS, para pôr o áudio no app)
e `...-v1-COM-MUSICA.mp4` (música do vídeo de referência, −16 LUFS). `alignment_log.txt`, `cortes.json`, `thumbnail.jpg`.

Inspiração (`source/v09025g...mp4`): cortes rápidos, clarão branco entre blocos, música com drop em 6,19 s, 77 BPM.

| Tempo | Bloco | Fonte |
|---|---|---|
| 0,00–2,40 | gancho: churrasqueira girando, ESTAMOS ABERTOS AGORA | IMG_1663 0,0 |
| 2,40–4,90 | fachada (cartela FACHADA até chegar fachada.mov), GUERREIRO'S GRILL | — |
| 4,90–12,68 | série: 5 planos de 2 batidas (1,556 s), cortes secos no giro | IMG_1822, IMG_1881, IMG_1818 |
| 12,68–16,57 | churrasqueira: frangos no rolete + outro trecho da grelha | copy_CD6275E9 0,3 · IMG_1663 5,0 |
| 16,57–21,00 | fecho: costela com o garfo (punch-in 105%), logo + PEDIDOS: WHATSAPP NA BIO | IMG_1828 0,2 |

- Alinhamento: para cada junção, o último quadro do plano que sai é comparado com todos os quadros possíveis do clipe
  que entra (miniatura 135x240 cinza bem desfocada = forma da tábua e da peça, não a textura da carne), sem espelhar e
  sem repetir trecho já usado. O primeiro plano começa onde a tábua gira mais.
- O drop da música cai no primeiro plano da série (música começa em 1,29 s da faixa).
- Cor fiel: exposição igualada (±8%) e contraste +4%; sem saturar a carne.
- Som (versão sem música): ambiente da churrasqueira contínuo por baixo de tudo, áudio real do gancho, dos frangos e da
  costela em −20 LUFS, pico −1,1 dBFS.
- Diferenças do roteiro: IMG_1879 e IMG_1939 não vieram → série com IMG_1822, IMG_1881 (frango) e IMG_1818; 5 planos
  de 1,56 s (o cliente pediu ~1,5 s) em vez de 8 de 1,0 s; {UNIDADE}, {DIAS} e {HORARIO} não informados → texto da
  fachada "GUERREIRO'S GRILL", sem a linha de dias/horário; logo centralizado acima do CTA (no canto inferior esquerdo
  ficava em cima da caixa). O logo oficial traz o WhatsApp impresso.
