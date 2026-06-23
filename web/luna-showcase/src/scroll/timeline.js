import { gsap } from 'gsap';
import { ScrollTrigger } from 'gsap/ScrollTrigger';

gsap.registerPlugin(ScrollTrigger);

// 設定捲動驅動：
//  1) 每個章節的文字淡入 / 位移（對應影片左側襯線字淡入）。
//  2) 一條覆蓋整頁的 ScrollTrigger，回報 0..1 進度給 3D 場景。
export function setupScroll({ onProgress, reduced = false }) {
  const chapters = gsap.utils.toArray('.chapter');

  chapters.forEach((ch) => {
    const items = ch.querySelectorAll('[data-title], [data-sub], [data-eyebrow], .specs li, .buybox');
    if (!items.length) return;

    gsap.set(items, { opacity: 0, y: reduced ? 0 : 36 });

    gsap.to(items, {
      opacity: 1,
      y: 0,
      duration: reduced ? 0.4 : 1.0,
      ease: 'power3.out',
      stagger: reduced ? 0 : 0.12,
      scrollTrigger: {
        trigger: ch,
        start: 'top 72%',
        toggleActions: 'play none none reverse',
      },
    });
  });

  // 整頁進度 → 3D 場景
  ScrollTrigger.create({
    trigger: '#story',
    start: 'top top',
    end: 'bottom bottom',
    onUpdate: (self) => onProgress(self.progress),
  });

  // 進度條
  const bar = document.getElementById('progress-bar');
  ScrollTrigger.create({
    trigger: document.documentElement,
    start: 'top top',
    end: 'bottom bottom',
    onUpdate: (self) => {
      if (bar) bar.style.transform = `scaleX(${self.progress})`;
    },
  });

  return ScrollTrigger;
}
