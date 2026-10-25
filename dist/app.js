const isEnglish = document.documentElement.lang.startsWith('en');
const menuLabels = isEnglish ? { open: 'Open navigation menu', close: 'Close navigation menu' } : { open: '打开导航菜单', close: '关闭导航菜单' };
const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#main-nav');
function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  menuButton.setAttribute('aria-label', menuLabels.open);
  navigation.classList.remove('open');
}
menuButton.addEventListener('click', () => {
  const open = menuButton.getAttribute('aria-expanded') !== 'true';
  menuButton.setAttribute('aria-expanded', String(open));
  menuButton.setAttribute('aria-label', open ? menuLabels.close : menuLabels.open);
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
const products = {
  superwagie: { name: isEnglish ? 'SuperWagie' : '犇马 SuperWagie', url: 'https://www.superwagie.com/' },
  agentwiki: { name: isEnglish ? 'AgentWiki' : '天枢 AgentWiki', url: 'https://AgentWiki.quukk.com/' },
  xuanji: { name: isEnglish ? 'XuanGene' : '璇玑 XuanGene', url: 'http://113.249.120.24:3001/cuiqiang/issues' },
  xiashuo: { name: isEnglish ? 'ClawMessenger' : '虾说 ClawMessenger', url: 'https://newsradar.dreamdt.cn/claw-web/' },
  lingxi: { name: isEnglish ? 'LingXi' : '灵犀 LingXi', url: 'https://newsradar.dreamdt.cn/lingxi/' }
};
const scenarios = isEnglish ? {
  create: { title: 'Take an idea further.', description: 'Use SuperWagie to organize research, create content and write code. Bring in ClawMessenger when you need more perspectives.', products: ['superwagie', 'xiashuo'] },
  knowledge: { title: 'Let what you know answer what’s next.', description: 'Build shared project knowledge for people and agents with AgentWiki. Use LingXi to search documents and ask questions with traceable sources.', products: ['agentwiki', 'lingxi'] },
  team: { title: 'Move forward with your AI team.', description: 'Discuss ideas and differences in ClawMessenger, assign tasks and track progress in XuanGene, and capture project knowledge in AgentWiki.', products: ['xiashuo', 'xuanji', 'agentwiki'] },
  build: { title: 'Give every role a place in the workflow.', description: 'Define agent roles, input and output events, and review loops in XuanGene. Reuse designs through subflows and document them in AgentWiki.', products: ['xuanji', 'agentwiki'] }
} : {
  create: { title: '让一个想法，走得更远。', description: '从资料整理、内容创作到代码开发，用犇马推进任务；需要更多视角时，邀请虾说中的智能体一起讨论。', products: ['superwagie', 'xiashuo'] },
  knowledge: { title: '让已有知识，回答新问题。', description: '用天枢积累人与智能体共享的项目知识；用灵犀围绕文档检索、提问，找到有来源的答案。', products: ['agentwiki', 'lingxi'] },
  team: { title: '让团队与 Agent，一起向前。', description: '用虾说讨论议题、梳理分歧，用璇玑分配任务、跟进进展，用天枢记录项目知识与团队经验。', products: ['xiashuo', 'xuanji', 'agentwiki'] },
  build: { title: '把角色分工，组织成流程。', description: '在璇玑中配置智能体角色、输入输出事件与返工分支，通过子流程复用已有设计；用天枢记录流程说明与项目经验。', products: ['xuanji', 'agentwiki'] }
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

const imageViewer = document.querySelector('.image-viewer');
const viewerImage = document.querySelector('#viewer-image');
let imageTrigger;
document.querySelectorAll('.screenshot-open').forEach(button => {
  button.addEventListener('click', () => {
    imageTrigger = button;
    viewerImage.src = button.dataset.fullImage;
    viewerImage.alt = button.dataset.imageTitle;
    document.querySelector('#image-viewer-title').textContent = button.dataset.imageTitle;
    imageViewer.showModal();
    imageViewer.querySelector('.viewer-scroll').scrollTo(0, 0);
    document.body.classList.add('viewer-active');
  });
});
imageViewer.querySelector('.viewer-close').addEventListener('click', () => imageViewer.close());
imageViewer.addEventListener('click', event => { if (event.target === imageViewer) imageViewer.close(); });
imageViewer.addEventListener('close', () => {
  document.body.classList.remove('viewer-active');
  imageTrigger?.focus();
});

document.querySelectorAll('[data-shot-src]').forEach(button => {
  button.addEventListener('click', () => {
    const figure = button.closest('figure');
    figure.querySelectorAll('[data-shot-src]').forEach(item => item.setAttribute('aria-pressed', String(item === button)));
    const image = figure.querySelector('.screenshot-open img');
    image.src = button.dataset.shotSrc;
    image.alt = button.dataset.shotAlt;
    image.width = button.dataset.shotSrc.includes('live') ? 1276 : 1280;
    image.height = button.dataset.shotSrc.includes('live') ? 910 : 860;
    figure.querySelector('figcaption > span').textContent = button.dataset.shotCaption;
    figure.querySelectorAll('.screenshot-open').forEach(trigger => {
      trigger.dataset.fullImage = button.dataset.shotSrc;
      trigger.dataset.imageTitle = button.dataset.shotTitle;
    });
  });
});
