#!/usr/bin/env python3
"""QA (Q1–Q11 automatizáveis) + edl.md a partir de work/edl.json.   python3 qa.py"""
import os, json, subprocess, re
ROOT = os.path.dirname(os.path.abspath(__file__)); P = lambda p: os.path.join(ROOT, p)
E = json.load(open(P("work/edl.json")))
OUT = P("../../entrega/guerreiros-grill_historia_20261122.mp4")
PREV = P("../../entrega/guerreiros-grill_historia_20261122_COM-MUSICA.mp4")
FPS = 30; beat = E["beat"]

def probe(f):
    r = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_name,profile,width,height,r_frame_rate,avg_frame_rate,pix_fmt,sample_rate,channels:format=duration,size,bit_rate",
                        "-of", "json", f], capture_output=True, text=True).stdout
    return json.loads(r)
def loud(f):
    r = subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    I = re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]; TP = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r)[-1]
    return float(I), float(TP)

NOMES = {"V1": "V1 (pai dançando, 2024)", "V2": "V2 (latão, 2024)", "HB": "Tropical Ville (hoje)", "HA": "Jardim Aclimação (hoje)",
         "HC": "Florais (hoje)", "HD": "Fabrício hoje (rolete)", "HE": "IMG_1663 (hoje, 4K)", "HG": "carnes no rolete (hoje)", "HK": "costela na grade (hoje)", "V3": "V3 (Fabrício, costela crua, 2025)", "V4": "V4 (Fabrício na churrasqueira de casa)", "FA1": "fachada 1 (vídeo novo)", "FA2": "fachada 2 (IMG_1429)"}
rows = []
for i, s in enumerate(E["segments"], 1):
    k = s["kind"]
    if k == "clip": src = f'{NOMES[s["src"]]} {s["src_t0"]:.2f}s'
    elif k == "rewind": src = f'{NOMES[s["src"]]} {s["src_t1"]:.2f}→{s["src_t0"]:.2f}s (ré 4x)'
    elif k in ("foto", "album"): src = f'F{s["f"]}'
    elif k == "split": src = f'{NOMES[s["l"][0]]} {s["l"][1]}s | {NOMES[s["r"][0]]} {s["r"][1]}s'
    elif k == "wall": src = "mural: F1–F6 + 6 quadros de V1/V2"
    else: src = "logo"
    rows.append(f'| {i} | {s["ini"]:.2f}–{s["fim"]:.2f} | {s["b0"]}–{s["b1"]} | {k} | {src} |')
open(P("edl.md"), "w").write("# EDL — A nossa história\n\n"
    f'Grade: {E["bpm"]} BPM (batida {beat:.4f} s). Música do começo ao fim: vídeo 0 s = {23.395+beat:.3f} s da gravação de "Time" ("And you run…") '
    f'(b32 "The sun is the same…" = {32*beat:.2f} s, b112 "the song is over" = {112*beat:.2f} s). Duração {E["total"]:.2f} s.\n\n'
    "| # | tempo (s) | batidas | tipo | fonte |\n|---|---|---|---|---|\n" + "\n".join(rows) + "\n")

p = probe(OUT); v = [s for s in p["streams"] if s.get("width")][0]; a = [s for s in p["streams"] if s.get("sample_rate")][0]
dur = float(p["format"]["duration"])
cuts = [s["ini"] for s in E["segments"][1:]]
on = sum(1 for c in cuts if abs(c / beat - round(c / beat)) * beat <= 1 / FPS + 1e-6)
Ip, TPp = loud(PREV); Io, TPo = loud(OUT)
print(f'Q1 {v["codec_name"]} {v["profile"]} {v["width"]}x{v["height"]} {v["r_frame_rate"]} {v["pix_fmt"]} | {a["codec_name"]} {a["sample_rate"]} Hz {a["channels"]}ch')
print(f'Q2 duração {dur:.2f} s')
print(f'Q8 com música {Ip} LUFS TP {TPp} | final sem música {Io} LUFS TP {TPo}')
print(f'Q9 cortes na batida (±1 quadro): {on}/{len(cuts)}')
print(f'tamanho final {int(p["format"]["size"])/1e6:.1f} MB, {int(p["format"]["bit_rate"])/1e6:.1f} Mbps')
