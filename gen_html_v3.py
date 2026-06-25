#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from collections import Counter

with open('/sessions/clever-tender-cerf/mnt/设计学习/矛盾对立视角案例库/cases_all_v2.json', encoding='utf-8') as f:
    cases = json.load(f)
for c in cases:
    c.setdefault('image', '')
    c.setdefault('link', '')
    c.setdefault('importance', 0)

DATA = json.dumps(cases, ensure_ascii=False, separators=(',',':')).replace('</script>', '<\\/script>')

MODULES = [
    ('一、本体框架论', ['1.1 本体与客体','1.2 二元与多元','1.3 联系与发展','1.4 具象与抽象','1.5 物质与非物质']),
    ('二、时间框架论', ['2.1 传统与当代','2.2 继承与创新']),
    ('三、社会框架论', ['3.1 精英与大众','3.2 服务于谁']),
    ('四、生产框架论', ['4.1 形式与功能','4.2 艺术与科学','4.3 媒介、材料与内容']),
    ('五、空间框架论', ['5.1 本土与异域','5.2 全球化与在地性']),
]
# 正式书目（新增整本书时追加到此列表，单篇材料不在此列）
BOOKS = ['《中国工艺美术史新编》','《中国美术简史》','《外国工艺美术史》','《外国美术简史》','《世界现代设计史》','《艺术概论》','《艺术设计概论》']
MODS_JSON  = json.dumps(MODULES, ensure_ascii=False)
BOOKS_JSON = json.dumps(BOOKS,   ensure_ascii=False)
ALL_NODES  = [n for _,nodes in MODULES for n in nodes]
NODES_JSON = json.dumps(ALL_NODES, ensure_ascii=False)
TOTAL = len(cases)

HTML = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>矛盾对立视角 · 案例库</title>
<style>
:root{{
  --sw:256px; --th:54px;
  /* Brand palette */
  --black:#111111; --beige:#c4b5a7; --purple:#9b7ed4; --cream:#f5efe7;
  /* Layout */
  --bg:#fdfaf6; --sb:#ffffff; --bd:transparent;
  /* Primary / accent */
  --p:#191919; --pl:#ede8f6; --acc:#9b7ed4;
  /* 国内 — warm beige */
  --dom:#8c7f75; --doml:#f0e8df; --domdk:#5c4e42;
  /* 国外 — lavender */
  --for:#9b7ed4; --forl:#ede8f6; --fordk:#7a5eb8;
  /* Misc */
  --muted:#7a6b5e; --text:#191919; --star:#9b7ed4;
  --amber:#fdf5e8; --amberbd:transparent; --ambertext:#6b4820;
  --r:10px; --sh:0 1px 3px rgba(0,0,0,.06),0 1px 2px rgba(0,0,0,.04);
  --shm:0 4px 12px rgba(0,0,0,.08);
}}
*{{box-sizing:border-box;margin:0;padding:0}}
body{{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","PingFang SC",Arial,sans-serif;
  background:var(--bg);color:var(--text);height:100vh;overflow:hidden;font-size:14px}}
button{{cursor:pointer;border:none;background:none;font-family:inherit;font-size:inherit}}
a{{color:var(--acc);text-decoration:none}}
a:hover{{text-decoration:underline}}

/* ── Layout ── */
.layout{{display:flex;height:100vh;overflow:hidden}}
.overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.45);z-index:40}}
.overlay.show{{display:block}}

