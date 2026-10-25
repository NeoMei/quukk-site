// Screenshot fixture: actual SuperWagie workbench components, isolated demo data.
// No production API, credentials, user task files, or disk writes are exposed.
import path from 'node:path';
import fs from 'node:fs/promises';

const productRoot = '/Users/neomei/项目/codexprojects/SuperWagie-open';
const panel = path.join(productRoot, 'packages/extensions/workbench/panel');
const bundle = await Bun.build({
  entrypoints: [path.join(panel, 'app.ts')], target: 'browser', format: 'iife', write: false,
  plugins: [{ name: 'sdk', setup(build) {
    build.onResolve({ filter: /^@openchamber\/sdk(?:\/ui)?$/ }, ({ path: entry }) => ({
      path: path.join(productRoot, `packages/sdk/src/${entry.endsWith('/ui') ? 'ui/index.ts' : 'index.ts'}`),
    }));
  } }],
});
if (!bundle.success) throw new Error('Workbench build failed');
const code = await bundle.outputs[0].text();
const context = {
  locale: 'zh', directory: null, session: null, surface: 'page',
  connection: { connected: false, account: '' }, settings: {}, item: null,
  theme: { mode: 'light', tokens: {
    background: '#fff', elevated: '#fff', foreground: '#182126', muted: '#657078',
    subtle: '#eee', border: '#ccc', hover: '#eee', selection: '#ddd', focus: '#444',
    primary: '#236c63', font: '"Segoe UI", Arial, sans-serif', mutedSurface: '#eee',
    elevatedForeground: '#111', active: '#ddd', selectionForeground: '#111',
    primaryForeground: '#fff', primaryText: '#236c63', successText: '#444',
    warningText: '#444', errorText: '#444', infoText: '#444', success: '#444',
    warning: '#444', error: '#444', info: '#444', mono: 'monospace', radius: '8px',
  } },
};
const now = Date.now();
const day = (offset = 0) => new Intl.DateTimeFormat('en-CA', {
  timeZone: 'Asia/Shanghai', year: 'numeric', month: '2-digit', day: '2-digit',
}).format(new Date(now + offset * 86400000));
const tasks = [
  `- [ ] 整理产品介绍材料 <!-- sw ${JSON.stringify({ id: 'demo-materials', state: 'in_progress', priority: 'high', due: day(), origin: 'user' })} -->`,
  `- [ ] 准备下周项目汇报 <!-- sw ${JSON.stringify({ id: 'demo-presentation', state: 'planned', priority: 'normal', due: day(1), origin: 'user' })} -->`,
].join('\n') + '\n';
const notes = [
  { id: 'demo-note-1', body: '产品介绍：先说清楚解决什么问题，再展示真实界面。', createdAt: now - 600000 },
  { id: 'demo-note-2', body: '项目汇报：目标、进展、下一步，控制在三页以内。', createdAt: now - 1800000 },
];
const project = { id: 'demo-product-intro', name: '产品介绍', directory: '/demo/Documents/SuperWagie/文档/产品介绍' };
const outputs = [
  { name: '产品介绍.docx', kind: 'file' },
  { name: '产品介绍.pdf', kind: 'file' },
];
const html = `<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>SuperWagie 演示工作台</title>
<style>html,body{margin:0;background:#fff}iframe{display:block;border:0;height:100vh;max-width:100%;margin:auto;background:#fff}</style>
<script>localStorage.setItem('oc.workbench.notes', ${JSON.stringify(JSON.stringify(notes))});localStorage.setItem('oc.workbench.notesCollapsed','0');</script>
<iframe title="SuperWagie 产品组件 · 演示数据" src="/panel/page.html"></iframe>
<script>
const f=document.querySelector('iframe');
const params=new URLSearchParams(location.search);
f.style.width=(params.get('width')||'1440')+'px';
const ready=${JSON.stringify(context)};
ready.locale=params.get('locale')||'zh';
const demoProject=${JSON.stringify(project)};
const demoTasks=${JSON.stringify(tasks)};
const demoOutputs=${JSON.stringify(outputs)};
function send(type,payload,id){f.contentWindow.postMessage({channel:'openchamber.sdk',v:1,type,...(id?{id,ok:true}:{}),payload},'*');}
addEventListener('message',e=>{
 if(e.source!==f.contentWindow||e.data?.channel!=='openchamber.sdk')return;
 const m=e.data;
 if(m.type==='hello'){send('ready',ready);return;}
 if(m.type==='workspace-read'){
   send('result',m.payload.kind==='projects'
    ?{kind:'projects',state:'ready',projects:[demoProject]}
    :{kind:'sessions',projectId:demoProject.id,state:'ready',coverage:[],sessions:[]},m.id);return;
 }
 if(m.type==='file-stat'){
   send('result',m.payload.path==='任务.md'?{kind:'missing'}:{kind:'file',size:16000,mtime:${now - 3600000}},m.id);return;
 }
 if(m.type==='file-read'){send('result',{content:m.payload.path==='~/.config/openchamber/tasks.md'?demoTasks:''},m.id);return;}
 if(m.type==='file-list'){send('result',{entries:m.payload.path===demoProject.directory?demoOutputs:[]},m.id);return;}
 if(m.type==='request'){send('result',{status:200,body:JSON.stringify({weather:null})},m.id);return;}
 // Unsupported actions deliberately do nothing: this fixture cannot write files or start real work.
 send('result',undefined,m.id);
});
</script></html>`;

const server = Bun.serve({ hostname: '127.0.0.1', port: 43185, async fetch(req) {
  const url = new URL(req.url);
  if (url.pathname === '/') return new Response(html, { headers: { 'content-type': 'text/html; charset=utf-8' } });
  if (url.pathname === '/panel/page.js') return new Response(code, { headers: { 'content-type': 'application/javascript' } });
  if (['/panel/page.html', '/panel/logo.png', '/panel/brand-logo.png'].includes(url.pathname)) {
    const file = path.join(panel, path.basename(url.pathname));
    return new Response(await fs.readFile(file), { headers: { 'content-type': file.endsWith('.png') ? 'image/png' : 'text/html; charset=utf-8' } });
  }
  return new Response('Not found', { status: 404 });
} });
console.log('SuperWagie demo-data fixture http://127.0.0.1:' + server.port);
