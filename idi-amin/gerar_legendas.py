import re, subprocess, textwrap, bisect
FF="/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2"
SP="/tmp/claude-0/-home-user-Success-/3984993b-d45d-5b10-a462-5a80108da1e6/scratchpad"

BL=[(13.80,"m1"),(35.00,"m2"),(72.70,"m3"),(110.70,"m4"),
    (151.80,"m6"),(194.20,"m5"),(237.30,"m7"),(280.70,"m8")]
TXT=[
"Esse homem é Idi Amin. Em 1971 tomou o poder em Uganda e governou por oito anos. Quando caiu, deixou um país arruinado. Mas não chegou lá sozinho.",
"Idi Amin nasceu no noroeste de Uganda por volta de 1925. Filho de agricultor, deixou a escola na quarta série. Mas tinha quase dois metros, e foi isso que o exército colonial britânico enxergou nele. Alistou-se em 1946, quando Uganda ainda era protetorado, e serviu ao império reprimindo revoltas de africanos no Quênia. Foi campeão de boxe do país por nove anos. Na independência, em 1962, era um dos dois únicos ugandeses oficiais.",
"Este é Milton Obote, primeiro-ministro de Uganda. Ele e Amin não eram inimigos: eram sócios. Obote promoveu Amin até o comando do exército, e em 1964 montaram uma aliança lucrativa de expansão militar e contrabando. Em 1966, acusado no parlamento de desviar ouro e marfim do Congo, Amin foi protegido. Obote prendeu os ministros que o acusavam, suspendeu a Constituição e se declarou presidente.",
"Dois dias depois de rasgar a Constituição, Obote entregou a Amin o comando de todas as forças militares e policiais. Meses depois, mandou tanques atacarem o palácio do rei de Buganda. Repara na ordem dos fatos: quando o golpe veio, as regras já estavam destruídas, e não foi Amin quem as destruiu. Em vinte e cinco de janeiro de 1971, com Obote fora do país, o exército tomou o poder. E boa parte da população foi para as ruas comemorar.",
"Em 1972, depois que Israel recusou dar dinheiro e armas, Amin rompeu com o país e se aproximou da Líbia de Kadafi. A retaliação veio contra quem morava em Uganda: noventa dias para a comunidade asiática deixar o território. Cerca de cinquenta mil pessoas saíram levando quase nada. Era essa comunidade que sustentava o comércio e as plantações. Os negócios foram entregues a apoiadores sem preparo, e em pouco tempo faltava comida.",
"Por trás da fachada, Amin montou os próprios esquadrões da morte. Entre cinco e seis mil soldados foram executados, quase todos das etnias Acholi e Lango, ligadas a Obote. E a repressão não parou no exército. Em 1977, o regime mandou matar o arcebispo Janani Luwum, a maior autoridade religiosa do país. Quando um governo chega a matar o arcebispo, não sobrou instituição capaz de segurá-lo.",
"Enquanto o país afundava, Amin construía um personagem: deu a si mesmo a presidência vitalícia e condecorações britânicas que nunca recebeu. Mas a conta chegou. Em 1978, os Estados Unidos cortaram a compra de café, um terço da exportação de Uganda. Sem dinheiro e sem apoio, Amin apostou tudo numa invasão ao norte da Tanzânia. A Tanzânia contra-atacou ao lado de exilados ugandeses, e o exército de Amin, corroído pelos próprios expurgos, não resistiu.",
"Amin fugiu, viveu exilado na Arábia Saudita e morreu em 2003, sem nunca ter sido julgado. Uganda levou anos para se reerguer. O homem carregado pela multidão no começo deste vídeo era o mesmo. O povo comemorou a chegada dele. É por isso que se estuda esse período: para reconhecer o começo, não só o fim.",
]
# frases grandes do proprio documentario: so audio, sem legenda minha
BLOQ=[(24.50,28.20),(87.70,92.40),(116.80,120.70),(193.90,197.70),(280.60,286.00)]
MAXC=74

def ffdur(f):
    o=subprocess.run([FF,"-i",f],capture_output=True,text=True).stderr
    h,m,s=re.search(r"Duration: (\d+):(\d+):([\d.]+)",o).groups()
    return int(h)*3600+int(m)*60+float(s)

def silencios(f):
    o=subprocess.run([FF,"-hide_banner","-i",f,"-af","silencedetect=n=-33dB:d=0.12","-f","null","-"],
                     capture_output=True,text=True).stderr
    st=[float(x) for x in re.findall(r"silence_start: (-?[\d.]+)",o)]
    en=[float(x) for x in re.findall(r"silence_end: ([\d.]+)",o)]
    return [(max(0.0,a),b) for a,b in zip(st,en) if b>a]

