import { fileURLToPath, URL } from "node:url"

import vue from '@vitejs/plugin-vue';
import { defineConfig } from 'vite';
import tsconfigPaths from 'vite-tsconfig-paths'

export default defineConfig({
    plugins: [
        vue(),
        tsconfigPaths()
    ],
    base: '/', //относительно WORKDIR в директивах сборки
    build: {
        outDir: './dist', 

        // Обязательно разрешаем очистку этой папки перед новой сборкой:
        emptyOutDir: true 

    },
    resolve: {
        alias: {
            app: fileURLToPath(new URL('./src/app', import.meta.url)), 
            pages: fileURLToPath(new URL('./src/pages', import.meta.url)),
            widgets: fileURLToPath(new URL('./src/widgets', import.meta.url)),
            features: fileURLToPath(new URL('./src/features', import.meta.url)),
            enttities: fileURLToPath(new URL('./src/entities', import.meta.url)),
            '@shared': fileURLToPath(new URL('./src/shared', import.meta.url))
        },
        optimizeDeps: {
            exclude: ['@shared'],
            include: ['vue']
        }
    },
    server: {
        port: 80
    }
})