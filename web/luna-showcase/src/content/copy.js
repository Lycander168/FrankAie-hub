// 各章節文案（中英並列），與動畫解耦 —— 改字只動這裡，不碰動畫邏輯。
// 對應影片節奏：散落 → 匯聚組裝 → 啟動發光 → 規格 → 品牌字卡/CTA。

export const COPY = {
  brand: 'LUNA',
  // 商品 handle，對應 SHOPLINE 商品；mock 階段用來查 luna.mock.json
  // 真實商品：LYCANDER LUNA Mag Qi22 二代 25W 認證 3-in-1 攜帶型無線充電器
  productHandle: 'lycander-luna-mag-qi22二代25w認證-3-in1攜帶型無線充電器',

  chapters: [
    {
      // 0 — Hero
      eyebrow: 'LYCANDER · 3-IN-1',
      title: '小露娜',
      sub: 'LUNA Mag Qi22 · 二代\n一片磁吸，三台同充。',
    },
    {
      // 1 — 散落（痛點 / 化繁為簡）
      title: 'Three cables. Three chargers.',
      sub: '手機、手錶、耳機 ——\n出門前的桌面，總是一團線。',
    },
    {
      // 2 — 匯聚組裝（工藝 / 技術價值）
      title: 'Folds into one.',
      sub: 'Qi2 磁吸對位，三座充電區\n收進一片可摺疊、放得進口袋的機身。',
    },
    {
      // 3 — 啟動發光（核心體驗）
      title: 'Snap. It charges.',
      sub: '磁吸即充，25W 快充認證。\n指示光柔柔亮起，像一彎小月。',
    },
    {
      // 4 — 規格（信任）— specs 由下方 specs 陣列渲染
      title: 'The details.',
      specs: [
        ['25W', 'Qi2 認證磁吸快充'],
        ['3-in-1', '手機 / 手錶 / 耳機'],
        ['MagSafe', '強磁對位不滑落'],
        ['Foldable', '摺疊攜帶型機身'],
      ],
    },
    {
      // 5 — 品牌字卡 + CTA（轉換）
      eyebrow: 'LYCANDER',
      title: 'LUNA',
      sub: '化繁為簡，磁吸即充。\nThree devices, one moon.',
    },
  ],
};
