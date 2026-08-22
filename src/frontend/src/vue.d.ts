import 'vue' 

declare module '@vue/runtime-core' {
    interface ComponentCustomProperties {
        // Для доступности $store в шаблоне компонента:
        $user: Record<string, any>,
        $profile: Record<string, any>,
        $lead: Record<string, any>,
        $unit: Record<string, any>
    }
}