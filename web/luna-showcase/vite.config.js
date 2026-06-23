import { defineConfig } from 'vite';

// 獨立 demo；root 即本資料夾。base 設成相對路徑，方便日後嵌入 SHOPLINE 自訂頁。
export default defineConfig({
  base: './',
  server: {
    host: true,
    port: 5180,
  },
  build: {
    outDir: 'dist',
    target: 'es2019',
  },
});
