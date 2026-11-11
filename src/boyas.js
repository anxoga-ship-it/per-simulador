
/* ---------- Balizamiento: fichas de marcas IALA región A ---------- */
const BC={R:"#D7332B",G:"#1E8E4E",K:"#151C21",Y:"#F2C230",W:"#F7F7F2",B:"#2456A6"};
const LIGHTC={R:"#FF4A3D",G:"#2EF29A",W:"#FFF4D6",Y:"#FFC23A",B:"#4F8BFF"};
// patrones de luz: [periodo s, [[inicio,fin,color],...]]
function fl(n,on,gap,c){ const a=[]; let t=0; for(let i=0;i<n;i++){ a.push([t,t+on,c]); t+=on+gap; } return a; }
const BUOYS=[
 {k:"bab",n:"Lateral de babor",cat:"Lateral",bands:["R"],top:"cyl",topC:"R",
  col:"Roja",tope:"Un cilindro rojo",luz:"Roja, cualquier ritmo salvo grupos de 2+1 (p. ej. Fl R 4s)",pat:[4,fl(1,.6,0,"R")],
  ind:"Lado de babor del canal al entrar en puerto (región A). Numeración par.",pasar:"Entrando en puerto, dejarla por babor; saliendo, por estribor."},
 {k:"est",n:"Lateral de estribor",cat:"Lateral",bands:["G"],top:"coneU",topC:"G",
  col:"Verde",tope:"Un cono verde con el vértice hacia arriba",luz:"Verde, cualquier ritmo salvo grupos de 2+1 (p. ej. Fl G 4s)",pat:[4,fl(1,.6,0,"G")],
  ind:"Lado de estribor del canal al entrar en puerto (región A). Numeración impar.",pasar:"Entrando en puerto, dejarla por estribor; saliendo, por babor."},
 {k:"mbab",n:"Canal principal a estribor",cat:"Lateral modificada",bands:["R","G","R"],top:"cyl",topC:"R",
  col:"Roja con una banda horizontal verde",tope:"Un cilindro rojo",luz:"Roja, grupos de 2+1 destellos: Fl(2+1) R",pat:[10,[[0,.5,"R"],[1.2,1.7,"R"],[3.4,3.9,"R"]]],
  ind:"Bifurcación: el canal principal (preferido) sigue a estribor.",pasar:"Entrando en puerto y siguiendo el canal principal, dejarla por babor."},
 {k:"mest",n:"Canal principal a babor",cat:"Lateral modificada",bands:["G","R","G"],top:"coneU",topC:"G",
  col:"Verde con una banda horizontal roja",tope:"Un cono verde con el vértice hacia arriba",luz:"Verde, grupos de 2+1 destellos: Fl(2+1) G",pat:[10,[[0,.5,"G"],[1.2,1.7,"G"],[3.4,3.9,"G"]]],
  ind:"Bifurcación: el canal principal (preferido) sigue a babor.",pasar:"Entrando en puerto y siguiendo el canal principal, dejarla por estribor."},
 {k:"N",n:"Cardinal Norte",cat:"Cardinal",bands:["K","Y"],top:"NN",topC:"K",
  col:"Negra arriba y amarilla abajo",tope:"Dos conos negros superpuestos con los vértices hacia arriba",luz:"Blanca, centelleante continua: Q o VQ",pat:[1,[[0,.4,"W"]]],
  ind:"Las aguas navegables están al norte de la marca.",pasar:"Pasar por el norte de la marca."},
 {k:"E",n:"Cardinal Este",cat:"Cardinal",bands:["K","Y","K"],top:"EE",topC:"K",
  col:"Negra con una banda horizontal amarilla",tope:"Dos conos negros unidos por sus bases (forma de rombo)",luz:"Blanca, grupos de 3 centelleos: Q(3) 10s o VQ(3) 5s",pat:[10,fl(3,.4,.6,"W")],
  ind:"Las aguas navegables están al este de la marca.",pasar:"Pasar por el este de la marca."},
 {k:"S",n:"Cardinal Sur",cat:"Cardinal",bands:["Y","K"],top:"SS",topC:"K",
  col:"Amarilla arriba y negra abajo",tope:"Dos conos negros superpuestos con los vértices hacia abajo",luz:"Blanca, 6 centelleos + 1 destello largo: Q(6)+LFl 15s",pat:[15,fl(6,.4,.6,"W").concat([[6,8,"W"]])],
  ind:"Las aguas navegables están al sur de la marca.",pasar:"Pasar por el sur de la marca."},
 {k:"W",n:"Cardinal Oeste",cat:"Cardinal",bands:["Y","K","Y"],top:"WW",topC:"K",
  col:"Amarilla con una banda horizontal negra",tope:"Dos conos negros unidos por sus vértices (forma de copa)",luz:"Blanca, grupos de 9 centelleos: Q(9) 15s o VQ(9) 10s",pat:[15,fl(9,.4,.6,"W")],
  ind:"Las aguas navegables están al oeste de la marca.",pasar:"Pasar por el oeste de la marca."},
 {k:"PA",n:"Peligro aislado",cat:"Peligro aislado",bands:["K","R","K"],top:"2B",topC:"K",
  col:"Negra con una o varias bandas horizontales rojas",tope:"Dos esferas negras superpuestas",luz:"Blanca, grupos de 2 destellos: Fl(2)",pat:[5,fl(2,.5,1,"W")],
  ind:"Peligro de pequeña extensión rodeado de aguas navegables.",pasar:"Se puede pasar por cualquier lado, sin acercarse."},
 {k:"AN",n:"Aguas navegables",cat:"Aguas navegables",bands:["R","W","R","W"],vert:true,top:"1B",topC:"R",
  col:"Franjas verticales rojas y blancas",tope:"Una esfera roja",luz:"Blanca: isofase, ocultaciones, un destello largo cada 10 s (LFl 10s) o Morse «A»",pat:[10,[[0,2,"W"]]],
  ind:"Aguas navegables alrededor: centro o eje de canal, punto de recalada.",pasar:"Se puede pasar por cualquier lado; se suele dejar por babor."},
 {k:"ES",n:"Marca especial",cat:"Especial",bands:["Y"],top:"X",topC:"Y",
  col:"Amarilla",tope:"Un aspa amarilla en forma de X",luz:"Amarilla, cualquier ritmo que no se confunda con los de las luces blancas (p. ej. Fl Y 5s)",pat:[5,fl(1,.8,0,"Y")],
  ind:"Zona o elemento especial: baño, cables, tuberías, ejercicios, recreo, vertidos...",pasar:"No sirve para navegar: consultar la carta."},
 {k:"PN",n:"Peligro nuevo",cat:"Peligro nuevo",bands:["B","Y","B","Y"],vert:true,top:"+",topC:"Y",
  col:"Franjas verticales azules y amarillas (en igual número, de 4 a 8)",tope:"Una cruz amarilla vertical (+)",luz:"Alternativa azul y amarilla: Al.Bu.Y",pat:[3,[[0,1,"B"],[1.5,2.5,"Y"]]],
  ind:"Peligro nuevo aún no cartografiado (p. ej. un naufragio reciente).",pasar:"Balizarlo como cualquier otro peligro: no acercarse."}
];
const BK={}; BUOYS.forEach(b=>BK[b.k]=b);
function topSVG(t,c,x,y){ const F=BC[c];
  const coneU=(yy)=>`<polygon points="${x-10},${yy+14} ${x+10},${yy+14} ${x},${yy}" fill="${F}"/>`;
  const coneD=(yy)=>`<polygon points="${x-10},${yy} ${x+10},${yy} ${x},${yy+14}" fill="${F}"/>`;
  if(t==="cyl") return `<rect x="${x-8}" y="${y}" width="16" height="24" fill="${F}"/>`;
  if(t==="coneU") return coneU(y+6);
  if(t==="NN") return coneU(y-6)+coneU(y+12);
  if(t==="SS") return coneD(y-6)+coneD(y+12);
  if(t==="EE") return coneU(y-6)+coneD(y+10);
  if(t==="WW") return coneD(y-6)+coneU(y+10);
  if(t==="2B") return `<circle cx="${x}" cy="${y-1}" r="7" fill="${F}"/><circle cx="${x}" cy="${y+17}" r="7" fill="${F}"/>`;
  if(t==="1B") return `<circle cx="${x}" cy="${y+10}" r="9" fill="${F}"/>`;
  if(t==="X") return `<path d="M${x-9},${y+2} L${x+9},${y+20} M${x+9},${y+2} L${x-9},${y+20}" stroke="${F}" stroke-width="5" stroke-linecap="round"/>`;
  if(t==="+") return `<path d="M${x},${y-2} L${x},${y+24} M${x-10},${y+11} L${x+10},${y+11}" stroke="${F}" stroke-width="5" stroke-linecap="round"/>`;
  return ""; }
