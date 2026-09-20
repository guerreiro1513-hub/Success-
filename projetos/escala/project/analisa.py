import subprocess, os, json, numpy as np
from PIL import Image, ImageFilter, ImageStat
FF="/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
P="/home/user/Success-/projetos/escala"
S="/tmp/claude-0/-home-user-Success-/9a22310a-9d20-508e-9102-cd8c1bfbea83/scratchpad"
TAKES={"T01":9.74,"T02":2.97,"T03":4.87,"T04":2.67,"T05":10.34}
os.makedirs(S+"/an",exist_ok=True)
rep={}
for t,dur in TAKES.items():
    step=0.25
    ts=[round(x,2) for x in np.arange(0.05,dur-0.05,step)]
    subprocess.run([FF,"-y","-hide_banner","-loglevel","error","-i",f"{P}/source/{t}.mov",
                    "-vf",f"fps={1/step},scale=270:480","-q:v","3",f"{S}/an/{t}_%03d.jpg"],check=True)
    fs=sorted([f for f in os.listdir(S+"/an") if f.startswith(t+"_")])
    prev=None; rows=[]
    for i,f in enumerate(fs):
        im=Image.open(f"{S}/an/{f}").convert("RGB")
        g=im.convert("L")
        sharp=ImageStat.Stat(g.filter(ImageFilter.FIND_EDGES)).stddev[0]
        bright=ImageStat.Stat(g).mean[0]
        a=np.asarray(g,dtype=np.float32)
        mot=0.0 if prev is None else float(np.abs(a-prev).mean())
        prev=a
        r,gg,b=[ImageStat.Stat(im).mean[k] for k in range(3)]
        rows.append(dict(t=round(i*step+0.05,2),nitidez=round(sharp,1),brilho=round(bright,1),
                         movimento=round(mot,2),calor=round((r-b),1)))
    rep[t]=rows
    sh=[x["nitidez"] for x in rows]; mo=[x["movimento"] for x in rows][1:]
    best=max(rows,key=lambda x:x["nitidez"])
    print(f"{t}  dur {dur:5.2f}s  nitidez med {np.mean(sh):5.1f} (min {min(sh):.1f} max {max(sh):.1f})"
          f"  movimento med {np.mean(mo):5.2f}  calor med {np.mean([x['calor'] for x in rows]):5.1f}"
          f"  pico de nitidez em {best['t']}s")
json.dump(rep,open(f"{P}/project/analise_tomadas.json","w"),indent=1,ensure_ascii=False)
