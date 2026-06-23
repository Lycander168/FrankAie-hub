import Lenis from 'lenis';
import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';
import { COPY } from './content/copy.js';
import { Scene } from './scene/scene.js';
import { setupScroll } from './scroll/timeline.js';
import { getProduct, formatPrice, DATA_SOURCE } from './data/shopline.js';

const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

// ── 1. 注入文案（內容與動畫解耦）─────────────────────────
function fillCopy() {
  document.querySelectorAll('.chapter').forEach((ch) => {
    const i = Number(ch.dataset.chapter);
    const c = COPY.chapters[i];
    if (!c) return;
    const set = (sel, val) => {
      const el = ch.querySelector(sel);
      if (el && val) el.textContent = val;
    };
    set('[data-eyebrow]', c.eyebrow);
    set('[data-title]', c.title);
    // sub 可能含換行
    const sub = ch.querySelector('[data-sub]');
    if (sub && c.sub) sub.innerHTML = c.sub.replace(/\n/g, '<br />');

    const specsEl = ch.querySelector('[data-specs]');
    if (specsEl && c.specs) {
      specsEl.innerHTML = c.specs
        .map(([k, v]) => `<li><b>${k}</b><span>${v}</span></li>`)
        .join('');
    }
  });
  const yEl = document.getElementById('year');
  if (yEl) yEl.textContent = String(new Date().getFullYear());
  const srcEl = document.getElementById('datasrc');
  if (srcEl) srcEl.textContent = `資料來源：${DATA_SOURCE === 'shopline' ? 'SHOPLINE (live)' : 'mock'}`;
}

// ── 2. 平滑捲動（Lenis）+ GSAP 同步 ────────────────────
function initLenis() {
  if (reduced) return null;
  const lenis = new Lenis({ duration: 1.1, smoothWheel: true });
  lenis.on('scroll', ScrollTrigger.update);
  gsap.ticker.add((time) => lenis.raf(time * 1000));
  gsap.ticker.lagSmoothing(0);
  return lenis;
}

// ── 3. SHOPLINE 商品資料 → 商品卡 ──────────────────────
async function fillBuybox() {
  const box = document.getElementById('buybox');
  try {
    const p = await getProduct(COPY.productHandle);

    const priceEl = document.getElementById('price');
    if (priceEl) priceEl.textContent = formatPrice(p.price, p.currency);
    const cmp = document.getElementById('compare');
    if (cmp) cmp.textContent = p.compareAtPrice ? formatPrice(p.compareAtPrice, p.currency) : '';

    const variantsEl = document.getElementById('variants');
    if (variantsEl) {
      variantsEl.innerHTML = p.variants
        .map(
          (v, i) =>
            `<button class="chip${i === 0 ? ' is-active' : ''}" ${v.available ? '' : 'disabled'} data-id="${v.id}">${v.title}${v.available ? '' : ' · 補貨中'}</button>`
        )
        .join('');
      variantsEl.addEventListener('click', (e) => {
        const t = e.target.closest('.chip');
        if (!t || t.disabled) return;
        variantsEl.querySelectorAll('.chip').forEach((c) => c.classList.remove('is-active'));
        t.classList.add('is-active');
      });
    }

    const cta = document.getElementById('cta');
    if (cta) {
      cta.href = p.url || 'https://www.lycander.tw';
      cta.textContent = p.available ? '加入購物車' : '補貨中';
      if (!p.available) cta.classList.add('is-disabled');
    }
    const stock = document.getElementById('stock');
    if (stock) stock.textContent = p.inventory != null ? `現貨 ${p.inventory} 件 · 免運` : '免運出貨';

    box.hidden = false;
  } catch (e) {
    console.warn('[luna] 商品資料載入失敗：', e?.message || e);
    if (box) {
      box.hidden = false;
      box.innerHTML = '<a class="btn" href="https://www.lycander.tw">前往官網選購</a>';
    }
  }
}

// ── 4. 啟動 ────────────────────────────────────────────
async function boot() {
  fillCopy();
  initLenis();

  const canvas = document.getElementById('scene');
  const scene = new Scene(canvas, { reducedMotion: reduced });
  await scene.init();

  setupScroll({ onProgress: (p) => scene.setProgress(p), reduced });

  // 3D 算繪迴圈（接 gsap ticker，與 Lenis 同一時脈）
  gsap.ticker.add(() => scene.render());

  // 收尾
  ScrollTrigger.refresh();
  fillBuybox();

  // 淡出載入遮罩
  const loader = document.getElementById('loader');
  if (loader) {
    loader.classList.add('is-hidden');
    setTimeout(() => loader.remove(), 700);
  }
}

boot();
