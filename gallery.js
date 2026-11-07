/* contrib-gallery: demos run on made-up sample data, nothing is fetched. */
const CATS=['Space','Games','3D','Dev','Music','Minimal','Nature'];
const META={
  1:{id:'constellation',cat:'Space'},2:{id:'orbit-rings',cat:'Space'},3:{id:'terminal-heatmap',cat:'Dev'},
  4:{id:'pulse-line',cat:'Minimal'},5:{id:'radial-bars',cat:'Minimal'},6:{id:'tower',cat:'3D'},
  7:{id:'equalizer',cat:'Music'},8:{id:'snake',cat:'Games'},9:{id:'pac-man',cat:'Games'},
  10:{id:'falling-blocks',cat:'Games'},11:{id:'radar-sweep',cat:'Space'},12:{id:'punch-card',cat:'Minimal'},
  13:{id:'streak-timeline',cat:'Minimal'},14:{id:'word-cloud',cat:'Minimal'},15:{id:'repo-bubbles',cat:'Minimal'},
  16:{id:'spiral-galaxy',cat:'Space'},17:{id:'solar-system',cat:'Space'},18:{id:'moon-phases',cat:'Space'},
  19:{id:'meteor-shower',cat:'Space'},20:{id:'git-graph',cat:'Dev'},21:{id:'matrix-rain',cat:'Dev'},
  22:{id:'hex-dump',cat:'Dev'},23:{id:'htop-monitor',cat:'Dev'},24:{id:'ridgeline',cat:'3D'},
  25:{id:'topographic-map',cat:'Nature'},26:{id:'dna-helix',cat:'3D'},27:{id:'barcode',cat:'Minimal'},
  101:{id:'vinyl-record',cat:'Music'},102:{id:'piano-roll',cat:'Music'},
  103:{id:'tree-growth',cat:'Nature'},104:{id:'ocean-waves',cat:'Nature'},
  105:{id:'space-invaders',cat:'Games'},106:{id:'rpg-status',cat:'Games'},
  107:{id:'skyline',cat:'3D'},108:{id:'terrain-mesh',cat:'3D'}
};
/* styles that already have a generator you can use */
const READY=new Map([
  ['spiral-galaxy',520],['htop-monitor',578],['constellation',400],['ridgeline',580],
  ['vinyl-record',580],['piano-roll',380],['tree-growth',600],['ocean-waves',580],
  ['space-invaders',430],['rpg-status',430],['skyline',610],['terrain-mesh',510]
]);
const REPO='inferism/contrib-gallery';
const THEMES={mono:'#ffffff',ice:'#7dd3fc',ember:'#fb923c',matrix:'#4ade80',sakura:'#f9a8d4',violet:'#c4b5fd'};
let theme='mono',ACC=[255,255,255],current=null;
const sampleUrl=id=>`samples/${theme}/${id}.svg`;

function workflowFor(id,th){
  /* the chosen theme is set; the other options are left as commented hints */
  const line=['\n          '+(th&&th!=='mono'?`theme: ${th}`:'# theme: ice'),
    '\n          # mode: light      # for light READMEs',
    '\n          # frame: none      # no border or corner brackets',
    '\n          # header: hide     # hide the title lines'].join('');
  return `name: Contribution chart
on:
  schedule:
    - cron: "0 18 * * *"
  workflow_dispatch:

permissions:
  contents: write

jobs:
  chart:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ${REPO}@main
        with:
          style: ${id}${line}
      - name: Commit and push
        run: |
          git config user.name "\${{ github.repository_owner }}"
          git config user.email "\${{ github.repository_owner_id }}+\${{ github.repository_owner }}@users.noreply.github.com"
          git add -A
          git commit -m "chore: update contribution chart" || exit 0
          git push`}
function readmeFor(id){return `<p align="center">
  <img src="./contrib-charts/${id}.svg" alt="My contribution chart" width="100%" />
</p>`}

function block(label,file,text){
  const wrap=document.createElement('div');wrap.className='snip';
  const bar=document.createElement('div');bar.className='snip-bar';
  const name=document.createElement('span');name.textContent=label+' '+file;
  const btn=document.createElement('button');btn.type='button';btn.textContent='copy';
  btn.setAttribute('aria-label','Copy '+file);
  const pre=document.createElement('pre');pre.className='code';pre.tabIndex=0;pre.textContent=text;
  btn.addEventListener('click',async()=>{
    try{await navigator.clipboard.writeText(text);btn.textContent='copied';}
    catch(e){const r=document.createRange();r.selectNodeContents(pre);const sel=getSelection();sel.removeAllRanges();sel.addRange(r);btn.textContent='press Ctrl+C';}
    setTimeout(()=>btn.textContent='copy',1800);
  });
  bar.append(name,btn);wrap.append(bar,pre);return wrap;
}

function card(n,title,note,html){
  const m=META[n]||{id:'style-'+n,cat:'Minimal'},ready=READY.has(m.id);
  const el=document.createElement('article');
  el.className='card'+(ready?' ready':'');el.id=m.id;el.dataset.cat=m.cat;
  const head=document.createElement('header');
  const h=document.createElement('h2');h.textContent=title;
  const tag=document.createElement('span');tag.className='tag'+(ready?' ok':'');tag.textContent=ready?'ready to use':'preview only';
  head.append(h,tag);
  const p=document.createElement('p');p.className='note';p.textContent=note;
  const stage=document.createElement('div');stage.className='stage';
  if(ready){
    /* ready styles show the real generated sample as a thumbnail; click for full size and snippets */
    const b=document.createElement('button');b.type='button';b.className='thumb';
    b.setAttribute('aria-label','Open '+title+' full size, with snippets');
    const img=document.createElement('img');img.dataset.id=m.id;img.src=sampleUrl(m.id);
    img.width=1000;img.height=READY.get(m.id);img.loading='lazy';img.alt=title+': '+note;
    b.append(img);b.addEventListener('click',()=>openStyle(m.id,title,note));stage.append(b);
  }else stage.innerHTML=html;
  el.append(head,p,stage);
  if(ready){
    const u=document.createElement('button');u.type='button';u.className='use-btn';u.textContent='Use this style';
    u.addEventListener('click',()=>openStyle(m.id,title,note));el.append(u);
  }else{
    const q=document.createElement('p');q.className='soon';q.textContent='Live preview only. The generator for this style is coming soon.';el.append(q);
  }
  document.getElementById('grid').appendChild(el);
  return el;
}

