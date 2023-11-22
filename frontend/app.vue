<template>
  <v-app class="bg-grey-lighten-2 overflow-auto">
    <v-card class="mx-12 mb-12"
      ><v-card bg-color="transparent">
        <v-tabs grow bg-color="#212b59">
          <v-tab
            v-for="item in items"
            :to="item.value"
            :text="item.title"
          ></v-tab> </v-tabs></v-card
    >
    <v-row justify="center">
      <v-col><NuxtPage /></v-col>
    </v-row></v-card>
  </v-app>
</template>
<script setup>
const items = ref([
  {
    title: "Home",
    value: "/",
  },
//   {
//     title: "Auditoria",
//     value: "audit",
//   },
//   {
//     title: "Não Corformidade",
//     value: "nonCompliance",
//   },
  {
    title: "Gerenciamento",
    value: "management",
  },
]);
</script>
