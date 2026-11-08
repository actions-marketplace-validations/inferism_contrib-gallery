/* contrib-gallery: demos run on made-up sample data, nothing is fetched. */
const CATS=['Space','Games','3D','Dev','Music','Minimal','Nature'];
/* the styles that have a generator come from samples/styles.json, built from generator/styles/catalog.py */
const CATALOG=await (await fetch('samples/styles.json')).json();
const READY=new Map(CATALOG.map(c=>[c.id,c.h]));
/* the few previews that have no generator, and why */
const META={
  12:{id:'punch-card',cat:'Minimal',why:'Needs the hour of each commit, which the contribution graph does not include.'},
  14:{id:'word-cloud',cat:'Minimal',why:'Needs commit messages, which are not part of the contribution data and could expose private work.'},
  15:{id:'repo-bubbles',cat:'Minimal',why:'Needs repository names, which could expose private repos on a public profile.'}
};
const REPO='inferism/contrib-gallery';
const THEMES={mono:'#ffffff',ice:'#7dd3fc',ember:'#fb923c',matrix:'#4ade80',sakura:'#f9a8d4',violet:'#c4b5fd'};
let theme='mono',ACC=[255,255,255],current=null;
const sampleUrl=id=>`samples/${theme}/${id}.svg`;

function workflowFor(id,th){
  /* the chosen theme is set; the other options are left as commented hints */
  const line=['\n          '+(th&&th!=='mono'?`theme: ${th}`:'# theme: ice'),
    '\n          # mode: dark          # default is auto, which follows light or dark GitHub',
    '\n          # frame: terminal     # default is none; also simple or brackets',
    '\n          # header: terminal    # default is none; also title',
    '\n          # details: show       # adds stars, decorations and a stats line',
    '\n          # background: "#0a0a0a"   # match a custom page color'].join('');
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

function card(n,title,note,html,entry){
  const m=entry||META[n]||{id:'style-'+n,cat:'Minimal'},ready=READY.has(m.id);
  if(ready&&!entry){  /* a demo for a style that now has a generator: keep it off the page */
    const gone=document.createElement('article');gone.innerHTML='<div class="stage">'+html+'</div>';return gone;
  }
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
    const q=document.createElement('p');q.className='soon';q.textContent='Preview only. '+(m.why||'The generator for this style is coming soon.');el.append(q);
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
  const p=document.createElement('p');p.className='note';p.textContent=current.note+' Shown on a dark page. By default your chart follows GitHub’s light or dark setting, with no frame, title or extras.';
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
const SH=['#1b1b1e','#3a3a3f','#66666c','#a6a6ac','#ffffff'];
const svg=(W,H,inner,extra='')=>`<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" ${extra}>${inner}</svg>`;

/* preview-only demos on made-up data */
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

/* every style that has a generator */
CATALOG.forEach(c=>card(0,c.title,c.note,'',{id:c.id,cat:c.cat}));

buildTabs();
buildThemes();
initViewer();