/* full-size viewer with the snippets */
function openStyle(id,title,note){
  current={id,title,note};renderViewer();
  const d=document.getElementById('viewer');if(!d.open)d.showModal();
}
function renderViewer(){
  if(!current)return;
  const box=document.getElementById('viewer-body');box.textContent='';
  const h=document.createElement('h2');h.id='viewer-title';h.textContent=current.title;
  const p=document.createElement('p');p.className='note';p.textContent=current.note;
  const img=document.createElement('img');img.className='full';img.src=sampleUrl(current.id);img.alt=current.title+': '+current.note;
  box.append(h,p,img,block('1.','.github/workflows/contrib-chart.yml',workflowFor(current.id,theme)),block('2.','README.md',readmeFor(current.id)));
}
function initViewer(){
  const d=document.getElementById('viewer');
  d.addEventListener('click',e=>{if(e.target===d)d.close()});
  d.addEventListener('close',()=>{current=null});
  d.querySelector('.close').addEventListener('click',()=>d.close());
}

/* color themes */
function applyTheme(name){
  if(!THEMES[name])name='mono';
  theme=name;
  const c=THEMES[name];
  document.documentElement.style.setProperty('--hi',c);
  ACC=[1,3,5].map(i=>parseInt(c.slice(i,i+2),16));
  document.querySelectorAll('img[data-id]').forEach(i=>{i.src=sampleUrl(i.dataset.id)});
  document.querySelectorAll('#themes button').forEach(b=>b.setAttribute('aria-pressed',b.dataset.theme===name));
  renderViewer();
  try{localStorage.setItem('cg-theme',name)}catch(e){}
}
function buildThemes(){
  const box=document.getElementById('themes');
  const label=document.createElement('span');label.textContent='theme';box.append(label);
  Object.entries(THEMES).forEach(([name,color])=>{
    const b=document.createElement('button');b.type='button';b.dataset.theme=name;
    b.style.setProperty('--sw',color);b.title=name;b.setAttribute('aria-label','Theme '+name);
    b.addEventListener('click',()=>applyTheme(name));box.append(b);
  });
  let saved='mono';
  try{saved=new URLSearchParams(location.search).get('theme')||localStorage.getItem('cg-theme')||'mono'}catch(e){}
  applyTheme(saved);
}

/* category tabs */
function buildTabs(){
  const tabs=document.getElementById('tabs');
  const names=['All',...CATS.filter(c=>document.querySelector(`.card[data-cat="${c}"]`))];
  function show(name){
    document.querySelectorAll('#tabs button').forEach(t=>{const on=t.dataset.cat===name;t.classList.toggle('on',on);t.setAttribute('aria-pressed',on)});
    document.querySelectorAll('.card').forEach(c=>c.hidden=!(name==='All'||c.dataset.cat===name));
    history.replaceState(null,'',location.pathname+location.search+(name==='All'?'':'#'+name));
  }
  names.forEach(name=>{
    const b=document.createElement('button');b.type='button';
    const count=name==='All'?document.querySelectorAll('.card').length:document.querySelectorAll(`.card[data-cat="${name}"]`).length;
    b.innerHTML=`${name}<i>${count}</i>`;b.dataset.cat=name;
    b.addEventListener('click',()=>show(name));tabs.appendChild(b);
  });
  const h=decodeURIComponent(location.hash.slice(1));
  show(names.includes(h)?h:'All');
}