let BID=0;
function buoySVG(b,opt={}){ const id="b"+(++BID), night=!!opt.night, x=70;
  const body={x:48,y:64,w:44,h:52};
  let bands="";
  b.bands.forEach((c,i,a)=>{ if(b.vert) bands+=`<rect x="${(body.x+i*body.w/a.length).toFixed(1)}" y="${body.y}" width="${(body.w/a.length+.4).toFixed(1)}" height="${body.h}" fill="${BC[c]}"/>`;
    else bands+=`<rect x="${body.x}" y="${(body.y+i*body.h/a.length).toFixed(1)}" width="${body.w}" height="${(body.h/a.length+.4).toFixed(1)}" fill="${BC[c]}"/>`; });
  const sky=night?`<linearGradient id="${id}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#050D17"/><stop offset="1" stop-color="#11263A"/></linearGradient>`
                 :`<linearGradient id="${id}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#BFD7E6"/><stop offset="1" stop-color="#EAF2F5"/></linearGradient>`;
  const lamp=`<g class="blamp" data-k="${b.k}"><circle cx="${x}" cy="58" r="18" fill="url(#${id}g)" opacity="0"/><circle cx="${x}" cy="58" r="4.5" fill="${night?"#2A3A46":"#C9D2D6"}"/></g>`;
  const glow=`<radialGradient id="${id}g"><stop offset="0" stop-color="#FFFFFF" stop-opacity=".9"/><stop offset="1" stop-color="#FFFFFF" stop-opacity="0"/></radialGradient>`;
  const dim=night?' opacity=".18"':'';
  return `<svg viewBox="0 0 140 150" role="img" aria-label="${night?"Luz de noche de una marca":"Marca: "+esc(b.col)+", tope "+esc(b.tope)}">
   <defs>${sky}${glow}</defs><rect width="140" height="150" fill="url(#${id}s)"/>
   <g${dim}>
    <line x1="${x}" y1="64" x2="${x}" y2="26" stroke="#24333D" stroke-width="2.5"/>
    <rect x="${x-6}" y="54" width="12" height="9" rx="2" fill="#3A4A55"/>
    ${topSVG(b.top,b.topC,x,14)}
    ${bands}<rect x="${body.x}" y="${body.y}" width="${body.w}" height="${body.h}" fill="none" stroke="#24333D" stroke-width="1.2"/>
    <path d="M34,116 L106,116 L98,128 L42,128 Z" fill="#24333D"/>
   </g>
   <path d="M0,124 Q17,120 35,124 T70,124 T105,124 T140,124 L140,150 L0,150 Z" fill="${night?"#071420":"#5D8496"}"/>
   ${lamp}</svg>`; }
