import { createVuetify} from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'

export default defineNuxtPlugin(nuxtApp => {

const vuetify = createVuetify({
  components: components,
  directives,
  icons: { defaultSet: 'mdi', },
  theme: {
    defaultTheme: 'prometeon',
    themes: {
      prometeon: {
        dark: false,
        colors: {
          primary: '#212b59',
          secondary: "#222",
          accent: "#E5E5E5",
          success: "#3f8255",
          warning: "#dfb256",
          error: "#c6453a",
          info: "#222",
          reprog: "#b55921",
        }
      }
    }
  }
})

  nuxtApp.vueApp.use(vuetify)
})