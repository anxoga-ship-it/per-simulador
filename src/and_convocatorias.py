import re, json, unicodedata, sys
src=sys.argv[1]; bank=sys.argv[2]
lines=open(src,encoding='utf-8').read().split('\n')
MES={'enero':'Enero','febrero':'Febrero','marzo':'Marzo','abril':'Abril','mayo':'Mayo','junio':'Junio','julio':'Julio','agosto':'Agosto','septiembre':'Septiembre','octubre':'Octubre','noviembre':'Noviembre','diciembre':'Diciembre'}
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]+',' ',s).strip()
UNIT=re.compile(r'UNIDAD TE[ÓO]RICA\s+(\d+)'); QRE=re.compile(r'^\s*(\d{1,2})\s*[\.\-]+\s*(.*)')
label=None; unit=None; cur=None; occ=[]
for ln in lines:
    m=re.search(r'Convocatoria:\s*(\d+)\s*(?:de\s*)?([a-záéíóú]+)\s*de\s*(\d{4})',ln,re.I)
    if m: label=f"{MES[m.group(2).lower()]} {m.group(3)}"; unit=None; continue
    mu=UNIT.search(ln)
    if mu: unit=int(mu.group(1)); continue
    if unit is None or label is None: continue
    mq=QRE.match(ln)
    if mq: occ.append([label,unit,mq.group(2)]); continue
    if occ and not re.match(r'^\s*[a-dA-D]\s*\)',ln) and occ[-1][1]==unit and len(occ[-1][2])<300 and ln.strip(): occ[-1][2]+=' '+ln.strip()
d=json.load(open(bank)); A=[q for q in d['Q'] if q.get('k')=='A']
idx={}
for lab,u,t in occ: idx.setdefault(norm(t)[:70],[]).append(lab)
miss=0
for q in A:
    k=norm(q['q'])[:70]; labs=idx.get(k)
    if not labs:
        # prefix fallback
        k2=norm(q['q'])[:40]; labs=[l for kk,v in idx.items() if kk.startswith(k2) for l in v]
    if labs:
        seen=[]; [seen.append(l) for l in labs if l not in seen]; q['s']=seen
    else: miss+=1; print('MISS',q['id'],q['q'][:80])
print('total',len(A),'miss',miss)
json.dump({q['id']:q.get('s') for q in A},open('/home/claude/work/and_conv.json','w'),ensure_ascii=False)
