type ApiMode = 'dev' | 'prod' 

interface ImportMetaEnv {
    readonly VITE_API_MODE?: ApiMode
    readonly VITE_DOMAIN: string
    readonly VITE_API_HOST: string
    readonly VITE_API_URL: string
    readonly VITE_BASE_URL: string
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}