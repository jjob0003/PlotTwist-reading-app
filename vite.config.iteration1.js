// vite.config.iteration1.js（旧版本）
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  base: '/iteration1/' // 非常关键：告诉 vite 生成的资源路径从 /iteration1/ 开始
})