def mapa_tempo(D,G,C):
    """devolve funcao posicao_de_caractere -> segundo, distribuindo os
       caracteres so pelos trechos em que a voz realmente soa"""
    runs=[]; cur=0.0
    for a,b in G:
        if a>cur: runs.append((cur,a))
        cur=max(cur,b)
    if D>cur: runs.append((cur,D))
    runs=[(a,b) for a,b in runs if b-a>0.02]
    V=sum(b-a for a,b in runs)
    lim=[0.0]; 
    for a,b in runs: lim.append(lim[-1]+C*(b-a)/V)
    def t(p):
        i=min(bisect.bisect_right(lim,p)-1,len(runs)-1); i=max(i,0)
        a,b=runs[i]; c0,c1=lim[i],lim[i+1]
        if c1<=c0: return b
        return a+(b-a)*max(0.0,min(1.0,(p-c0)/(c1-c0)))
    return t, runs

def tc(t):
    m=int(t//60); s=t-m*60
    return f"00:{m:02d}:{s:06.3f}".replace(".",",")

cues=[]
for (st,tag),txt in zip(BL,TXT):
    f=f"{SP}/narr3/{tag}.mp3"
    D=ffdur(f); G=silencios(f); C=len(txt)
    t,runs=mapa_tempo(D,G,C)
    pausas=[(a,b) for a,b in G if b-a>=0.38]
    pal=[]; p=0
    for w in txt.split():
        pal.append([st+t(p), st+t(p+len(w)), w]); p+=len(w)+1

    def bloqueada(a,b):
        m=(a+b)/2
        return any(x<=m<=y for x,y in BLOQ)
    def limites(a,b):
        lo,hi=-1e9,1e9
        for x,y in BLOQ:
            if y<=a: lo=max(lo,y)
            if x>=b: hi=min(hi,x)
        return lo,hi

    # quebra em segmentos: as palavras que caem sob a frase grande saem fora
    segs=[]; cur=[]
    for a,b,w in pal:
        if bloqueada(a,b):
            if cur: segs.append(cur); cur=[]
        else:
            if cur:
                la,lb,_=cur[-1]
                if any(la<x and b>y for x,y in BLOQ): segs.append(cur); cur=[]
            cur.append((a,b,w))
    if cur: segs.append(cur)

    for seg in segs:
        lo,hi=limites(seg[0][0],seg[-1][1])
        linhas=[]; buf=[]; nc=0
        for i,(a,b,w) in enumerate(seg):
            if buf and nc+1+len(w)>MAXC: linhas.append(buf); buf=[]; nc=0
            buf.append((a,b,w)); nc=nc+len(w)+(1 if nc else 0)
            fim_frase=w.endswith((".",":",";","!","?"))
            prox=seg[i+1][0] if i+1<len(seg) else None
            pausa=prox is not None and any(st+x<=prox+0.02 and st+y>=b-0.02 for x,y in pausas)
            if (fim_frase and nc>=34) or (pausa and nc>=50):
                linhas.append(buf); buf=[]; nc=0
        if buf: linhas.append(buf)
        for k,ln in enumerate(linhas):
            a=max(ln[0][0],lo); b=ln[-1][1]
            b=min(b+0.35, linhas[k+1][0][0]-0.05) if k+1<len(linhas) else min(b+0.45,hi,st+D)
            b=min(b,hi)
            for wx,wy in BLOQ:            # nunca invade a frase grande
                if wx-0.001<=a<wy: a=wy
            for wx,wy in BLOQ:
                if a<wx<b: b=wx
            if b-a>=1.00:
                cues.append((a,b-0.06,"\n".join(textwrap.wrap(" ".join(w for _,_,w in ln),42))))

cues.sort()
open("legendas.srt","w").write("".join(f"{i}\n{tc(a)} --> {tc(b)}\n{t}\n\n" for i,(a,b,t) in enumerate(cues,1)))
cps=[(len(t.replace('\n',' '))/(b-a),a,t) for a,b,t in cues]
print(f"{len(cues)} legendas | cps max {max(c for c,_,_ in cps):.1f} | cps min {min(c for c,_,_ in cps):.1f}")
print("mais rapidas:", [f"{c:.1f}@{a:.0f}s" for c,a,_ in sorted(cps,reverse=True)[:4]])
