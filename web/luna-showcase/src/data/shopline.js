// SHOPLINE 資料層 —— 對外只暴露 getProduct(handle)。
// 現在：回傳 mock（luna.mock.json）。
// 之後：設好環境變數即自動切到 SHOPLINE Storefront GraphQL API（read-only），UI/動畫完全不動。
//
// 切 live 需要的環境變數（放在 web/luna-showcase/.env.local，見 .env.example）：
//   VITE_SHOPLINE_DOMAIN   例：your-store.myshopline.com
//   VITE_SHOPLINE_TOKEN    Storefront Access Token（guest 讀取商品只需這個）
//   VITE_SHOPLINE_API_VER  例：v20240301（可省略，有預設）
//
// SHOPLINE Storefront API 為 GraphQL：
//   POST https://{domain}/admin/api/{ver}/storefront/graphql.json   （依店家設定可能略有不同）
//   Headers: Content-Type: application/json, X-SL-Storefront-Access-Token: {token}

import mock from './luna.mock.json';

const DOMAIN = import.meta.env.VITE_SHOPLINE_DOMAIN;
const TOKEN = import.meta.env.VITE_SHOPLINE_TOKEN;
const API_VER = import.meta.env.VITE_SHOPLINE_API_VER || 'v20240301';

export const DATA_SOURCE = TOKEN && DOMAIN ? 'shopline' : 'mock';

const PRODUCT_QUERY = `
  query ProductByHandle($handle: String!) {
    productByHandle(handle: $handle) {
      title
      vendor
      onlineStoreUrl
      availableForSale
      totalInventory
      priceRange { minVariantPrice { amount currencyCode } }
      compareAtPriceRange { minVariantPrice { amount } }
      images(first: 6) { edges { node { url altText } } }
      variants(first: 20) {
        edges { node { id title availableForSale price { amount } } }
      }
    }
  }
`;

// 統一回傳格式 —— 動畫/UI 只認這個介面，不管底層是 mock 還是 live。
function normalize(raw, currencyFallback = 'TWD') {
  return {
    handle: raw.handle,
    title: raw.title,
    vendor: raw.vendor,
    currency: raw.currency || currencyFallback,
    price: raw.price,
    compareAtPrice: raw.compareAtPrice ?? null,
    available: raw.available,
    inventory: raw.inventory ?? null,
    url: raw.url,
    images: raw.images || [],
    variants: raw.variants || [],
  };
}

function fromShopline(node, handle) {
  const price = Number(node.priceRange?.minVariantPrice?.amount ?? 0);
  const compare = Number(node.compareAtPriceRange?.minVariantPrice?.amount ?? 0);
  return normalize(
    {
      handle,
      title: node.title,
      vendor: node.vendor,
      currency: node.priceRange?.minVariantPrice?.currencyCode || 'TWD',
      price,
      compareAtPrice: compare > price ? compare : null,
      available: node.availableForSale,
      inventory: node.totalInventory,
      url: node.onlineStoreUrl,
      images: (node.images?.edges || []).map((e) => ({ src: e.node.url, alt: e.node.altText || '' })),
      variants: (node.variants?.edges || []).map((e) => ({
        id: e.node.id,
        title: e.node.title,
        available: e.node.availableForSale,
        price: Number(e.node.price?.amount ?? price),
      })),
    },
    'TWD'
  );
}

/**
 * 取得商品資料。預設讀 copy.js 設定的 handle（luna）。
 * @param {string} handle
 * @returns {Promise<object>} 正規化商品物件
 */
export async function getProduct(handle = 'luna') {
  if (DATA_SOURCE === 'mock') {
    // 模擬網路延遲，讓載入狀態看得出來
    await new Promise((r) => setTimeout(r, 200));
    return normalize(mock);
  }

  const endpoint = `https://${DOMAIN}/admin/api/${API_VER}/storefront/graphql.json`;
  const res = await fetch(endpoint, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-SL-Storefront-Access-Token': TOKEN,
    },
    body: JSON.stringify({ query: PRODUCT_QUERY, variables: { handle } }),
  });

  if (!res.ok) throw new Error(`SHOPLINE API ${res.status}`);
  const json = await res.json();
  const node = json?.data?.productByHandle;
  if (!node) throw new Error('SHOPLINE: product not found');
  return fromShopline(node, handle);
}

// 價格格式化（給 UI 用）
export function formatPrice(amount, currency = 'TWD') {
  if (amount == null) return '';
  try {
    return new Intl.NumberFormat('zh-TW', { style: 'currency', currency, maximumFractionDigits: 0 }).format(amount);
  } catch {
    return `${currency} ${amount}`;
  }
}
