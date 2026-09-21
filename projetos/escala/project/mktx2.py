exec(open('mkpktext2.py').read())
TOT=660; EXL=14
badge=Image.open("logo_key.png"); bw=430
badge=badge.resize((bw,int(bw*badge.height/badge.width)),Image.LANCZOS)
HDL=Line("@GUERREIROSGRILL",355,0.16)

# (ini, fim, pequena, grande, larg_peq, larg_grande, altura_base)
SPEC=[
 ( 20,130,"ISSO AQUI","É SÓ 1 DE 6.",380,760,0.760),
 (392,450, None, "6 CHURRASQUEIRAS.", 0,900,0.205),
 (454,512, None, "AO MESMO TEMPO.",   0,840,0.205),
]
BLK=[(s,e,(Line(sm,tws,0.055) if sm else None),Line(bg,twb,0.012),by)
     for s,e,sm,bg,tws,twb,by in SPEC]
def stg(ln,b):
    n=max(1,len(ln.txt)-1); return max(0.55,min(2.4,b/float(n)))
for s,e,S_,B_,by in BLK:
    for ln,off in ((S_,0),(B_,0 if S_ is None else 14)):
        if ln is None: continue
        need=stg(ln,12)*(len(ln.txt)-1)+13; have=(e-s)-off-EXL
        assert need<=have,"sem tempo: %r precisa %.1f tem %d"%(ln.txt,need,have)
        assert 540-ln.w/2>14 and 540+ln.w/2<1066,"estoura a borda: %r"%ln.txt
print("linhas verificadas")

LOCK=620
OUT="tx2"; shutil.rmtree(OUT,ignore_errors=True); os.makedirs(OUT)
scrim=Image.new("RGBA",(W,H),(0,0,0,0)); sp=scrim.load()
for y in range(H):
    v=int((clamp((y-H*0.40)/(H*0.60))**1.4)*208)
    for x in range(W): sp[x,y]=(0,0,0,v)

for fr in range(TOT):
    c=Image.new("RGBA",(W,H),(0,0,0,0))
    for s,e,S_,B_,by in BLK:
        if not (s<=fr<e): continue
        r=fr-s; exr=(fr-(e-EXL)) if fr>=e-EXL else None
        base=int(H*by)
        gap=int((S_.cap*0.62 if S_ else 0)+B_.cap*0.72)
        if S_ is not None:
            draw_line(c,S_,W//2,base,r,stag=stg(S_,10),ent=11,exit_r=exr,exit_len=EXL)
        r2=r if S_ is None else r-14
        if r2>0:
            draw_line(c,B_,W//2,base+gap,r2,stag=stg(B_,12),ent=13,ghost=True,
                      exit_r=exr,exit_len=EXL)
            pr=out_cubic(clamp((r2-20)/13.0))
            if exr is not None: pr*=(1-clamp(exr/float(EXL)))
            if pr>0:
                rw=int(B_.w*0.92*pr)
                if rw>2: c.paste(rule(rw),(W//2-int(B_.w*0.46), base+gap+int(B_.cap*0.72)),rule(rw))
    if fr>=LOCK:
        sa=out_cubic(seg(fr,LOCK,LOCK+12))
        sc2=scrim.copy()
        if sa<0.999: sc2.putalpha(sc2.split()[3].point(lambda v:int(v*sa)))
        c=Image.alpha_composite(sc2,c)
        if fr>=LOCK+4:
            t=seg(fr,LOCK+4,LOCK+20); s2=1.0+0.24*(1-out_back(t))
            a=out_cubic(seg(fr,LOCK+4,LOCK+12))
            b=badge.resize((max(1,int(bw*s2)),max(1,int(badge.height*s2))),Image.LANCZOS)
            bl=4.0*(1-out_cubic(seg(fr,LOCK+4,LOCK+14)))
            if bl>0.35: b=b.filter(ImageFilter.GaussianBlur(bl))
            if a<0.999:
                b=b.copy(); b.putalpha(b.split()[3].point(lambda v:int(v*a)))
            by2=1070-int(18*(1-out_cubic(t)))
            c.paste(b,(W//2-b.width//2,by2-b.height//2),b)
            bot=by2+badge.height//2
            pr=out_cubic(seg(fr,LOCK+20,LOCK+30))
            if pr>0:
                rw=int(295*pr)
                if rw>2: c.paste(rule(rw,7),(W//2-rw//2,bot+34),rule(rw,7))
            draw_line(c,HDL,W//2,bot+104,fr-(LOCK+20),stag=stg(HDL,10),ent=11)
    c.save(f"{OUT}/t_{fr:04d}.png")
print("quadros",len(os.listdir(OUT)))