/* ── Sidebar ── */
.sidebar{{
  width:var(--sw);min-width:var(--sw);height:100vh;
  background:var(--sb);border-right:1px solid var(--bd);
  display:flex;flex-direction:column;z-index:50;
  transition:transform .22s ease;
}}
.sb-head{{padding:16px 14px 12px;border-bottom:1px solid var(--bd)}}
.brand{{font-size:20px;font-weight:700;color:var(--p);line-height:1.2;margin-bottom:12px;letter-spacing:-.3px}}
.vtabs{{display:flex;background:#fdfaf6;border-radius:8px;padding:3px;gap:2px}}
.vtab{{
  flex:1;padding:6px 4px;font-size:12px;font-weight:600;border-radius:6px;
  color:var(--muted);transition:all .15s;
}}
.vtab.active{{background:#fff;color:var(--p);box-shadow:0 1px 3px rgba(0,0,0,.1)}}

.sb-nav{{flex:1;overflow-y:auto;padding:8px 0}}
.sb-nav::-webkit-scrollbar{{width:3px}}
.sb-nav::-webkit-scrollbar-thumb{{background:#fff;border-radius:2px}}

.nav-module{{
  padding:10px 14px 3px;font-size:10px;font-weight:700;
  color:var(--muted);letter-spacing:.8px;text-transform:uppercase;
}}
.nav-item{{
  display:flex;align-items:center;justify-content:space-between;
  margin:1px 8px;padding:6px 10px;font-size:13px;color:#191919;cursor:pointer;
  border-radius:7px;transition:background .1s,color .1s;
  user-select:none;
}}
.nav-item:hover{{background:#fdfaf6;color:var(--p)}}
.nav-item.active{{
  background:#ede8f6;color:var(--acc);font-weight:600;
}}
.nav-item.all{{font-weight:700;color:var(--p)}}
.nav-indent{{padding-left:20px}}
.nav-badge{{
  font-size:11px;color:var(--muted);background:#fdfaf6;
  padding:1px 6px;border-radius:10px;flex-shrink:0;
}}
.nav-item.active .nav-badge{{background:#ede8f6;color:var(--acc)}}

.sb-foot{{padding:12px 14px;border-top:1px solid var(--bd);flex-shrink:0}}
.sb-stats{{font-size:11px;color:var(--muted);text-align:center;margin-bottom:8px}}
.export-btn{{
  width:100%;padding:9px;background:var(--p);color:#fff;
  border-radius:8px;font-size:13px;font-weight:600;transition:background .15s;
}}
.export-btn:hover{{background:var(--acc)}}

/* ── Main ── */
.main{{flex:1;display:flex;flex-direction:column;overflow:hidden;min-width:0}}

/* ── Topbar ── */
.topbar{{
  display:flex;align-items:center;gap:8px;flex-shrink:0;
  padding:9px 14px;background:var(--sb);border-bottom:1px solid var(--bd);
}}
.hamburger{{
  display:none;width:34px;height:34px;border-radius:7px;
  flex-direction:column;justify-content:center;gap:4px;padding:6px;flex-shrink:0;
}}
.hamburger span{{height:2px;background:var(--p);border-radius:2px}}
.hamburger:hover{{background:#fdfaf6}}
.search-wrap{{
  flex:1;min-width:0;display:flex;align-items:center;gap:7px;
  background:#fdfaf6;border:1px solid #f6f1ec;border-radius:8px;
  padding:0 10px;transition:border-color .15s,background .15s;
}}
.search-wrap:focus-within{{border-color:var(--acc);background:#fff}}
.search-icon{{color:var(--muted);font-size:13px;flex-shrink:0}}
#searchInput{{
  flex:1;border:none;background:none;outline:none;padding:7px 0;
  font-size:13px;color:var(--text);min-width:0;
}}
#searchInput::placeholder{{color:var(--muted)}}
.tb-right{{display:flex;align-items:center;gap:6px;flex-shrink:0}}
.sort-select{{
  padding:6px 8px;border:1px solid #f6f1ec;border-radius:7px;
  font-size:12px;font-family:inherit;background:#fdfaf6;color:var(--text);
  cursor:pointer;outline:none;transition:border-color .15s;
}}
.sort-select:focus{{border-color:var(--acc)}}
.filter-chip{{
  padding:5px 9px;font-size:12px;font-weight:500;
  border:1px solid #f6f1ec;border-radius:7px;
  color:var(--muted);background:#fdfaf6;
  transition:all .15s;white-space:nowrap;
}}
.filter-chip:hover{{border-color:var(--acc);color:var(--acc);background:#fdf5e8}}
.filter-chip.on{{background:#ede8f6;color:#9b7ed4;border-color:transparent}}

/* ── Stats bar ── */
.statsbar{{
  padding:6px 14px;font-size:12px;color:var(--muted);
  border-bottom:1px solid var(--bd);background:var(--sb);flex-shrink:0;
}}

/* ── Cards area ── */
.cards-area{{flex:1;overflow-y:auto;padding:14px}}
.cards-area::-webkit-scrollbar{{width:5px}}
.cards-area::-webkit-scrollbar-thumb{{background:#e2d8cf;border-radius:3px}}
.grid{{display:grid;grid-template-columns:1fr;gap:12px}}
@media(min-width:1000px){{.grid{{grid-template-columns:1fr 1fr}}}}
.empty{{
  grid-column:1/-1;text-align:center;padding:64px 20px;
  color:var(--muted);font-size:15px;
}}

/* ── Card ── */
.card{{
  background:#fff;border-radius:var(--r);border:1px solid #f6f1ec;
  padding:15px;position:relative;
  display:flex;flex-direction:column;gap:9px;
}}

/* Edit button — hidden until hover/longpress */
.edit-btn{{
  position:absolute;top:10px;right:10px;
  padding:3px 9px;font-size:11px;font-weight:600;
  background:#fff;border:1px solid #f6f1ec;border-radius:6px;
  color:var(--muted);opacity:0;transition:opacity .15s,background .15s,color .15s;
  z-index:2;
}}
.edit-btn:hover{{background:var(--acc);color:#fff;border-color:var(--acc)}}
@media(hover:hover){{.card:hover .edit-btn{{opacity:1}}}}
.card.lp .edit-btn{{opacity:1}}

/* Card inner */
.c-title-row{{display:flex;align-items:flex-start;gap:8px;padding-right:68px}}
.c-title{{font-size:15px;font-weight:700;color:var(--p);line-height:1.4;flex:1;min-width:0}}
.c-stars{{display:flex;gap:1px;flex-shrink:0;margin-top:3px}}
.c-stars .s{{font-size:14px;color:#d4c8be;display:inline-block;position:relative}}
.c-stars .s.full{{color:var(--star)}}
.c-stars .s.half{{color:#d4c8be}}
.c-stars .s.half::after{{
  content:"★";color:var(--star);position:absolute;
  left:0;top:0;width:50%;overflow:hidden;display:inline-block;
}}

.quote{{
  background:#fefaf7;border-radius:6px;padding:8px 10px;
  font-size:12px;color:#7a6b5e;line-height:1.7;
}}
.q-text{{display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.q-text.open{{display:block}}
.q-toggle{{font-size:11px;color:var(--acc);cursor:pointer;margin-top:3px;display:inline-block}}

.analysis{{font-size:13px;color:#191919;line-height:1.75}}
.note{{
  background:var(--amber);border-radius:7px;
  padding:9px 11px;font-size:12px;color:var(--ambertext);line-height:1.65;
}}
.note-lbl{{font-size:10px;font-weight:700;color:#6b4820;margin-bottom:4px;letter-spacing:.3px}}
.card-img{{width:100%;border-radius:6px;max-height:220px;object-fit:cover}}

.link-sep{{border:none;border-top:1px solid #e8e0d8}}
.link-row{{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--muted)}}

/* Card footer: tags left, meta right */
.c-foot{{display:flex;align-items:flex-end;justify-content:space-between;gap:10px;flex-wrap:wrap}}
.tags{{display:flex;flex-wrap:wrap;gap:4px;flex:1;min-width:0}}
.tag{{
  display:inline-block;padding:2px 7px;border-radius:4px;
  font-size:11px;font-weight:500;background:#fdfaf6;
  color:#191919;border:1px solid #f6f1ec;cursor:pointer;
}}
.no-tag{{font-size:11px;color:#b0a49c;font-style:italic}}
.tag.cat-dom{{background:var(--dom);color:#fff;border-color:var(--dom)}}
.tag.cat-for{{background:var(--dom);color:#fff;border-color:var(--dom)}}
.tag.era-tag{{background:var(--dom);color:#fff;border-color:var(--dom)}}
.c-chapter{{font-size:10px;color:#b0a49c}}
.c-meta{{
  font-size:11px;color:var(--muted);text-align:right;
  flex-shrink:0;white-space:nowrap;
}}
.c-cat{{
  display:inline-block;padding:1px 5px;border-radius:3px;
  font-size:10px;font-weight:700;margin-left:2px;
}}
.c-cat.dom{{background:var(--doml);color:var(--domdk)}}
.c-cat.for{{background:var(--forl);color:var(--fordk)}}

/* ── Modal ── */
.mbd{{display:none;position:fixed;inset:0;background:rgba(0,0,0,.5);z-index:100}}
.mbd.show{{display:block}}
.mbox{{
  display:none;position:fixed;top:50%;left:50%;transform:translate(-50%,-50%);
  width:min(600px,95vw);max-height:90vh;background:#fff;border-radius:12px;
  box-shadow:0 20px 60px rgba(0,0,0,.2);z-index:101;
  flex-direction:column;overflow:hidden;
}}
.mbox.show{{display:flex}}
.mhead{{
  display:flex;align-items:center;justify-content:space-between;
  padding:14px 18px;border-bottom:1px solid var(--bd);flex-shrink:0;
}}
.mhead h3{{font-size:15px;font-weight:700;color:var(--p)}}
.mclose{{
  width:28px;height:28px;border-radius:6px;font-size:16px;
  color:var(--muted);display:flex;align-items:center;justify-content:center;
}}
.mclose:hover{{background:#fdfaf6}}
.mbody{{flex:1;overflow-y:auto;padding:18px}}
.mbody::-webkit-scrollbar{{width:4px}}
.mbody::-webkit-scrollbar-thumb{{background:#d4c8be}}
.mfoot{{
  display:flex;gap:8px;justify-content:flex-end;
  padding:12px 18px;border-top:1px solid var(--bd);flex-shrink:0;
}}
.fg{{margin-bottom:14px}}
.fl{{display:block;font-size:12px;font-weight:600;color:#191919;margin-bottom:5px}}
.fl .opt{{color:var(--muted);font-weight:400;margin-left:3px}}
.fta,.fin{{
  width:100%;padding:7px 9px;border:1px solid #f6f1ec;border-radius:7px;
  font-size:13px;font-family:inherit;outline:none;transition:border-color .15s;
}}
.fta{{resize:vertical;min-height:72px}}
.fta:focus,.fin:focus{{border-color:var(--acc)}}
/* Tag editor */
.tag-editor{{
  display:flex;flex-wrap:wrap;align-items:center;gap:5px;
  padding:6px 8px;border:1px solid #f6f1ec;border-radius:7px;
  background:#fff;min-height:38px;cursor:text;transition:border-color .15s;
}}
.tag-editor:focus-within{{border-color:var(--acc)}}
.te-chip{{
  display:inline-flex;align-items:center;gap:3px;
  padding:2px 7px;border-radius:4px;font-size:12px;
  background:#ede8f6;color:var(--acc);border:1px solid #d8ceef;
}}
.te-rm{{
  font-size:11px;color:#c4b5e8;padding:0 1px;line-height:1;
  border-radius:2px;transition:color .1s;
}}
.te-rm:hover{{color:#ef4444}}
.te-in{{
  border:none;outline:none;font-size:13px;font-family:inherit;
  flex:1;min-width:100px;background:transparent;padding:2px 4px;color:var(--text);
}}
.img-area{{
  border:2px dashed #f6f1ec;border-radius:8px;padding:20px;
  text-align:center;cursor:pointer;color:var(--muted);font-size:13px;
  transition:border-color .15s;
}}
.img-area:hover{{border-color:var(--acc);color:var(--acc)}}
.img-wrap{{position:relative;display:inline-block}}
.img-preview{{max-width:100%;max-height:130px;border-radius:6px;display:block}}
.img-rm{{
  position:absolute;top:-7px;right:-7px;width:20px;height:20px;
  border-radius:50%;background:#dc2626;color:#fff;font-size:11px;
  display:flex;align-items:center;justify-content:center;cursor:pointer;
}}
/* Star input */
.sinput{{display:flex;align-items:center;gap:3px}}
.spos{{font-size:22px;cursor:pointer;user-select:none;line-height:1;display:inline-block}}
.spos:hover{{transform:scale(1.15)}}
.spos .si{{color:#d4c8be;transition:color .1s;display:inline-block;position:relative}}
.spos .si.lit{{color:var(--star)}}
.spos .si.half-lit{{color:#d4c8be}}
.spos .si.half-lit::after{{
  content:"★";color:var(--star);position:absolute;
  left:0;top:0;width:50%;overflow:hidden;display:inline-block;
}}
.sval{{font-size:12px;color:var(--muted);margin-left:8px}}
.bsave{{
  padding:8px 20px;background:var(--p);color:#fff;border-radius:8px;
  font-size:13px;font-weight:600;transition:background .15s;
}}
.bsave:hover{{background:var(--acc)}}
.bcancel{{
  padding:8px 15px;background:#fdfaf6;color:#191919;
  border-radius:8px;font-size:13px;font-weight:600;
}}
.bcancel:hover{{background:#f0ebe4}}
/* Mobile */
@media(max-width:767px){{
  .hamburger{{display:flex}}
  .sidebar{{position:fixed;left:0;top:0;bottom:0;transform:translateX(-100%)}}
  .sidebar.open{{transform:translateX(0)}}
  .sort-select .long{{display:none}}
  .cards-area{{padding:10px}}
}}
@media(max-width:500px){{
  .filter-chip span{{display:none}}
  .tb-right{{gap:4px}}
}}
</style>
</head>
<body>
<div class="overlay" id="overlay" onclick="closeSidebar()"></div>
<div class="layout">

<aside class="sidebar" id="sidebar">
  <div class="sb-head">
    <div class="brand">Art Cases</div>
    <div class="vtabs">
      <button class="vtab active" id="tbooks" onclick="switchTab('books')">学科汇总</button>
      <button class="vtab"        id="tnodes" onclick="switchTab('nodes')">主题案例</button>
    </div>
  </div>
  <nav class="sb-nav" id="sbNav"></nav>
  <div class="sb-foot">
    <div class="sb-stats" id="sbStats">{TOTAL} 个案例</div>
    <button class="export-btn" onclick="exportJSON()">↓ 导出 JSON</button>
  </div>
</aside>

<div class="main">
  <div class="topbar">
    <button class="hamburger" id="hbg" onclick="toggleSidebar()">
      <span></span><span></span><span></span>
    </button>
    <div class="search-wrap">
      <span class="search-icon">⌕</span>
      <input type="search" id="searchInput" placeholder="搜索案例名称、作者、年代…" oninput="applyAll()">
    </div>
    <div class="tb-right">
      <select class="sort-select" id="sortSel" onchange="applyAll()">
        <option value="year-asc">↑ 时间从远到近</option>
        <option value="year-desc">↓ 时间从近到远</option>
        <option value="importance">★ 重要性从高到低</option>
      </select>
      <button class="filter-chip" data-f="hasImage" onclick="toggleChip(this)">🖼 <span>有图片</span></button>
      <button class="filter-chip" data-f="hasNote"  onclick="toggleChip(this)">📝 <span>有批注</span></button>
    </div>
  </div>
  <div class="statsbar" id="statsbar">加载中…</div>
  <div class="cards-area">
    <div class="grid" id="grid"></div>
  </div>
</div>
</div>

<!-- Modal -->
<div class="mbd" id="mbd" onclick="closeModal()"></div>
<div class="mbox" id="mbox">
  <div class="mhead">
    <h3 id="mtitle">编辑案例</h3>
    <button class="mclose" onclick="closeModal()">✕</button>
  </div>
  <div class="mbody" id="mbody"></div>
  <div class="mfoot">
    <button class="bsave" onclick="saveEdit()">保存</button>
    <button class="bcancel" onclick="closeModal()">取消</button>
  </div>
</div>
<input type="file" id="imgFile" accept="image/*" style="display:none" onchange="onImgPick(event)">

<script>
const ORIGINAL  = {DATA};
const MODULES   = {MODS_JSON};
const BOOKS     = {BOOKS_JSON};
const ALL_NODES = {NODES_JSON};

// ── State ─────────────────────────────────────────────────────
let D = ORIGINAL.map((c,i)=>({{...c,_i:i}}));
let curTab='books', curSel=null, curFilters=new Set();
let editIdx=null, editImg=null;

function bookCnt(b){{ return D.filter(c=>c.来源书目===b).length }}
function suppCnt(){{ return D.filter(c=>!BOOKS.includes(c.来源书目)).length }}
function nodeCnt(n){{ return D.filter(c=>(c.标签||[]).includes(n)).length }}

// ── Sidebar ────────────────────────────────────────────────────
function switchTab(t){{
  curTab=t; curSel=null;
  document.getElementById('tbooks').classList.toggle('active',t==='books');
  document.getElementById('tnodes').classList.toggle('active',t==='nodes');
  renderNav(); applyAll();
}}

function renderNav(){{
  const nav=document.getElementById('sbNav');
  let h='';
  const allActive=!curSel;
  if(curTab==='books'){{
    h+=ni('全部','all','all',D.length,allActive,false);
    BOOKS.forEach(b=>{{
      const cnt=bookCnt(b);
      const act=curSel&&curSel.t==='book'&&curSel.v===b;
      h+=ni(b,'book',b,cnt,act,false);
    }});
    // 补充阅读固定在最后（兜底：来源书目不在 BOOKS 列表的案例）
    const sc=suppCnt();
    if(sc>0){{
      const suppAct=curSel&&curSel.t==='supplement';
      h+=ni('补充阅读','supplement','',sc,suppAct,false);
    }}
  }} else {{
    const taggedTotal=D.filter(c=>(c.标签||[]).length>0).length;
    h+=ni('全部（含标签案例）','all','all',taggedTotal,allActive,false);
    MODULES.forEach(([title,nodes])=>{{
      h+=`<div class="nav-module">${{title}}</div>`;
      nodes.forEach(node=>{{
        const cnt=nodeCnt(node);
        const act=curSel&&curSel.t==='node'&&curSel.v===node;
        h+=ni(node,'node',node,cnt,act,true);
      }});
    }});
    const untagged=D.filter(c=>!(c.标签||[]).length).length;
    if(untagged){{
      h+=`<div class="nav-module">补充</div>`;
      const act=curSel&&curSel.t==='untagged';
      h+=ni('未标注（史实综述）','untagged','',untagged,act,true);
    }}
  }}
  nav.innerHTML=h;
}}

function ni(label,type,val,cnt,active,indent){{
  const cls=['nav-item',active?'active':'',type==='all'?'all':'',indent?'nav-indent':''].filter(Boolean).join(' ');
  return `<div class="${{cls}}" data-t="${{type}}" data-v="${{e(val)}}">
    <span>${{e(label)}}</span>
    <span class="nav-badge">${{cnt}}</span>
  </div>`;
}}

// Event delegation for nav clicks — fixes HTML-escaping issues
document.getElementById('sbNav').addEventListener('click',ev=>{{
  const item=ev.target.closest('.nav-item');
  if(!item) return;
  const t=item.dataset.t, v=item.dataset.v;
  curSel = (t==='all') ? null : {{t,v}};
  renderNav(); applyAll();
  if(window.innerWidth<768) closeSidebar();
}});

// ── Filter & Sort ──────────────────────────────────────────────
function toggleChip(btn){{
  const f=btn.dataset.f;
  if(curFilters.has(f)) curFilters.delete(f); else curFilters.add(f);
  btn.classList.toggle('on',curFilters.has(f));
  applyAll();
}}

function applyAll(){{
  const q=document.getElementById('searchInput').value.trim().toLowerCase();
  const sort=document.getElementById('sortSel').value;
  let arr=[...D];

  if(curSel){{
    if(curSel.t==='book')           arr=arr.filter(c=>c.来源书目===curSel.v);
    else if(curSel.t==='supplement')arr=arr.filter(c=>!BOOKS.includes(c.来源书目));
    else if(curSel.t==='node')      arr=arr.filter(c=>(c.标签||[]).includes(curSel.v));
    else if(curSel.t==='untagged')  arr=arr.filter(c=>!(c.标签||[]).length);
  }}
  if(curFilters.has('hasImage')) arr=arr.filter(c=>c.image);
  if(curFilters.has('hasNote'))  arr=arr.filter(c=>c.批注&&c.批注.trim());
  if(q) arr=arr.filter(c=>
    [c['作品/事件名称'],c['作者/设计师'],c.年代,c.来源书目,c.简介,c.教学分析]
    .join(' ').toLowerCase().includes(q)
  );
  if(sort==='year-asc')    arr.sort((a,b)=>a.排序年-b.排序年);
  else if(sort==='year-desc')arr.sort((a,b)=>b.排序年-a.排序年);
  else arr.sort((a,b)=>(b.importance||0)-(a.importance||0));

  renderCards(arr);
  document.getElementById('statsbar').textContent=
    `显示 ${{arr.length}} / ${{D.length}} 个案例`;
}}

// ── Cards ──────────────────────────────────────────────────────
function renderCards(arr){{
  const g=document.getElementById('grid');
  if(!arr.length){{g.innerHTML='<div class="empty">🔍 没有符合条件的案例</div>';return}}
  g.innerHTML=arr.map(c=>card(c)).join('');
  g.querySelectorAll('.card').forEach(initLP);
}}

function card(c){{
  const dom=c.类别==='国内';
  const idx=c._i;
  const tags=(c.标签||[]);
  const imp=c.importance||0;
  const rawQuote=(c.原文引用||'').trim();
  const analysis=(c.教学分析||'').trim();
  const body=analysis;
  const note=(c.批注||'').trim();
  const link=(c.link||'').trim();
  // Shorten era: keep text up to first paren
  const era=(c.年代||'').replace(/[（(].*$/,'').trim().slice(0,20);

  // Parse ——书名/章节 prefix from quote
  let quoteText=rawQuote, chapter='';
  if(rawQuote.startsWith('——')){{
    const nl=rawQuote.indexOf('\\n');
    const header=nl>-1?rawQuote.slice(0,nl):rawQuote;
    quoteText=nl>-1?rawQuote.slice(nl+1).trim():'';
    const si=header.indexOf('/');
    if(si>-1) chapter=header.slice(si+1).trim();
    // also handle · separator with no /
    else {{ const m=header.match(/——[^·]*·(.+)/); if(m) chapter=m[1].trim(); }}
  }}

  const starsH=imp?`<div class="c-stars">${{starsDisp(imp)}}</div>`:'';

  const quoteH=quoteText?`<div class="quote">
    <div class="q-text">${{e(quoteText)}}</div>
    <span class="q-toggle" onclick="togQ(this)">展开 ▾</span>
  </div>`:'';

  const bodyH=body?`<div class="analysis">${{bold(e(body))}}</div>`:'';
  const imgH=c.image?`<img class="card-img" src="${{c.image}}" alt="">`:'';
  const noteH=note?`<div class="note"><div class="note-lbl">📌 批注</div>${{e(note)}}</div>`:'';
  const linkH=link?`<hr class="link-sep">
    <div class="link-row">🔗 <a href="${{e(link)}}" target="_blank" rel="noopener">${{e(link.length>55?link.slice(0,55)+'…':link)}}</a></div>
    <hr class="link-sep">`:'';

  // Tags: [国内/国外] [年代?] [subject tags...]
  const catCls=dom?'cat-dom':'cat-for';
  const catChip=`<span class="tag ${{catCls}}">${{e(c.类别||'')}}</span>`;
  const eraChip=era?`<span class="tag era-tag">${{e(era)}}</span>`:'';
  const nodeChips=tags.map(t=>`<span class="tag" data-node="${{e(t)}}">${{e(t)}}</span>`).join('');
  const tagsH=catChip+eraChip+nodeChips;

  // Meta: 来源书目 (+ 章节 if any), single line
  const src=(c.来源书目||'').replace(/[《》]/g,'');
  const metaH=`<div class="c-meta">${{e(src)}}${{chapter?`<br><span class="c-chapter">${{e(chapter)}}</span>`:''}}</div>`;

  return `<div class="card ${{dom?'dom':'for'}}" data-idx="${{idx}}">
  <button class="edit-btn" onclick="openEdit(${{idx}})">✎ 编辑</button>
  <div class="c-title-row">
    <div class="c-title">${{e(c['作品/事件名称']||'')}}</div>
    ${{starsH}}
  </div>
  ${{quoteH}}${{bodyH}}${{imgH}}${{noteH}}${{linkH}}
  <div class="c-foot">
    <div class="tags">${{tagsH}}</div>
    ${{metaH}}
  </div>
</div>`;
}}

// Tag click → filter by node
document.getElementById('grid').addEventListener('click',ev=>{{
  const tag=ev.target.closest('.tag');
  if(!tag) return;
  const node=tag.dataset.node;
  if(!node) return;
  curTab='nodes'; curSel={{t:'node',v:node}};
  document.getElementById('tbooks').classList.remove('active');
  document.getElementById('tnodes').classList.add('active');
  renderNav(); applyAll();
}});

function starsDisp(r){{
  let h='';
  for(let i=1;i<=5;i++){{
    if(r>=i)      h+=`<span class="s full">★</span>`;
    else if(r>=i-.5) h+=`<span class="s half">★</span>`;
    else           h+=`<span class="s">★</span>`;
  }}
  return h;
}}
function togQ(btn){{
  const t=btn.closest('.quote').querySelector('.q-text');
  const open=t.classList.toggle('open');
  btn.textContent=open?'收起 ▴':'展开 ▾';
}}
function bold(s){{return s.replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')}}
function e(s){{
  return String(s)
    .replace(/&/g,'&amp;').replace(/</g,'&lt;')
    .replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}}

// ── Long press ─────────────────────────────────────────────────
let lpt=null;
function initLP(card){{
  card.addEventListener('touchstart',()=>{{
    lpt=setTimeout(()=>card.classList.add('lp'),480);
  }},{{passive:true}});
  ['touchend','touchmove','touchcancel'].forEach(ev=>
    card.addEventListener(ev,()=>clearTimeout(lpt),{{passive:true}})
  );
  card.addEventListener('touchend',()=>
    setTimeout(()=>card.classList.remove('lp'),2500),{{passive:true}}
  );
}}

// ── Edit Modal ──────────────────────────────────────────────────
function openEdit(idx){{
  editIdx=idx; editImg=null;
  const c=D[idx];
  document.getElementById('mtitle').textContent=c['作品/事件名称']||'编辑案例';
  document.getElementById('mbody').innerHTML=buildForm(c);
  document.getElementById('mbd').classList.add('show');
  document.getElementById('mbox').classList.add('show');
}}

function buildForm(c){{
  const r=c.importance||0;
  const siClass=i=>r>=i?'si lit':r>=i-.5?'si half-lit':'si';
  const siChar =i=>r>=i?'★':r>=i-.5?'★':'☆';
  const starsIn=[1,2,3,4,5].map(i=>
    `<span class="spos" data-p="${{i}}"><span class="${{siClass(i)}}">${{siChar(i)}}</span></span>`
  ).join('');
  const imgSec=c.image
    ?`<div class="img-wrap"><img class="img-preview" src="${{c.image}}"><span class="img-rm" onclick="rmImg()">✕</span></div>`
    :`<div class="img-area" onclick="document.getElementById('imgFile').click()">📷 点击上传图片</div>`;

  // Tag editor: existing chips + input
  const existChips=(c.标签||[]).map(t=>
    `<span class="te-chip" data-v="${{e(t)}}">${{e(t)}}<button class="te-rm" type="button" onclick="rmTeChip(this)">×</button></span>`
  ).join('');
  const datalistOpts=ALL_NODES.map(n=>`<option value="${{e(n)}}">`).join('');

  return `
<div class="fg"><label class="fl">标题</label>
  <input class="fin" id="ftitle" type="text" value="${{e(c['作品/事件名称']||'')}}"></div>
<div class="fg"><label class="fl">原文引用</label>
  <textarea class="fta" id="fq" rows="4">${{e(c.原文引用||'')}}</textarea></div>
<div class="fg"><label class="fl">教学分析</label>
  <textarea class="fta" id="fa" rows="6">${{e(c.教学分析||'')}}</textarea></div>
<div class="fg"><label class="fl">批注</label>
  <textarea class="fta" id="fn" rows="3">${{e(c.批注||'')}}</textarea></div>
<div class="fg"><label class="fl">主题标签 <span class="opt">（输入后按 Enter 添加）</span></label>
  <div class="tag-editor" id="tagEditor" onclick="this.querySelector('.te-in').focus()">
    ${{existChips}}
    <input class="te-in" id="tagInput" list="nodeList" placeholder="选择或输入标签…" onkeydown="onTeKey(event)" oninput="onTeInput(event)">
  </div>
  <datalist id="nodeList">${{datalistOpts}}</datalist>
</div>
<div class="fg"><label class="fl">图片 <span class="opt">（可选）</span></label>
  <div id="imgArea">${{imgSec}}</div></div>
<div class="fg"><label class="fl">链接 <span class="opt">（可选）</span></label>
  <input class="fin" id="fl2" type="url" placeholder="https://…" value="${{e(c.link||'')}}"></div>
<div class="fg"><label class="fl">重要性 <span class="opt">（可选 · 单击½星 双击整星）</span></label>
  <div class="sinput" id="sinput" data-r="${{r}}">
    ${{starsIn}}
    <span class="sval" id="sval">${{r>0?r+'星':'未评'}}</span>
  </div></div>`;
}}

// Star events via delegation
document.getElementById('mbox').addEventListener('click',ev=>{{
  const sp=ev.target.closest('.spos');
  if(!sp) return;
  const p=parseInt(sp.dataset.p);
  const inp=document.getElementById('sinput');
  if(!inp) return;
  const cur=parseFloat(inp.dataset.r)||0;
  // Single click: set to p-0.5; if already p-0.5, clear back one step
  const nr=(cur===p-.5)?Math.max(0,p-1):p-.5;
  setStar(nr);
}});
document.getElementById('mbox').addEventListener('dblclick',ev=>{{
  const sp=ev.target.closest('.spos');
  if(!sp) return;
  const p=parseInt(sp.dataset.p);
  const inp=document.getElementById('sinput');
  if(!inp) return;
  const cur=parseFloat(inp.dataset.r)||0;
  const nr=(cur===p)?p-.5:p;
  setStar(nr);
}});

function setStar(r){{
  r=Math.max(0,Math.min(5,r));
  const inp=document.getElementById('sinput');
  if(!inp) return;
  inp.dataset.r=r;
  inp.querySelectorAll('.spos').forEach((sp,i)=>{{
    const si=sp.querySelector('.si');
    const n=i+1;
    if(r>=n)        {{ si.className='si lit';      si.textContent='★' }}
    else if(r>=n-.5){{ si.className='si half-lit'; si.textContent='★' }}
    else             {{ si.className='si';          si.textContent='☆' }}
  }});
  document.getElementById('sval').textContent=r>0?r+'星':'未评';
}}

// Tag editor helpers
function rmTeChip(btn){{ btn.closest('.te-chip').remove(); }}

function onTeKey(e){{
  if(e.key==='Enter'||e.key===','){{
    e.preventDefault();
    const v=e.target.value.trim().replace(/,/g,'');
    if(v) addTeChip(v);
    e.target.value='';
  }} else if(e.key==='Backspace'&&!e.target.value){{
    const chips=document.querySelectorAll('#tagEditor .te-chip');
    if(chips.length) chips[chips.length-1].remove();
  }}
}}

function onTeInput(e){{
  // Auto-add when user selects from datalist (value matches exactly)
  const v=e.target.value.trim();
  if(ALL_NODES.includes(v)){{ addTeChip(v); e.target.value=''; }}
}}

function addTeChip(v){{
  const ed=document.getElementById('tagEditor');
  const inp=document.getElementById('tagInput');
  const existing=[...ed.querySelectorAll('.te-chip')].map(c=>c.dataset.v);
  if(existing.includes(v)) return;
  const chip=document.createElement('span');
  chip.className='te-chip'; chip.dataset.v=v;
  chip.innerHTML=`${{e(v)}}<button class="te-rm" type="button" onclick="rmTeChip(this)">×</button>`;
  ed.insertBefore(chip,inp);
}}

function onImgPick(ev){{
  const f=ev.target.files[0];
  if(!f) return;
  const rd=new FileReader();
  rd.onload=e=>{{
    editImg=e.target.result;
    document.getElementById('imgArea').innerHTML=
      `<div class="img-wrap"><img class="img-preview" src="${{editImg}}"><span class="img-rm" onclick="rmImg()">✕</span></div>`;
  }};
  rd.readAsDataURL(f);
  ev.target.value='';
}}
function rmImg(){{
  editImg='';
  document.getElementById('imgArea').innerHTML=
    `<div class="img-area" onclick="document.getElementById('imgFile').click()">📷 点击上传图片</div>`;
}}

function saveEdit(){{
  if(editIdx===null) return;
  const c=D[editIdx];
  const newTitle=document.getElementById('ftitle').value.trim();
  if(newTitle) c['作品/事件名称']=newTitle;
  c.原文引用 = document.getElementById('fq').value;
  c.教学分析  = document.getElementById('fa').value;
  c.批注     = document.getElementById('fn').value;
  c.link     = document.getElementById('fl2').value;
  if(editImg!==null) c.image=editImg;
  const inp=document.getElementById('sinput');
  if(inp) c.importance=parseFloat(inp.dataset.r)||0;
  // Save tags
  const tagChips=document.querySelectorAll('#tagEditor .te-chip');
  // Also check if there's a partial typed tag to commit
  const tagInpVal=(document.getElementById('tagInput')||{{}}).value?.trim();
  const tagArr=[...tagChips].map(ch=>ch.dataset.v);
  if(tagInpVal) tagArr.push(tagInpVal);
  c.标签=tagArr;
  editImg=null;
  closeModal(); applyAll();
}}
function closeModal(){{
  document.getElementById('mbd').classList.remove('show');
  document.getElementById('mbox').classList.remove('show');
  editIdx=null;
}}

// ── Mobile sidebar ─────────────────────────────────────────────
function toggleSidebar(){{
  document.getElementById('sidebar').classList.toggle('open');
  document.getElementById('overlay').classList.toggle('show');
}}
function closeSidebar(){{
  document.getElementById('sidebar').classList.remove('open');
  document.getElementById('overlay').classList.remove('show');
}}

// ── Export ─────────────────────────────────────────────────────
function exportJSON(){{
  const out=D.map(c=>{{const {{_i,...r}}=c;return r;}});
  const a=Object.assign(document.createElement('a'),{{
    href:URL.createObjectURL(new Blob([JSON.stringify(out,null,2)],{{type:'application/json'}})),
    download:'案例库_export.json'
  }});
  a.click(); URL.revokeObjectURL(a.href);
}}

// ── Init ────────────────────────────────────────────────────────
renderNav(); applyAll();
</script>
</body>
</html>'''

with open('/sessions/clever-tender-cerf/mnt/设计学习/矛盾对立视角案例库/案例库.html','w',encoding='utf-8') as f:
    f.write(HTML)
print(f"完成 {len(HTML)//1024} KB")
