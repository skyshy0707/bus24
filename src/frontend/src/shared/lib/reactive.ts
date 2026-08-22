import { reactive, onUnmounted, watch } from 'vue'
import type { Mutate, StoreApi } from 'zustand/vanilla'

// Универсальная функция, которая делает Zustand-хранилище реактивным для Vue
export function useStore<T extends object>(zustandStore: Mutate<StoreApi<T>, []>) {
  // Создаем реактивный объект Vue, наполняя его текущим состоянием стора
  const state = reactive({ ...zustandStore.getState() }) as any

  // Подписываемся на изменения Zustand-стора в памяти
  const unsubscribe = zustandStore.subscribe((newState) => {
    Object.assign(state, newState) // Синхронизируем данные при обновлении
  })

  // Автоматически отписываемся от обновлений при уничтожении компонента Vue
  onUnmounted(() => {
    unsubscribe()
  })

  return state as T
}


export function makeReactive<T>(key: string, initValue: T){
  const saved = localStorage.getItem(key)
  const state = reactive({ value: saved !== null ? JSON.parse(saved) : initValue})
  watch(
    () => state.value, 
    (newState) => {
      localStorage.setItem(key, JSON.stringify(newState))
    }, { deep: true })

  return state
}