// animación de las luces
let BLT0=performance.now(), BLraf=null;
function blampLoop(){
  const t=(performance.now()-BLT0)/1000;
  document.querySelectorAll(".blamp").forEach(g=>{ const b=BK[g.dataset.k]; if(!b) return; const [P,segs]=b.pat; const tt=t%P;
    const s=segs.find(x=>tt>=x[0]&&tt<x[1]); const glow=g.children[0], dot=g.children[1];
    if(s){ glow.setAttribute("opacity","1"); glow.style.fill=""; dot.setAttribute("fill",LIGHTC[s[2]]); glow.setAttribute("fill",LIGHTC[s[2]]); }
    else { glow.setAttribute("opacity","0"); dot.setAttribute("fill", g.closest("svg").querySelector("rect").getAttribute("fill").includes("url")?"#2A3A46":"#2A3A46"); } });
  BLraf=requestAnimationFrame(blampLoop);
}
if(!BLraf && typeof requestAnimationFrame==="function") BLraf=requestAnimationFrame(blampLoop);
function buoyFig(f){ const b=BK[f.b]; return `<figure>${buoySVG(b,{night:f.night})}<figcaption>${f.night?"De noche: observa el ritmo de la luz":"De día"}</figcaption></figure>`; }

// generador de preguntas
const BATTR=[["col","Su color es: "],["tope","Su marca de tope es: "],["luz","Su luz es: "],["ind","Indica: "]];
function lc(s){ return s.charAt(0).toLowerCase()+s.slice(1); }
function genIncorrect(b){
  const attrs=shuffle(BATTR); const falseA=attrs[0][0];
  const other=shuffle(BUOYS.filter(o=>o.k!==b.k && o[falseA]!==b[falseA] && !(falseA==="tope"&&o.top===b.top)))[0];
  const opts=[{t:attrs[0][1]+lc(other[falseA]),ok:false}].concat(attrs.slice(1).map(a=>({t:a[1]+lc(b[a[0]]),ok:true})));
  const sh=shuffle(opts);
  const withFig=Math.random()<.5;
  return {id:"B-inc-"+b.k, t:"B", bt:b.k, q:withFig?"Sobre la marca de la figura, señale la INCORRECTA:":`Sobre la marca «${b.n}», señale la INCORRECTA:`,
    o:sh.map(x=>x.t), a:sh.findIndex(x=>!x.ok), fig:withFig?{b:b.k}:null,
    e:`Es falsa porque eso corresponde a «${other.n}». ${b.n}: ${lc(b.col)}; tope: ${lc(b.tope)}; luz: ${lc(b.luz)}.`};
}
function genIdent(b,night){
  const pool=night? BUOYS.filter(o=>o.k!==b.k && JSON.stringify(o.pat)!==JSON.stringify(b.pat)) : BUOYS.filter(o=>o.k!==b.k);
  const opts=shuffle([b].concat(shuffle(pool).slice(0,3)));
  return {id:(night?"B-noc-":"B-id-")+b.k, t:"B", bt:b.k, q:night?"De noche ves esta luz (mira su ritmo unos segundos). ¿Qué marca es?":"¿Qué marca es la de la figura?",
    o:opts.map(o=>o.n), a:opts.indexOf(b), fig:{b:b.k,night},
    e:`${b.n}: ${lc(b.col)}; tope: ${lc(b.tope)}; luz: ${lc(b.luz)}. ${b.ind}`};
}
function genPass(b){
  const cands=BUOYS.filter(o=>o.k!==b.k && o.pasar!==b.pasar);
  const opts=shuffle([b.pasar].concat(shuffle([...new Set(cands.map(o=>o.pasar))]).slice(0,3)));
  return {id:"B-pas-"+b.k,t:"B",bt:b.k,q:`Navegando, encuentras una marca «${b.n}». ¿Cómo debes pasarla?`,o:opts,a:opts.indexOf(b.pasar),fig:{b:b.k},e:`${b.ind} ${b.pasar}`};
}
function buoySet(kind,n){
  const out=[];
  for(let i=0;i<n;i++){ const b=BUOYS[Math.floor(Math.random()*BUOYS.length)];
    const k=kind==="mix"?["inc","inc","id","noc","pas"][Math.floor(Math.random()*5)]:kind;
    out.push(k==="inc"?genIncorrect(b):k==="id"?genIdent(b,false):k==="noc"?genIdent(b,true):genPass(b)); }
  return out;
}
function renderBuoys(){
  const cards=BUOYS.map(b=>`<div class="bcard"><div class="bpics">${buoySVG(b)}${buoySVG(b,{night:true})}</div>
    <div class="btxt"><span class="eyebrow">${esc(b.cat)}</span><h3>${esc(b.n)}</h3>
    <dl><dt>Color</dt><dd>${esc(b.col)}</dd><dt>Tope</dt><dd>${esc(b.tope)}</dd><dt>Luz</dt><dd>${esc(b.luz)}</dd><dt>Indica</dt><dd>${esc(b.ind)}</dd><dt>Cómo pasar</dt><dd>${esc(b.pasar)}</dd></dl></div></div>`).join("");
  $("#view").innerHTML=`<div class="stack"><div class="panel"><h2>Boyas y marcas</h2>
    <p class="muted">Las 12 marcas del sistema IALA, región A (España), dibujadas de día y de noche. De noche, la luz parpadea con su ritmo real: obsérvala unos segundos.</p>
    <div class="row"><button class="btn" id="bInc">Señale la incorrecta</button><button class="btn ghost" id="bId">Identificar por la figura</button><button class="btn ghost" id="bNoc">Reconocer por la luz</button><button class="btn ghost" id="bMix">Mezcla de 20</button></div></div>
    <section class="section"><h3>Trucos para no confundirlas</h3>
      <ul class="tips">
        <li><b>Cardinales:</b> los conos «apuntan» a donde está el negro. ▲▲ negro arriba = Norte · ▼▼ negro abajo = Sur · ▲▼ (rombo) negro arriba y abajo = Este · ▼▲ (copa) negro en medio = Oeste.</li>
        <li><b>Luces de las cardinales, como un reloj:</b> Este 3 · Sur 6 (+ destello largo) · Oeste 9 · Norte continuo.</li>
        <li><b>Peligro aislado:</b> «dos esferas, dos destellos». <b>Aguas navegables:</b> franjas verticales y esfera roja, luz «larga»: isofase, ocultaciones, LFl 10s o Morse A.</li>
        <li><b>Modificadas:</b> la luz 2+1 es del color de la boya. El color de la banda indica hacia dónde sigue el canal principal: banda verde = canal principal a estribor.</li>
        <li><b>Especial:</b> todo amarillo (cuerpo, aspa X y luz). <b>Peligro nuevo:</b> azul y amarillo, cruz +, luz alternativa azul-amarilla.</li>
      </ul></section>
    <section class="section"><h3>Las 12 marcas</h3><div class="bgrid2">${cards}</div></section></div>`;
  const go=(k,t)=>()=>{ const mk=()=>({kind:"practice",tab:"buoys",title:t,qs:buoySet(k,k==="mix"?20:15).map(q=>Object.assign({},q,{_o:q})),immediate:true}); const o=mk(); o.again=mk; startRun(o); };
  $("#bInc").onclick=go("inc","Boyas · señale la incorrecta"); $("#bId").onclick=go("id","Boyas · identificar");
  $("#bNoc").onclick=go("noc","Boyas · reconocer por la luz"); $("#bMix").onclick=go("mix","Boyas · mezcla");
}
