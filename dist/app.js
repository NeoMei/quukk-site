const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', '打开导航菜单');
  navigation.classList.remove('open');
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? '关闭导航菜单' : '打开导航菜单');
  navigation.classList.toggle('open', open);
});
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
document.addEventListener('click', event => {
  if (!event.target.closest('.site-header')) closeMenu();
});
const demoPrompts = {
  office: '整理项目资料，生成一份清晰的汇报大纲。',
  knowledge: '从本地资料中，找到这个项目的背景与关键结论。',
  code: '阅读项目代码，分析问题并给出修改方案。'
};
document.querySelectorAll('[data-demo]').forEach(button => {
  button.addEventListener('click', () => {
    document.querySelectorAll('[data-demo]').forEach(item => {
      const active = item === button;
      item.classList.toggle('active', active);
      item.setAttribute('aria-pressed', String(active));
    });
    document.querySelector('#demo-prompt-text').textContent = demoPrompts[button.dataset.demo];
  });
});
const products = {
  superwagie: { name: 'SuperWagie', url: 'https://superwagie.quukk.com/' },
  agentwiki: { name: 'AgentWiki', url: 'https://agentwiki.quukk.com/' },
  llmrouter: { name: 'LLMRouter', url: 'https://llmrouter.quukk.com/' },
  unihub: { name: 'UniHub', url: 'https://unihub.quukk.com/' },
  xuanji: { name: '璇玑', url: 'http://113.249.120.24:3001/cuiqiang/issues' },
  xiashuo: { name: '虾说', url: 'https://newsradar.dreamdt.cn/claw-web/' },
  lingxi: { name: '灵犀知识库', url: 'https://newsradar.dreamdt.cn/lingxi/' }
};
const scenarios = {
  create: { title: '让一个想法，走得更远。', description: '从资料整理、内容创作到代码开发，用 SuperWagie 推进任务；需要更多视角时，邀请虾说中的智能体一起讨论。', products: ['superwagie', 'xiashuo'] },
  knowledge: { title: '让已有知识，回答新问题。', description: '用 AgentWiki 积累人与智能体共享的项目知识；用灵犀知识库围绕文档检索、提问，找到有来源的答案。', products: ['agentwiki', 'lingxi'] },
  team: { title: '让团队与 Agent，一起向前。', description: '用璇玑分配团队任务、编排多智能体工作流，通过输入与输出事件衔接角色分工；用虾说展开讨论，用 UniHub 管理个人与团队账户。', products: ['xuanji', 'xiashuo', 'unihub'] },
  build: { title: '把模型能力，接入你的应用。', description: '用 LLMRouter 统一模型接口与路由，用 AgentWiki 积累知识与上下文；用璇玑设计多智能体协作流程，配置事件流转与可复用的子流程。', products: ['llmrouter', 'agentwiki', 'xuanji'] }
};
const tabs = [...document.querySelectorAll('[data-scenario]')];
function selectScenario(tab, moveFocus = false) {
  const scenario = scenarios[tab.dataset.scenario];
  tabs.forEach(item => {
    const active = item === tab;
    item.setAttribute('aria-selected', String(active));
    item.tabIndex = active ? 0 : -1;
  });
  document.querySelector('#scenario-title').textContent = scenario.title;
  document.querySelector('#scenario-description').textContent = scenario.description;
  document.querySelector('#scenario-panel').setAttribute('aria-labelledby', tab.id);
  const container = document.querySelector('#scenario-products');
  container.replaceChildren(...scenario.products.map(id => {
    const product = products[id];
    const a = document.createElement('a');
    a.href = product.url;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.textContent = product.name;
    const icon = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    const use = document.createElementNS('http://www.w3.org/2000/svg', 'use');
    use.setAttribute('href', '#arrow-up');
    icon.setAttribute('aria-hidden', 'true');
    icon.append(use);
    a.append(icon);
    return a;
  }));
  if (moveFocus) tab.focus();
}
tabs.forEach((tab, index) => {
  tab.addEventListener('click', () => selectScenario(tab));
  tab.addEventListener('keydown', event => {
    let next;
    if (event.key === 'ArrowRight' || event.key === 'ArrowDown') next = (index + 1) % tabs.length;
    if (event.key === 'ArrowLeft' || event.key === 'ArrowUp') next = (index - 1 + tabs.length) % tabs.length;
    if (event.key === 'Home') next = 0;
    if (event.key === 'End') next = tabs.length - 1;
    if (next !== undefined) { event.preventDefault(); selectScenario(tabs[next], true); }
  });
});
document.querySelector('#year').textContent = new Date().getFullYear();
const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
if ('IntersectionObserver' in window && !reduceMotion) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('entering');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.reveal').forEach((element, index) => {
    element.style.animationDelay = `${(index % 3) * 65}ms`;
    observer.observe(element);
  });
}
