import re, subprocess, json, unicodedata, sys
SRC = '/mnt/user-data/uploads/PER/examenes/'
CONV = [  # (id, etiqueta, enunciados, plantilla)
 ('2019-07','Junio 2019','examenes_050719','plantillas_corregidas_050719'),
 ('2020-12','Diciembre 2020','examenes_recreo_diciembre_2020_v1','respuestas_examenes_recreo_diciembre_2020'),
 ('2021-02','Febrero 2021','examenes_recreo_febrero_2021','plantillas_respuesta_febrero_2021'),
 ('2021-04','Abril 2021','examenes_dgmm_25_abril_2021','plantillas_correccion_dgmm_25_abril_2021_rev.2_0'),
 ('2021-07','Julio 2021','examenes_titulos_recreo_julio_2021','plantillas_respuesta_julio_2021'),
 ('2021-10','Octubre 2021','examenes_octubre_2021','plantillas_respuestas_examenes_octubre_2021'),
 ('2021-12','Diciembre 2021','examenes_diciembre_2021','1._plantillas_examenes_diciembre_2021_v1'),
 ('2022-04','Abril 2022','examenes_abril_2022','plantillas_examenes_abril_2022_v1'),
 ('2022-06','Junio 2022','examenes_recreo_junio_2022','plantillas_examenes_recreo_junio_2022_rev2'),
 ('2022-10','Octubre 2022','examenes_octubre_2022','plantillas_octubre_2022'),
 ('2022-12','Diciembre 2022','enunciados_examenes_convocatoria_de_diciembre_2022','plantilla_de_respuestas_examenes_convocatoria_de_diciembre_2022'),
 ('2023-04','Abril 2023','examenes_recreo_abril_2023','plantillas_examenes_abril_2023_rev_2_0'),
 ('2023-06','Junio 2023','examenes_recreo_junio_2023_1','plantillas_examen_junio_2023'),
 ('2023-11','Noviembre 2023','examenes_recreo_noviembre_2023','plantillas_respuesta_examenes_recreo_noviembre_2023'),
 ('2024-04','Abril 2024','enunciados_examenes_titulos_recreo_abril_2024','plantillas_respuestas_examenes_titulos_recreo_abril_2024'),
 ('2024-06','Junio 2024','enunciados_examenes_titulos_recreo_junio_2024','plantillas_respuestas_examenes_titulos_recreo_junio_2024'),
 ('2024-11','Noviembre 2024','enunciados_examenes_recreo_noviembre_2024','plantillas_examenes_noviembre_2024'),
 ('2025-04','Abril 2025','enunciados_examenes_recreo_abril_2025','plantillas-examenes_abril-2025_(rev-1)'),
 ('2025-06','Junio 2025','enunciados_examenes_junio_2025','plantilla_respuestas_examenes_junio_2025'),
 ('2025-11','Noviembre 2025','enunciados_examenes_noviembre_2025','plantilla_respuestas_noviembre_2025'),
 ('2026-04','Abril 2026','enunciados_examenes_abril_2026','plantillas_respuestas_abril_2026'),
 ('2026-06','Junio 2026','enunciados_examenes_recreo_junio_2026','plantillas_respuestas_examenes_junio_2026'),
]
# Preguntas anuladas o con varias respuestas válidas según resoluciones del tribunal (solo PER, test completo)
EXCL = {
 ('2019-07','01'):{15,31,36,37,42,44,45}, ('2019-07','02'):{8,20,37,38,39,42,45},
 ('2019-07','03'):{42,43,45}, ('2019-07','04'):{9,44,45},
 ('2023-04','01'):{19}, ('2023-04','03'):{20}, ('2023-04','02'):{13,32}, ('2023-04','04'):{14,30},
 ('2025-04','02'):{8}, ('2025-04','04'):{9},
 ('2026-04','02'):{21}, ('2026-04','04'):{20},
}
TOPIC_HDR = [
 (r'^nomenclatura', 1), (r'^elementos de amarre', 2), (r'^seguridad', 3), (r'^legislaci', 4),
 (r'^balizamiento', 5), (r'^reglamento', 6), (r'^(ripa|reglas? )', 6), (r'^maniobra', 7), (r'^emergencias', 8),
 (r'^meteorolog', 9), (r'^teor[ií]a de (la )?navegaci', 10), (r'^carta de navegaci', 11),
]
NOISE = re.compile(r'^(\d{1,2}$|Y AGENDA URBANA|AGENDA URBANA|SUBDIRECCI|ÁREA FUNCIONAL|AREA FUNCIONAL|MINISTERIO|SECRETAR|DIRECCI[ÓO]N GENERAL|DE LA MARINA|Y MOVILIDAD|DE TRANSPORTES|MARINA MERCANTE|P[áa]gina \d|-\s*\d+\s*-$|\d+\s*/\s*\d+$|C/ RUIZ|CORREO|titulosderecreo|28071)', re.I)

def txt(name, layout=False):
    args = ['pdftotext'] + (['-layout'] if layout else []) + [SRC + name + '.pdf', '-']
    return subprocess.run(args, capture_output=True, text=True).stdout

def norm(s):
    s = unicodedata.normalize('NFD', s.lower()); s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()

