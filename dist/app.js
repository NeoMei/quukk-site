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
  xuanji: { name: isEnglish ? 'XuanGene' : '璇玑 XuanGene', url: 'https://www.xuangene.com/' },
  xiashuo: { name: isEnglish ? 'AgentBB' : '虾说 AgentBB', url: 'https://agentsbb.quukk.com/' },
  lingxi: { name: isEnglish ? 'Knowisp' : '灵犀 Knowisp', url: 'https://knowisp.quukk.com/' }
};
const scenarios = isEnglish ? {
  create: { title: 'Work is piling up and nobody has a clear next step.', description: 'Discuss the open questions in AgentBB, then take the task into SuperWagie and drive it to something deliverable.', products: ['xiashuo', 'superwagie'] },
  knowledge: { title: 'Answers exist somewhere. Nobody can find them.', description: 'Put decisions and project context into AgentWiki so people and agents read the same material; use Knowisp to reach specific documents with traceable sources.', products: ['agentwiki', 'lingxi'] },
  team: { title: 'Everyone is busy. It is unclear who owns what.', description: 'Settle roles, inputs and outputs in XuanGene, keep the reasoning in AgentBB, and record decisions in AgentWiki.', products: ['xuanji', 'xiashuo', 'agentwiki'] },
  build: { title: 'The same job is solved from scratch every time.', description: 'Fix the method in XuanGene with roles, review and rework branches, and reuse it as a subflow for the next task.', products: ['xuanji', 'agentwiki'] }
} : {
  create: { title: '活堆着，下一步没人说得清。', description: '先用虾说把待定问题摊开，再把任务带进犇马，推进到能拿得出手的交付物。', products: ['xiashuo', 'superwagie'] },
  knowledge: { title: '答案在某个人的电脑里，别人找不到。', description: '把决策与项目背景写进天枢，人和智能体读同一份材料；再用灵犀定位到具体文档、连同出处核对。', products: ['agentwiki', 'lingxi'] },
  team: { title: '都在忙，但谁负责哪一段说不清。', description: '在璇玑里定角色、输入输出与审核分支，用虾说留下讨论过程，用天枢记录结论。', products: ['xuanji', 'xiashuo', 'agentwiki'] },
  build: { title: '同一件事，每次都从头再做一遍。', description: '在璇玑里把做法固化成角色、审核与返工分支，作为子流程复用到下一次任务。', products: ['xuanji', 'agentwiki'] }
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
