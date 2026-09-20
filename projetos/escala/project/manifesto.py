import json
# posicao na linha do tempo em quadros a 30 fps. 640 quadros = 21,333 s
# 90 BPM -> 1 tempo = 20 quadros exatos
EDL=[
 # id     take  in(s)  quadros  z0    z1    fy    grade  papel
 ("h1","T04", 0.90, 45, 1.02,1.12, 0.50,"GA","gancho: a tomada mais nitida do lote"),
 ("h2","T03", 3.60, 40, 1.12,1.02, 0.50,"GA","mesma churrasqueira, outro angulo"),
 ("h3","T02", 0.30, 35, 1.02,1.11, 0.50,"GA","costela"),
 ("h4","T03", 0.20, 25, 1.11,1.02, 0.50,"GA","fumaca, a mais quente do lote"),
 ("h5","T04", 0.05, 20, 1.02,1.12, 0.50,"GA","aperta o ritmo"),
 ("h6","T02", 1.40, 15, 1.14,1.24, 0.50,"GA","antecipacao: meio segundo, empurra pra dentro"),
 ("r1","T01", 0.30,120, 1.62,1.12, 0.92,"GB","REVEAL. impacto musical no primeiro quadro"),
 ("s1","T01", 4.60, 60, 1.16,1.26, 0.90,"GB","escala: a fileira correndo"),
 ("s2","T04", 1.60, 20, 1.06,1.14, 0.50,"GA","corte de carne, casa movimento"),
 ("s3","T01", 6.70, 40, 1.18,1.28, 0.90,"GB","volta pra fileira"),
 ("s4","T03", 2.70, 20, 1.04,1.12, 0.50,"GA","brasa"),
 ("s5","T01", 8.10, 40, 1.20,1.30, 0.88,"GB","ultima passada"),
 ("b1","T05", 2.40, 80, 1.00,1.05, 0.50,"GC","a frase dele, corta na pausa natural de 5,07 s"),
 ("b2","END", 9.55, 80, 1.00,1.04, 0.88,"GB","fecho: quadro congelado + brasao"),
]
pos=0; out=[]
for i,(cid,take,tin,nf,z0,z1,fy,gr,why) in enumerate(EDL):
    out.append(dict(id=cid,take=take,entrada_fonte=tin,quadro_inicio=pos,quadros=nf,
                    tempo_inicio=round(pos/30,3),duracao=round(nf/30,3),
                    zoom=[z0,z1],janela_vertical=fy,grade=gr,motivo=why))
    pos+=nf
assert pos==640, pos
json.dump(dict(fps=30,largura=1080,altura=1920,quadros=pos,duracao=round(pos/30,3),
               bpm=90,quadros_por_tempo=20,
               impacto_musical=dict(fonte_s=70.605,quadro=180,tempo_s=6.000),
               cortes=out), open("/home/user/Success-/projetos/escala/project/manifesto.json","w"),
          indent=1,ensure_ascii=False)
print("%d cortes, %d quadros, %.3f s"%(len(out),pos,pos/30))
for c in out:
    print("  %-3s %-4s  %6.3f s  %5.2f s  z %.2f->%.2f  %s"%(
        c["id"],c["take"],c["tempo_inicio"],c["duracao"],c["zoom"][0],c["zoom"][1],c["grade"]))
