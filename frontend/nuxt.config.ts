export default defineNuxtConfig({
  ssr: false,
  css: ["vuetify/lib/styles/main.sass"],
  build: {
    transpile: ["vuetify"],
  },
});
