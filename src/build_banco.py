import json, re, unicodedata, collections
exec(open('parse_dgmm_fix.py').read().split('all_q = []')[0])
old=json.load(open('/home/claude/per-simulador/src/preguntas_oficiales.json'))
def key(q): return norm(q['q'])+'|'+'|'.join(sorted(norm(o) for o in q['o']))
oldD={}
for q in old['Q']:
    if q['k']=='D': oldD.setdefault(key(q),q)
raw=[]; tests=collections.OrderedDict()
for cid,label,en,pl in CONV:
    Q=parse_questions(en); A=parse_answers(pl)
    for (test,lib),qs in Q.items():
        if lib: continue
        if test=='00' and cid=='2021-02': test='05'
        ans=A.get((test,lib))
        if not ans: continue
        if len(qs) < 40 and (cid,test)==('2020-12','06'): continue   # PNB liberado sin marca
        tag=f"{label} · Test {test}"
        for q in qs:
            a=ans.get(q['n'])
            if a is None or len(q['o'])!=4 or q['n'] in EXCL.get((cid,test),set()): continue
            t=q['t'] or pos_topic(q['n'])
            if len(qs)==45 and pos_topic(q['n'])!=t: t=pos_topic(q['n'])
            if t is None: continue
            r={'id':f"{cid}-{test}-{q['n']}",'t':t,'q':clean(q['q'],True),'o':[clean(o) for o in q['o']],'a':'ABCD'.index(a),'tag':tag,'n':q['n']}
            raw.append(r); tests.setdefault((cid,label,test),[]).append(r)
groups=collections.OrderedDict()
for r in raw: groups.setdefault(key(r),[]).append(r)
newQ=[]; idof={}; conflicts=[]
for k,rs in groups.items():
    o=oldD.get(k)
    base=rs[0]
    qid=o['id'] if o else base['id']
    ansset={r['o'][r['a']] for r in rs}
    if len(ansset)>1: conflicts.append((qid,[r['tag'] for r in rs]))
    s=[]; [s.append(r['tag']) for r in rs if r['tag'] not in s]
    q=o.copy() if o else {'id':qid,'t':base['t'],'q':base['q'],'o':base['o'],'a':base['a'],'k':'D'}
    q['s']=s
    newQ.append(q)
    for r in rs: idof[id(r)]=qid
T=[]
for (cid,label,test),rs in tests.items():
    ids=[]; [ids.append(idof[id(r)]) for r in rs if idof[id(r)] not in ids]
    T.append({'name':f"{label} · Test {test}",'c':label,'ids':ids,'n':len(ids)})
T.reverse()
oldids={q['id'] for q in old['Q'] if q['k']=='D'}; newids={q['id'] for q in newQ}
print('D antes',len(oldids),'ahora',len(newids),'nuevas',len(newids-oldids),'perdidas',len(oldids-newids))
print('tests antes',len(old['T']),'ahora',len(T)); print('conflictos',len(conflicts), conflicts[:5])
for i in sorted(oldids-newids)[:20]: print('PERDIDA',i)
json.dump({'newQ':newQ,'T':T},open('dgmm_new.json','w'),ensure_ascii=False)
