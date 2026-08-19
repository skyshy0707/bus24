import { createApp } from 'vue';

//import s from 'entities/profile/model'

import App from 'app/app.vue'
import router from 'app/router'

//const originalWarn = console.warn;
const app = createApp(App)

app.use(router)


/*
app.config.warnHandler = (msg, ...args) => {
  // Если предупреждение содержит текст про этот проклятый emits — просто молча его игнорируем!
  if (typeof msg === 'string' && msg.includes('neither declared in the emits option')) {
    return
  }
  // Все остальные реальные и важные предупреждения Vue выводим в консоль как обычно
  originalWarn.apply(console, [msg, ...args]);
}
*/
//app.use(s)

app.mount('#app')