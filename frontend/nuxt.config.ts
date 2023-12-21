export default defineNuxtConfig({
  modules: ["@nuxtjs/apollo"],
  apollo: {
    clients: {
      default: {
        httpEndpoint: "http://localhost:8000/graphql",
        inMemoryCacheOptions: {
          addTypename: false,
          resultCaching: false,
        },
      },
    },
  },
  ssr: false,
  css: ["vuetify/lib/styles/main.sass"],
  build: {
    transpile: ["vuetify"],
  },
});
