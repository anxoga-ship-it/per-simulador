import re, json, unicodedata, sys
src="/root/.claude/projects/-home-claude/38807202-562d-5e0d-a88d-e3274e4405ca/tool-results/project-doc-1319c411-5aa6-48b1-83aa-93a625e19fc7.txt"
lines=open(src,encoding='utf-8').read().split('\n')
unit=None; exam=0; qs=[]; cur=None; opt=None
UNIT=re.compile(r'UNIDAD TE[ÓO]RICA\s+(\d+)')
QRE=re.compile(r'^\s*(\d{1,2})\s*[\.\-]+\s*(.*)')
ORE=re.compile(r'^\s*([a-dA-D])\s*\)\s*(.*)')
def close():
    global cur
    if cur and len(cur['o'])==4: qs.append(cur)
    cur=None
for ln in lines:
    if 'EXAMEN PARA LA OBTENCI' in ln or 'EXAMEN TEÓRICO PARA LA OBTENCI' in ln:
        close(); exam+=1
    m=UNIT.search(ln)
    if m: close(); unit=int(m.group(1)); continue
    if unit is None: continue
    mq=QRE.match(ln); mo=ORE.match(ln)
    if mo and cur is not None and len(cur['o'])<4 and mo.group(1).lower()==('abcd'[len(cur['o'])]):
        cur['o'].append(mo.group(2)); cur['ts'].append(ln.endswith(' ')); opt=True; continue
    if mq and (cur is None or len(cur['o'])==4 or len(cur['o'])==0 and False):
        close(); cur={'u':unit,'ex':exam,'n':int(mq.group(1)),'q':mq.group(2),'o':[],'ts':[]}; opt=False; continue
    if cur is None or not ln.strip(): continue
    if cur['o']:
        cur['o'][-1]+=' '+ln.strip(); cur['ts'][-1]=ln.endswith(' ')
    else:
        cur['q']+=' '+ln.strip()
close()
def norm(s):
    s=unicodedata.normalize('NFD',s.lower()); s=''.join(c for c in s if unicodedata.category(c)!='Mn')
    return re.sub(r'[^a-z0-9]+',' ',s).strip()
seen={}; out=[]
for q in qs:
    q['q']=re.sub(r'\s+',' ',q['q']).strip(); q['o']=[re.sub(r'\s+',' ',o).strip() for o in q['o']]
    k=norm(q['q'])+'|'+'|'.join(sorted(norm(o) for o in q['o']))
    if k in seen: seen[k]['rep']+=1; continue
    q['rep']=1; seen[k]=q; out.append(q)
from collections import Counter
print('exams',exam,'raw',len(qs),'dedup',len(out))
print(sorted(Counter(q['u'] for q in out).items()))
print(sorted(Counter(q['u'] for q in qs).items()))
json.dump(out,open('dedup.json','w'),ensure_ascii=False,indent=0)