function rng(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const R=rng(11), WEEKS=53, N=WEEKS*7;
const cnt=[];
for(let i=0;i<N;i++){
  let c=0;
  if(i>N-30){c=R()<.9?Math.floor(R()*30)+2:0}
  else if(i>N-110){if(R()<.42)c=Math.floor(R()*14)+1}
  else if(R()<.05){c=Math.floor(R()*5)+1}
  cnt.push(c);
}
const max=Math.max(...cnt);
const lvl=c=>c===0?0:Math.min(4,Math.ceil(4*c/max));
const SH=['#1b1b1e','#3a3a3f','#66666c','#a6a6ac','#ffffff'];
const weekTotals=Array.from({length:WEEKS},(_,w)=>cnt.slice(w*7,w*7+7).reduce((a,b)=>a+b,0));
const maxWeek=Math.max(...weekTotals);
const svg=(W,H,inner,extra='')=>`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" ${extra}>${inner}</svg>`;
const anims=[];
function anim(el,fn){anims.push({el,fn,on:false,n:0})}


/* 1 constellation */
(function(){
  const W=440,H=210,r=rng(3);let o='';
  for(let k=0;k<70;k++)o+=`<circle cx="${(r()*W).toFixed(1)}" cy="${(r()*H).toFixed(1)}" r="0.7" fill="#fff" fill-opacity="${(.15+r()*.3).toFixed(2)}"/>`;
  const pts=[];
  cnt.forEach((c,i)=>{if(!c)return;const w=Math.floor(i/7),d=i%7;pts.push({i,c,x:14+w/52*(W-28)+(r()-.5)*5,y:18+d/6*(H-36)+(r()-.5)*8})});
  for(let k=1;k<pts.length;k++)if(pts[k].i-pts[k-1].i<=3)o+=`<line x1="${pts[k-1].x.toFixed(1)}" y1="${pts[k-1].y.toFixed(1)}" x2="${pts[k].x.toFixed(1)}" y2="${pts[k].y.toFixed(1)}" stroke="#fff" stroke-opacity=".3"/>`;
  pts.forEach(p=>o+=`<circle class="tw" style="animation-delay:-${(r()*4).toFixed(1)}s" cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="${(1+p.c/max*3.2).toFixed(1)}" fill="#fff"/>`);
  card(1,'constellation','Active days are stars. Close days connect into constellations.',svg(W,H,o));
})();

/* 2 orbit rings */
(function(){
  const W=440,H=230,cx=W/2,cy=H/2,per=N/12;let o='';
  for(let m=0;m<12;m++)o+=`<circle cx="${cx}" cy="${cy}" r="${22+m*8.5}" fill="none" stroke="#2a2a2d"/>`;
  cnt.forEach((c,i)=>{const m=Math.min(11,Math.floor(i/per)),a=(i%per)/per*Math.PI*2-Math.PI/2,rad=22+m*8.5;
    o+=`<circle cx="${(cx+Math.cos(a)*rad).toFixed(1)}" cy="${(cy+Math.sin(a)*rad).toFixed(1)}" r="${c?1.4+lvl(c)*.5:.7}" fill="${c?SH[lvl(c)]:'#333'}"/>`});
  card(2,'orbit rings','One ring per month. Dots on the ring are the days.',svg(W,H,o));
})();

/* 3 terminal heatmap */
(function(){
  const ch=['·','░','▒','▓','█'];let t='$ cat contributions.txt\n\n';
  for(let d=0;d<7;d++){let row='';for(let w=0;w<WEEKS;w++)row+=ch[lvl(cnt[w*7+d])];t+=row+'\n'}
  t+='\nless · ░ ▒ ▓ █ more';
  card(3,'terminal heatmap','The usual grid, but as text characters like a command output.',`<pre>${t}</pre>`);
})();

/* 4 pulse line */
(function(){
  const W=440,H=180,base=130;let d='M0 '+base;
  cnt.forEach((c,i)=>{const x=i/(N-1)*W;d+=` L${x.toFixed(1)} ${c?(base-8-c/max*95).toFixed(1):base} L${(x+.8).toFixed(1)} ${base}`});
  const o=`<line x1="0" y1="${base}" x2="${W}" y2="${base}" stroke="#2a2a2d"/>
  <path d="${d}" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="1.3"/>
  <path id="pl" pathLength="100" d="${d}" fill="none" stroke="#fff" stroke-width="2.6" stroke-dasharray="7 93"/>`;
  const el=card(4,'pulse line','A heartbeat monitor. The bright segment keeps scanning along.',svg(W,H,o));
  const p=el.querySelector('#pl');let t=0;
  anim(el,()=>{t=(t+.6)%100;p.setAttribute('stroke-dashoffset',-t)});
})();

/* 5 radial bars */
(function(){
  const W=440,H=240,cx=W/2,cy=H/2,r0=40;let o='';
  cnt.forEach((c,i)=>{const a=i/N*Math.PI*2-Math.PI/2,len=3+c/max*68,
    x1=cx+Math.cos(a)*r0,y1=cy+Math.sin(a)*r0,x2=cx+Math.cos(a)*(r0+len),y2=cy+Math.sin(a)*(r0+len);
    o+=`<line x1="${x1.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x2.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="${c?SH[Math.max(2,lvl(c))]:'#26262a'}" stroke-width="1.5"/>`});
  o+=`<circle cx="${cx}" cy="${cy}" r="${r0-4}" fill="none" stroke="#2a2a2d"/><text x="${cx}" y="${cy+5}" text-anchor="middle" fill="#fff" font-size="15" font-family="monospace">365d</text>`;
  card(5,'radial bars','Every day is a spoke, taller for busier days. Starts at the top and goes clockwise.',svg(W,H,o));
})();

/* 6 tower */
(function(){
  const W=440,H=240,months=12,per=Math.floor(N/months);let o='';
  const tot=[];for(let m=0;m<months;m++)tot.push(cnt.slice(m*per,m*per+per));
  const mt=tot.map(a=>a.reduce((x,y)=>x+y,0)),mm=Math.max(...mt);
  for(let m=0;m<months;m++){
    const y=H-14-(m+1)*17,w=90+Math.sqrt(mt[m]/mm)*110,x=(W-w)/2;
    o+=`<rect x="${x.toFixed(1)}" y="${y}" width="${w.toFixed(1)}" height="15" fill="#141416" stroke="#3a3a3f"/>`;
    const act=tot[m].filter(c=>c>0).length;
    for(let k=0;k<12;k++){const wx=x+8+k*((w-16)/12);o+=`<rect x="${wx.toFixed(1)}" y="${y+4}" width="${((w-16)/12-2).toFixed(1)}" height="7" fill="${k<Math.round(act/per*12*2.2)?'#fff':'#222226'}"/>`}
  }
  o+=`<line x1="40" y1="${H-14}" x2="${W-40}" y2="${H-14}" stroke="#3a3a3f"/>`;
  card(6,'tower','One floor per month. Wider floors and more lit windows mean busier months.',svg(W,H,o));
})();

/* 7 equalizer */
(function(){
  const W=440,H=190,bw=6.4;let o='';
  weekTotals.forEach((v,i)=>o+=`<rect x="${(i*8.2+4).toFixed(1)}" y="${H-8}" width="${bw}" height="2" rx="1" fill="#fff" fill-opacity="${(.35+v/maxWeek*.65).toFixed(2)}"/>`);
  const el=card(7,'equalizer','Weekly totals as audio bars that bounce. Fitting for a volume extension.',svg(W,H,o));
  const bars=[...el.querySelectorAll('rect')];let t=0;
  anim(el,()=>{t+=.09;bars.forEach((b,i)=>{const h=Math.max(2,(weekTotals[i]/maxWeek*(H-30))*(.82+.18*Math.sin(t+i*.7)));b.setAttribute('height',h.toFixed(1));b.setAttribute('y',(H-8-h).toFixed(1))})});
})();

/* 8 snake */
(function(){
  const W=440,cell=8.2,H=7*cell+16;let o='';
  const order=[];for(let w=0;w<WEEKS;w++){for(let k=0;k<7;k++)order.push(w*7+(w%2?6-k:k))}
  cnt.forEach((c,i)=>{const w=Math.floor(i/7),d=i%7;o+=`<rect data-i="${i}" x="${(w*cell+3).toFixed(1)}" y="${(d*cell+8).toFixed(1)}" width="6.4" height="6.4" rx="1.4" fill="${SH[lvl(c)]}"/>`});
  const el=card(8,'snake','A snake eats its way across the graph, like the one you had.',svg(W,H,o));
  const rects=[];el.querySelectorAll('rect').forEach(r=>rects[+r.dataset.i]=r);
  let head=0;
  anim(el,()=>{
    head=(head+1)%(N+14);
    order.forEach((idx,pos)=>{const r=rects[idx];
      if(pos<=head&&pos>head-9)r.setAttribute('fill','#fff');
      else if(pos<head)r.setAttribute('fill','#141416');
      else r.setAttribute('fill',SH[lvl(cnt[idx])])});
  });
})();

/* 9 pac-man */
(function(){
  const W=440,cell=8.2,H=7*cell+30;let o='';
  cnt.forEach((c,i)=>{const w=Math.floor(i/7),d=i%7;o+=`<circle data-i="${i}" cx="${(w*cell+7).toFixed(1)}" cy="${(d*cell+19).toFixed(1)}" r="${c?1.5+lvl(c)*.5:.8}" fill="${c?'#fff':'#333'}"/>`});
  o+=`<path id="pac" d="" fill="#fff"/>`;
  const el=card(9,'pac-man','He eats the days one row at a time, left to right then right to left.',svg(W,H,o));
  const dots=[];el.querySelectorAll('circle').forEach(c=>dots[+c.dataset.i]=c);
  const pac=el.querySelector('#pac');
  const order=[];for(let d=0;d<7;d++){for(let k=0;k<WEEKS;k++){const w=d%2?WEEKS-1-k:k;order.push(w*7+d)}}
  let pos=0,t=0;
  anim(el,()=>{
    pos=(pos+1.4)%(N+10);t+=.35;
    const p=Math.min(Math.floor(pos),N-1),idx=order[p],w=Math.floor(idx/7),d=idx%7;
    order.forEach((ix,k)=>dots[ix].setAttribute('opacity',k<p?0:1));
    const cx=w*cell+7,cy=d*cell+19,r=6,m=.15+.45*Math.abs(Math.sin(t)),dir=(d%2)?Math.PI:0;
    const a1=dir+m,a2=dir-m;
    pac.setAttribute('d',`M${cx} ${cy} L${cx+r*Math.cos(a1)} ${cy+r*Math.sin(a1)} A${r} ${r} 0 1 ${dir?0:1} ${cx+r*Math.cos(a2)} ${cy+r*Math.sin(a2)} Z`);
  });
})();

/* 10 falling blocks */
(function(){
  const W=440,H=200,bs=6,cols=WEEKS;
  const el=card(10,'falling blocks','Blocks drop into place and stack up, one column per week.',svg(W,H,'<g id="fb"></g>'));
  const g=el.querySelector('#fb');let f=0;
  const target=weekTotals.map(v=>Math.max(0,Math.ceil(v/maxWeek*22)));
  anim(el,()=>{
    f=(f+1)%260;let o='';
    for(let i=0;i<cols;i++){
      const h=Math.max(0,Math.min(target[i],Math.floor((f-i*.8)/2.2)));
      for(let k=0;k<h;k++)o+=`<rect x="${(i*8.2+4).toFixed(1)}" y="${H-8-(k+1)*7}" width="${bs+.4}" height="${bs}" rx="1" fill="${k>h-3?'#fff':'#8e8e94'}"/>`;
    }
    g.innerHTML=o;
  });
})();

/* 11 radar sweep */
(function(){
  const W=440,H=250,cx=W/2,cy=H/2;let o='';
  for(let d=0;d<7;d++)o+=`<circle cx="${cx}" cy="${cy}" r="${22+d*14}" fill="none" stroke="#222226"/>`;
  o+=`<line x1="${cx-115}" y1="${cy}" x2="${cx+115}" y2="${cy}" stroke="#222226"/><line x1="${cx}" y1="${cy-115}" x2="${cx}" y2="${cy+115}" stroke="#222226"/>`;
  const pts=[];
  cnt.forEach((c,i)=>{if(!c)return;const w=Math.floor(i/7),d=i%7,a=w/WEEKS*Math.PI*2,r=22+d*14;
    pts.push({a,x:cx+Math.cos(a)*r,y:cy+Math.sin(a)*r,c})});
  pts.forEach((p,k)=>o+=`<circle data-k="${k}" cx="${p.x.toFixed(1)}" cy="${p.y.toFixed(1)}" r="${1.4+lvl(p.c)*.55}" fill="#fff" opacity=".15"/>`);
  o+=`<line id="sw" x1="${cx}" y1="${cy}" x2="${cx+120}" y2="${cy}" stroke="#fff" stroke-width="1.5"/>`;
  const el=card(11,'radar sweep','A scan line rotates and lights up the days it passes.',svg(W,H,o));
  const dots=[...el.querySelectorAll('circle[data-k]')],sw=el.querySelector('#sw');let th=0;
  anim(el,()=>{
    th=(th+.03)%(Math.PI*2);
    sw.setAttribute('x2',cx+Math.cos(th)*120);sw.setAttribute('y2',cy+Math.sin(th)*120);
    dots.forEach((d,k)=>{let diff=th-pts[k].a;diff=((diff%(Math.PI*2))+Math.PI*2)%(Math.PI*2);d.setAttribute('opacity',(.12+.88*Math.exp(-diff/1.1)).toFixed(2))});
  });
})();

/* 12 punch card */
(function(){
  const W=440,H=210,r=rng(5);let o='';
  const days=['Sun','Mon','Tue','Wed','Thu','Fri','Sat'];
  for(let d=0;d<7;d++){
    o+=`<text x="4" y="${24+d*26}" fill="#85858b" font-size="11" font-family="monospace">${days[d]}</text>`;
    for(let h=0;h<24;h++){
      const v=Math.max(0,.7*Math.exp(-Math.pow((h-22.5)/3.2,2))+.5*Math.exp(-Math.pow((h-14)/2.5,2))+(r()-.5)*.25);
      o+=`<circle cx="${(44+h*16.2).toFixed(1)}" cy="${20+d*26}" r="${(v*8).toFixed(1)}" fill="#fff" fill-opacity="${(.3+v*.7).toFixed(2)}"/>`;
    }
  }
  [0,6,12,18].forEach(h=>o+=`<text x="${(44+h*16.2).toFixed(1)}" y="${H-6}" fill="#85858b" font-size="10" font-family="monospace" text-anchor="middle">${String(h).padStart(2,'0')}:00</text>`);
  card(12,'punch card','When you code: weekdays down, hours across. Bigger dots are busier times.',svg(W,H,o));
})();

/* 13 streak timeline */
(function(){
  const W=440,H=150;let o='',runs=[],s=-1;
  cnt.forEach((c,i)=>{if(c>0&&s<0)s=i;if((c===0||i===N-1)&&s>=0){runs.push({s,e:i-(c===0?1:0)});s=-1}});
  o+=`<rect x="0" y="86" width="${W}" height="14" fill="#161618"/>`;
  runs.forEach(r=>{const x=r.s/N*W,w=Math.max(2,(r.e-r.s+1)/N*W);o+=`<rect x="${x.toFixed(1)}" y="86" width="${w.toFixed(1)}" height="14" fill="#fff" fill-opacity="${r.e-r.s>=5?1:.45}"/>`;
    if(r.e-r.s>=5)o+=`<text x="${(x+w/2).toFixed(1)}" y="78" fill="#fff" font-size="11" font-family="monospace" text-anchor="middle">${r.e-r.s+1}d</text>`});
  const best=Math.max(...runs.map(r=>r.e-r.s+1));
  o+=`<text x="${W/2}" y="40" fill="#fff" font-size="30" font-weight="700" font-family="monospace" text-anchor="middle">${best}d</text><text x="${W/2}" y="58" fill="#85858b" font-size="12" font-family="monospace" text-anchor="middle">longest streak</text>`;
  o+=`<text x="2" y="124" fill="#85858b" font-size="11" font-family="monospace">12 months ago</text><text x="${W-2}" y="124" fill="#85858b" font-size="11" font-family="monospace" text-anchor="end">today</text>`;
  card(13,'streak timeline','Every streak as a block along one year. Long streaks get a label.',svg(W,H,o));
})();

/* 14 word cloud */
(function(){
  const words=[['fix',34],['feat',30],['add',26],['docs',20],['test',24],['update',18],['refactor',16],['style',14],['deploy',22],['page',15],['button',13],['auth',17],['wallet',16],['chat',15],['ui',19],['merge',14],['polish',13],['init',12]];
  const sh=['#fff','#d4d4d8','#a1a1a6','#7a7a80'];
  const html='<div class="cloud">'+words.map(([w,s],i)=>`<span style="font-size:${s}px;color:${sh[i%sh.length]}">${w}</span>`).join('')+'</div>';
  card(14,'commit word cloud','The words you use most in commit messages. Words here are sample ones.',html);
})();

/* 15 repo bubbles */
(function(){
  const W=440,H=230;
  const b=[[150,118,74,'project-a',212],[268,92,46,'project-b',96],[336,152,36,'project-c',64],[234,176,28,'profile',41],[92,58,24,'repo-d',22],[372,64,20,'repo-e',14]];
  let o='';
  b.forEach(([x,y,r,n,c],i)=>o+=`<circle cx="${x}" cy="${y}" r="${r}" fill="#131316" stroke="${SH[Math.max(2,4-i)]}" stroke-width="1.4"/>
    <text x="${x}" y="${y-2}" fill="#fff" font-size="${Math.max(10,r/4.5)}" font-family="monospace" text-anchor="middle">${n}</text>
    <text x="${x}" y="${y+13}" fill="#85858b" font-size="11" font-family="monospace" text-anchor="middle">${c}</text>`);
  card(15,'repo bubbles','One bubble per repo, sized by commits. Names here are placeholders.',svg(W,H,o));
})();

/* 16 spiral galaxy */
(function(){
  const W=440,H=250,cx=W/2,cy=H/2,r=rng(8);
  let o='<defs><radialGradient id="gcore"><stop offset="0" stop-color="#fff" stop-opacity=".4"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient></defs>';
  for(let k=0;k<120;k++){const a=r()*Math.PI*2,d=Math.sqrt(r())*118;o+=`<circle cx="${(cx+Math.cos(a)*d*1.65).toFixed(1)}" cy="${(cy+Math.sin(a)*d*.95).toFixed(1)}" r=".6" fill="#fff" fill-opacity="${(.1+r()*.25).toFixed(2)}"/>`}
  o+=`<ellipse cx="${cx}" cy="${cy}" rx="46" ry="28" fill="url(#gcore)"/>`;
  cnt.forEach((c,i)=>{const t=i/N,ang=t*Math.PI*2*3+.6,rad=12+t*108,j=(r()-.5)*5;
    o+=`<circle cx="${(cx+Math.cos(ang)*(rad+j)*1.55).toFixed(1)}" cy="${(cy+Math.sin(ang)*(rad+j)*.9).toFixed(1)}" r="${c?(1+lvl(c)*.6).toFixed(1):.7}" fill="#fff" fill-opacity="${c?(.45+lvl(c)*.13).toFixed(2):.16}"/>`});
  card(16,'spiral galaxy','Your year winds out from the center along a spiral arm. Brighter stars are busier days.',svg(W,H,o));
})();

/* 17 solar system */
(function(){
  const W=440,H=250,cx=W/2,cy=H/2;
  const pl=[[30,3,.05,'#a1a1a6'],[50,5,.034,'#fff'],[72,8,.022,'#d4d4d8'],[94,4.5,.016,'#7a7a80'],[114,6.5,.011,'#a1a1a6']];
  let o=`<circle cx="${cx}" cy="${cy}" r="11" fill="#fff"/><circle cx="${cx}" cy="${cy}" r="17" fill="none" stroke="#fff" stroke-opacity=".25"/>`;
  pl.forEach(([rad,s,sp,col],i)=>{o+=`<circle cx="${cx}" cy="${cy}" r="${rad}" fill="none" stroke="#2a2a2d"/><g data-p="${i}" transform="rotate(${i*70} ${cx} ${cy})"><circle cx="${cx+rad}" cy="${cy}" r="${s}" fill="${col}"/>${i===4?`<ellipse cx="${cx+rad}" cy="${cy}" rx="${s*2}" ry="${s*.6}" fill="none" stroke="#a1a1a6" stroke-opacity=".7"/>`:''}</g>`});
  const el=card(17,'solar system','One planet per repo orbiting you. Bigger planets are repos with more commits.',svg(W,H,o));
  const gs=[...el.querySelectorAll('g[data-p]')],ang=pl.map((_,i)=>i*70);
  anim(el,()=>{gs.forEach((g,i)=>{ang[i]=(ang[i]+pl[i][2]*40)%360;g.setAttribute('transform',`rotate(${ang[i].toFixed(1)} ${cx} ${cy})`)})});
})();

/* 18 moon phases */
(function(){
  const W=440,H=140,rad=6,sp=16.4;let o='';
  for(let c=0;c<26;c++)for(let d=0;d<7;d++){
    const i=(WEEKS-26+c)*7+d,f=lvl(cnt[i])/4,x=14+c*sp,y=14+d*sp;
    o+=`<circle cx="${x}" cy="${y}" r="${rad}" fill="#161618" stroke="#26262a"/>`;
    if(f>0){
      if(f>=1)o+=`<circle cx="${x}" cy="${y}" r="${rad}" fill="#fff"/>`;
      else{const rx=rad*Math.abs(1-2*f);o+=`<path d="M${x} ${y-rad}A${rad} ${rad} 0 0 1 ${x} ${y+rad}A${rx.toFixed(2)} ${rad} 0 0 ${f<.5?1:0} ${x} ${y-rad}Z" fill="#fff"/>`}
    }
  }
  card(18,'moon phases','Each day is a moon: new moon for no activity, full moon for your busiest days. Shows the last 26 weeks.',svg(W,H,o));
})();

/* 19 meteor shower */
(function(){
  const W=440,H=230,r=rng(21),ca=Math.cos(.5),sa=Math.sin(.5);let o='';
  for(let k=0;k<80;k++)o+=`<circle cx="${(r()*W).toFixed(1)}" cy="${(r()*H).toFixed(1)}" r=".6" fill="#fff" fill-opacity="${(.15+r()*.3).toFixed(2)}"/>`;
  const ms=[];
  cnt.forEach((c,i)=>{if(!c)return;const w=Math.floor(i/7),x=10+w/52*(W-90),y=10+r()*(H-80),len=14+c/max*48;
    o+=`<line x1="${x.toFixed(1)}" y1="${y.toFixed(1)}" x2="${(x+len*ca).toFixed(1)}" y2="${(y+len*sa).toFixed(1)}" stroke="#fff" stroke-opacity=".12"/>`;
    o+=`<line data-m="${ms.length}" pathLength="100" x1="${x.toFixed(1)}" y1="${y.toFixed(1)}" x2="${(x+len*ca).toFixed(1)}" y2="${(y+len*sa).toFixed(1)}" stroke="#fff" stroke-width="${(1+lvl(c)*.4).toFixed(1)}" stroke-linecap="round" stroke-dasharray="14 120" stroke-opacity="${(.5+lvl(c)*.12).toFixed(2)}"/>`;
    ms.push(r())});
  const el=card(19,'meteor shower','Every active day is a streak across the sky. Busier days are longer and brighter.',svg(W,H,o));
  const ls=[...el.querySelectorAll('line[data-m]')];let t=0;
  anim(el,()=>{t+=.012;ls.forEach((l,k)=>{const p=((t+ms[k])%1);l.setAttribute('stroke-dashoffset',(14-p*134).toFixed(1))})});
})();

/* 20 git graph */
(function(){
  const W=440,H=190,my=95,r=rng(33);let o='',nodes='';
  const X=w=>12+w/52*(W-24);
  const act=[];weekTotals.forEach((v,w)=>{if(v>0)act.push(w)});
  o+=`<line x1="${X(act[0])}" y1="${my}" x2="${X(act[act.length-1])}" y2="${my}" stroke="#a1a1a6" stroke-width="1.6"/>`;
  let k=0;
  while(k<act.length-6){
    if(r()<.38){const len=2+Math.floor(r()*3),up=r()<.5,by=my+(up?-34:34)*(.6+r()*.6),x0=X(act[k]),x1=X(act[k+len+1]);
      o+=`<path d="M${x0} ${my} C${x0+8} ${my},${x0+6} ${by},${x0+16} ${by} L${x1-16} ${by} C${x1-6} ${by},${x1-8} ${my},${x1} ${my}" fill="none" stroke="#7a7a80" stroke-width="1.4"/>`;
      for(let j=1;j<=len;j++)nodes+=`<circle cx="${(x0+16+(x1-x0-32)*j/(len+1)).toFixed(1)}" cy="${by.toFixed(1)}" r="3" fill="#0b0b0c" stroke="#d4d4d8" stroke-width="1.4"/>`;
      k+=len+2;
    }else k++;
  }
  act.forEach(w=>nodes+=`<circle cx="${X(w).toFixed(1)}" cy="${my}" r="3.4" fill="#fff"/>`);
  const hex=()=>Math.floor(r()*0xfffffff).toString(16).padStart(7,'0');
  const lx=X(act[act.length-1]);
  nodes+=`<text x="${lx-6}" y="${my+22}" fill="#85858b" font-size="10" font-family="monospace" text-anchor="end">${hex()}</text><text x="${lx-6}" y="${my-14}" fill="#fff" font-size="11" font-family="monospace" text-anchor="end">HEAD → main</text><text x="${X(act[0])}" y="${my+22}" fill="#85858b" font-size="10" font-family="monospace">${hex()}</text>`;
  card(20,'git graph','Looks like git log --graph: a main line with branches that fork and merge back. Hashes are fake.',svg(W,H,o+nodes));
})();

/* 21 matrix rain */
(function(){
  const W=440,H=230;
  const el=card(21,'matrix rain','Falling characters. Weeks with more commits rain brighter and more often.',`<canvas width="${W}" height="${H}" style="background:#08080a;max-width:100%"></canvas>`);
  const cv=el.querySelector('canvas'),g=cv.getContext('2d'),cols=WEEKS,cw=W/cols,drops=Array.from({length:cols},()=>Math.random()*-20);
  const chars='01<>/{}[]$#=+*';g.font='10px monospace';
  anim(el,()=>{
    g.fillStyle='rgba(8,8,10,.16)';g.fillRect(0,0,W,H);
    for(let i=0;i<cols;i++){
      const a=.15+weekTotals[i]/maxWeek*.85;
      if(drops[i]<0){drops[i]+=Math.random()*a*1.5;continue}
      g.fillStyle=`rgba(${ACC[0]},${ACC[1]},${ACC[2]},${(.25+a*.7).toFixed(2)})`;
      g.fillText(chars[Math.floor(Math.random()*chars.length)],i*cw,drops[i]*11);
      if(drops[i]*11>H&&Math.random()>.94-a*.05)drops[i]=-Math.random()*12;else drops[i]+=.6+a*.7;
    }
  });
})();

/* 22 hex dump */
(function(){
  let t='$ xxd contributions.bin\n\n';
  for(let row=0;row<24;row++){
    let hex='',asc='';
    for(let k=0;k<16;k++){const i=row*16+k;if(i>=N){hex+='   ';continue}
      const b=Math.min(255,cnt[i]*7);hex+=b.toString(16).padStart(2,'0')+(k%2?' ':'');
      asc+=b>0?String.fromCharCode(33+Math.min(90,Math.floor(b/3))):'.'}
    t+=(row*16).toString(16).padStart(8,'0')+': '+hex.padEnd(40)+' '+asc+'\n';
  }
  card(22,'hex dump','Each day is one byte. Busy days show as larger hex values, like opening a binary file.',`<pre style="font-size:10px">${t}</pre>`);
})();

/* 23 htop monitor */
(function(){
  const names=['Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov'],per=Math.floor(N/12);
  const tot=names.map((_,m)=>cnt.slice(m*per,m*per+per).reduce((a,b)=>a+b,0)),mx=Math.max(...tot);
  let t='$ htop --contributions\n\n';
  names.forEach((n,m)=>{const f=Math.round(tot[m]/mx*24);t+=`${n} [${'|'.repeat(f)}${' '.repeat(24-f)}] ${String(Math.round(tot[m]/mx*100)).padStart(3)}%  ${String(tot[m]).padStart(4)}\n`});
  t+=`\nTasks: ${cnt.filter(c=>c).length} active days, ${N} total\nUptime: 365 days`;
  card(23,'htop monitor','Months as system-monitor bars with percentages. Shows how busy each month was.',`<pre style="font-size:12px">${t}</pre>`);
})();

/* 24 ridgeline mountains */
(function(){
  const W=440,H=270,per=Math.floor(N/12),r=rng(14);let o='';
  for(let m=0;m<12;m++){
    const base=34+m*19,pts=[];
    for(let k=0;k<per;k++){const c=cnt[m*per+k]||0;pts.push([14+k/(per-1)*(W-28),base-(c?c/max*38+r()*3:r()*1.4)])}
    const d='M'+pts.map(p=>p[0].toFixed(1)+' '+p[1].toFixed(1)).join(' L');
    o+=`<path d="${d} L${W-14} ${base+30} L14 ${base+30} Z" fill="#08080a"/><path d="${d}" fill="none" stroke="#fff" stroke-width="1.1" stroke-opacity="${(.45+m/12*.5).toFixed(2)}"/>`;
  }
  card(24,'ridgeline mountains','One jagged line per month stacked on black, like the Unknown Pleasures album cover. Peaks are busy days.',svg(W,H,o));
})();

/* 25 topographic map */
(function(){
  const W=440,H=210,cs=5,gw=Math.floor(W/cs),gh=Math.floor(H/cs),sg=17;
  const pts=[];cnt.forEach((c,i)=>{if(c)pts.push([14+Math.floor(i/7)/52*(W-28),16+(i%7)/6*(H-32),c])});
  const F=[];let fm=0;
  for(let j=0;j<=gh;j++){F[j]=[];for(let i=0;i<=gw;i++){let v=0;const x=i*cs,y=j*cs;
    for(const p of pts){const dx=x-p[0],dy=y-p[1];if(dx*dx+dy*dy<(sg*3)*(sg*3))v+=p[2]*Math.exp(-(dx*dx+dy*dy)/(2*sg*sg))}
    F[j][i]=v;if(v>fm)fm=v}}
  const T={1:[[3,2]],2:[[2,1]],3:[[3,1]],4:[[0,1]],5:[[0,3],[1,2]],6:[[0,2]],7:[[0,3]],8:[[0,3]],9:[[0,2]],10:[[0,1],[2,3]],11:[[0,1]],12:[[3,1]],13:[[2,1]],14:[[3,2]]};
  let o='';
  [.05,.13,.25,.4,.6,.82].forEach((lv,li)=>{
    const th=lv*fm;let d='';
    for(let j=0;j<gh;j++)for(let i=0;i<gw;i++){
      const tl=F[j][i],tr=F[j][i+1],br=F[j+1][i+1],bl=F[j+1][i];
      const idx=(tl>th?8:0)|(tr>th?4:0)|(br>th?2:0)|(bl>th?1:0);
      if(!T[idx])continue;
      const x=i*cs,y=j*cs,lerp=(a,b)=>(th-a)/(b-a);
      const e=[[x+cs*lerp(tl,tr),y],[x+cs,y+cs*lerp(tr,br)],[x+cs*lerp(bl,br),y+cs],[x,y+cs*lerp(tl,bl)]];
      T[idx].forEach(([a,b])=>d+=`M${e[a][0].toFixed(1)} ${e[a][1].toFixed(1)}L${e[b][0].toFixed(1)} ${e[b][1].toFixed(1)}`);
    }
    o+=`<path d="${d}" fill="none" stroke="#fff" stroke-width="${li>3?1.3:.8}" stroke-opacity="${(.25+li*.13).toFixed(2)}" stroke-linecap="round"/>`;
  });
  card(25,'topographic map','Contour lines rise around your busiest weeks, like a hiking map. Recent weeks form the peak.',svg(W,H,o));
})();

/* 26 DNA helix */
(function(){
  const W=440,H=210,cy=H/2,A=58,k=Math.PI*2*3/W;
  const el=card(26,'DNA helix','Two twisting strands with a rung for every active day. It slowly rotates.',svg(W,H,'<g id="dna"></g>'));
  const g=el.querySelector('#dna');let ph=0;
  const act=[];cnt.forEach((c,i)=>{if(c)act.push([i,c])});
  anim(el,()=>{
    ph+=.05;let a='',b='',rungs='';
    for(let x=0;x<=W;x+=4){const y1=cy+A*Math.sin(k*x+ph),y2=cy+A*Math.sin(k*x+ph+Math.PI);a+=(x?'L':'M')+x+' '+y1.toFixed(1);b+=(x?'L':'M')+x+' '+y2.toFixed(1)}
    act.forEach(([i,c])=>{const x=i/N*W,y1=cy+A*Math.sin(k*x+ph),y2=cy+A*Math.sin(k*x+ph+Math.PI);
      rungs+=`<line x1="${x.toFixed(1)}" y1="${y1.toFixed(1)}" x2="${x.toFixed(1)}" y2="${y2.toFixed(1)}" stroke="#fff" stroke-width="${(.6+lvl(c)*.35).toFixed(2)}" stroke-opacity="${(.25+lvl(c)*.15).toFixed(2)}"/>`});
    g.innerHTML=`<path d="${a}" fill="none" stroke="#fff" stroke-width="1.8"/><path d="${b}" fill="none" stroke="#a1a1a6" stroke-width="1.8"/>${rungs}`;
  });
})();

/* 27 barcode */
(function(){
  const W=440,H=170,bx=20,bw=W-40;let o='';
  cnt.forEach((c,i)=>{const x=bx+i/N*bw,w=c?.7+lvl(c)*.4:.25;o+=`<rect x="${x.toFixed(2)}" y="22" width="${w.toFixed(2)}" height="92" fill="#fff" fill-opacity="${c?1:.35}"/>`});
  o+=`<text x="${W/2}" y="136" fill="#fff" font-size="13" letter-spacing="6" font-family="monospace" text-anchor="middle">INFERISM  2026  ${String(cnt.reduce((a,b)=>a+b,0)).padStart(5,'0')}</text><text x="${W/2}" y="156" fill="#85858b" font-size="10" font-family="monospace" text-anchor="middle">one bar per day, thicker when you were busier</text>`;
  card(27,'barcode','Your year as a product barcode. Thick bars are active days.',svg(W,H,o));
})();

/* styles that only exist as generators, so there is no live demo code for them */
card(101,'vinyl record','A record with one ring of grooves per month. Every active day is a blip along its ring.','');
card(102,'piano roll','Weekdays are piano keys, weeks run left to right, and every active day is a note. Longer notes are busier days.','');
card(103,'tree','A tree grows a branch for every active week. Longer branches are busier weeks, and each leaf is an active day.','');
card(104,'ocean waves','One wave per month, stacked in the sea. Taller swells are busier days.','');
card(105,'space invaders','Every active day is an invader. Busier days are bigger, brighter invaders.','');
card(106,'RPG status','A character sheet built from your year: level, XP and stat bars like HP and mana.','');
card(107,'3D skyline','A 3D city floating in space. One building per day, taller and brighter when you were busier.','');
card(108,'terrain mesh','A wireframe landscape. Weeks run left to right, weekdays go into the distance, and height is how busy you were.','');

buildTabs();
buildThemes();
initViewer();

/* animation loop (~25 fps), only for cards that are on screen */
const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
const io=new IntersectionObserver(es=>es.forEach(e=>anims.forEach(a=>{if(a.el===e.target)a.on=e.isIntersecting})),{rootMargin:'120px'});
anims.forEach(a=>io.observe(a.el));
let last=0;
function loop(ts){
  if(ts-last>40){
    last=ts;
    anims.forEach(a=>{if(!a.on||a.el.hidden||(reduce&&a.n>40))return;a.n++;a.fn()});
  }
  requestAnimationFrame(loop);
}
requestAnimationFrame(loop);