def sections(lines, answers=False):
    """Divide en secciones (tipo, liberado, test) -> líneas."""
    out = []; typ = None; lib = False; cur = None
    for i, raw in enumerate(lines):
        l = raw.strip()
        m = re.search(r'EXAMEN DE (CAPIT|PATR[ÓO]N DE YATE|PATR[ÓO]N DE EMBARCACIONES|PATR[ÓO]N PARA NAVEGACI|PATR[ÓO]N DE NAVEGACI)', l, re.I)
        if m:
            k = m.group(1).upper()
            typ = 'CY' if k.startswith('CAPIT') else 'PY' if 'YATE' in k else 'PER' if 'EMBARCACIONES' in k else 'PNB'
            lib = False; cur = None; continue
        if typ is None and re.search(r'EMBARCACIONES\s*$', l): pass
        if re.search(r'PNB\s*Liberado|\(Con PNB|Con PNB', l, re.I):
            lib = True; continue
        m = re.search(r'C[óo]digo de Test\s*0?\s*(\d)', l, re.I)
        if m:
            cur = {'typ': typ, 'lib': lib, 'test': '0' + m.group(1), 'lines': []}
            out.append(cur); continue
        if cur is not None: cur['lines'].append(raw)
    return out

def parse_answers(name):
    secs = sections(txt(name, layout=True).split('\n'))
    res = {}
    for s in secs:
        if s['typ'] != 'PER': continue
        key = (s['test'], s['lib']); ans = {}; last = None
        for raw in s['lines']:
            l = raw.strip()
            m = re.match(r'^(\d{1,2})\s*(.*)$', l)
            if m and (last is None or int(m.group(1)) == last + 1 or int(m.group(1)) == 1):
                n = int(m.group(1)); rest = m.group(2).strip(); last = n
                mm = re.match(r'^([A-Da-d])\.?$', rest)
                ans[n] = mm.group(1).upper() if mm else None   # None = anulada / varias válidas
            elif last is not None and l and re.match(r'^[A-D]$', l) and ans.get(last) is None and 'ANUL' not in ' '.join(s['lines']).upper()[:0]:
                pass
        if ans: res[key] = ans
    return res

def parse_questions(name):
    secs = sections(txt(name).split('\n'))
    res = {}
    for s in secs:
        if s['typ'] != 'PER': continue
        qs = []; cur = None; topic = None; expect = 1
        for raw in s['lines']:
            l = raw.strip()
            if not l or NOISE.match(l): continue
            nl = norm(l)
            hit = next((t for p, t in TOPIC_HDR if re.match(p, nl) and len(l) < 60 and not re.match(r'^\d', l)), None)
            if hit and (cur is None or len(cur['o']) == 4):
                topic = hit; continue
            m = re.match(r'^(\d{1,2})[\.\-]?\s+(\S.*)$', l) or re.match(r'^(\d{1,2})[\.\-]?$', l)
            if cur is not None and len(cur['o']) == 4 and (re.match(r'^\d{1,2}[\.\-]?\s+\S', l) or re.match(r'^[a-d]\)', l)) and not (m and int(m.group(1)) == expect):
                cur['closed'] = True; continue
            if m and int(m.group(1)) == expect and (cur is None or len(cur['o']) == 4):
                cur = {'n': expect, 'q': (m.group(2) if m.lastindex and m.lastindex >= 2 else '') or '', 'o': [], 't': topic}
                qs.append(cur); expect += 1; continue
            mo = re.match(r'^([a-d])\)\s*(.*)$', l)
            if mo and cur is not None and len(cur['o']) < 4 and mo.group(1) == 'abcd'[len(cur['o'])]:
                cur['o'].append(mo.group(2)); continue
            if cur is None or cur.get('closed'): continue
            if cur['o']:
                if len(cur['o']) == 4 and re.match(r'^(Nota|Para (las|los) preguntas|Datos|Utilice|Situaci)', l): continue
                cur['o'][-1] += ' ' + l
            else:
                cur['q'] += ' ' + l
        res[(s['test'], s['lib'])] = qs
    return res

def clean(s, q=False):
    s = re.sub(r'\s+', ' ', s).strip()
    if q: s = re.sub(r'^\d{1,2}\s+(?=[¿A-ZÁÉÍÓÚÑ«“"])', '', s)
    s = s.replace('embarcacioón', 'embarcación')
    return s

POS = [(1,4,1),(5,6,2),(7,10,3),(11,12,4),(13,17,5),(18,27,6),(28,29,7),(30,32,8),(33,36,9),(37,41,10),(42,45,11)]
def pos_topic(n):
    for a, b, t in POS:
        if a <= n <= b: return t

all_q = []; report = []
for cid, label, en, pl in CONV:
    Q = parse_questions(en); A = parse_answers(pl)
    for key, qs in Q.items():
        test, lib = key
        ans = A.get(key)
        tag = f"{label} · Test {test}" + (" (PNB liberado)" if lib else "")
        if not ans:
            report.append((tag, len(qs), 'SIN PLANTILLA')); continue
        ok = 0; bad = 0
        for q in qs:
            a = ans.get(q['n'])
            t = q['t'] or (pos_topic(q['n']) if not lib else None)
            if not lib and len(qs) == 45 and pos_topic(q['n']) != t:
                t = pos_topic(q['n'])
            if a is None or len(q['o']) != 4 or q['n'] in EXCL.get((cid, test), set()) and not lib or t is None:
                bad += 1; continue
            all_q.append({'id': f"{cid}-{test}{'L' if lib else ''}-{q['n']}", 'c': cid, 'src': tag, 'n': q['n'], 't': t,
                          'q': clean(q['q'], True), 'o': [clean(o) for o in q['o']], 'a': 'ABCD'.index(a)})
            ok += 1
        report.append((tag, len(qs), f'{ok} ok, {bad} descartadas, plantilla {len(ans)}'))
for r in report: print(r)
json.dump(all_q, open('raw_dgmm.json', 'w'), ensure_ascii=False)
print('total', len(all_q))
