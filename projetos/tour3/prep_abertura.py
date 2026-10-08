#!/usr/bin/env python3
"""Prepara a entrada do GTA (referencia 1) em 1080x1920 sem perder nitidez.

A fonte e 1024x576. Cortar uma faixa vertical do meio (324 px) e ampliar 3,3x
deixa tudo borrado (testado: nem super-resolucao EDSR ajuda, a fonte ja vem
comprimida). Aqui a imagem horizontal inteira (menos as bordas com a marca do
TikTok) aparece nitida numa "janela" no centro, sobre um fundo desfocado dela
mesma, e no ultimo salto a janela cresce ate a tela cheia, acompanhando a
descida da camera. Sai com os mesmos tempos da fonte (30 fps), com o som original.

    python3 prep_abertura.py   ->   work/REF1_vertical.mp4
"""
import os, subprocess, numpy as np, cv2

FF = "/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "referencias/REF1_abertura_aerea.mp4")
OUT = os.path.join(ROOT, "work/REF1_vertical.mp4")
W, H, FPS = 1080, 1920, 30
T_END = 7.42                 # ultimo quadro antes do salto para a rua (personagens)
GROW = (6.0, 7.42)           # a janela abre ate a tela cheia nesse intervalo
CROP_X0, CROP_X1 = 175, 880  # fora das marcas do TikTok (canto sup. esq. e inf. dir.)
CROP_Y0, CROP_Y1 = 48, 498


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    raw = subprocess.run([FF, "-v", "error", "-t", f"{T_END + 0.2}", "-i", SRC, "-vf", f"fps={FPS}",
                          "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, check=True).stdout
    fr = np.frombuffer(raw, np.uint8).reshape(-1, 576, 1024, 3)
    enc = subprocess.Popen([FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}",
                            "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "slow", "-crf", "12",
                            "-pix_fmt", "yuv420p", OUT + ".v.mp4"], stdin=subprocess.PIPE)
    cw = CROP_X1 - CROP_X0
    base = W / cw                                     # janela ocupando a largura toda
    full = H / (CROP_Y1 - CROP_Y0)                                    # janela cobrindo a altura toda
    yy, xx = np.mgrid[0:H, 0:W]
    for i, f in enumerate(fr):
        t = i / FPS
        # fundo: faixa central ampliada, bem desfocada e mais escura
        bg = cv2.resize(f[:, 350:674], (W, H), interpolation=cv2.INTER_LINEAR)
        bg = cv2.GaussianBlur(bg, (0, 0), 28) * 0.45
        # janela
        p = np.clip((t - GROW[0]) / (GROW[1] - GROW[0]), 0, 1) ** 2.2
        s = base + (full - base) * p
        win = f[CROP_Y0:CROP_Y1, CROP_X0:CROP_X1]
        ww, wh = int(cw * s), int((CROP_Y1 - CROP_Y0) * s)
        big = cv2.resize(win, (ww, wh), interpolation=cv2.INTER_LANCZOS4)
        if s < 1.6:   # nitidez so enquanto a ampliacao e pequena (evita realcar blocos)
            big = cv2.addWeighted(big, 1.45, cv2.GaussianBlur(big, (0, 0), 1.2), -0.45, 0)
        x0, y0 = (W - ww) // 2, (H - wh) // 2
        canvas = bg.astype(np.float32)
        # mascara com borda suave (sem moldura dura)
        sx0, sy0 = max(0, -x0), max(0, -y0)
        dx0, dy0 = max(0, x0), max(0, y0)
        w_ = min(ww - sx0, W - dx0); h_ = min(wh - sy0, H - dy0)
        m = np.zeros((H, W), np.float32); m[dy0:dy0 + h_, dx0:dx0 + w_] = 1
        m = cv2.GaussianBlur(m, (0, 0), 6)[..., None]
        layer = np.zeros_like(canvas); layer[dy0:dy0 + h_, dx0:dx0 + w_] = big[sy0:sy0 + h_, sx0:sx0 + w_]
        # sombra da janela sobre o fundo
        sh = cv2.GaussianBlur(m[..., 0], (0, 0), 30)[..., None] * 0.5
        canvas = canvas * (1 - sh)
        canvas = canvas * (1 - m) + layer * m
        enc.stdin.write(np.clip(canvas, 0, 255).astype(np.uint8).tobytes())
    enc.stdin.close(); enc.wait()
    subprocess.run([FF, "-y", "-v", "error", "-i", OUT + ".v.mp4", "-t", f"{T_END + 0.2}", "-i", SRC,
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", OUT], check=True)
    os.remove(OUT + ".v.mp4")
    print(OUT, len(fr), "quadros")


if __name__ == "__main__":
    main()
