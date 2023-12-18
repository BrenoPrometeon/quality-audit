<template>
  <v-card elevation="8" :disabled="!(i == stepCompliance)" width="350">
    <v-card
      rounded="0"
      :class="['text-h6', 'timeline__opossitive', 'text-center', 'pa-2']"
    >
      {{ item.textOppositive }}
    </v-card>
    <v-card-text v-if="item.title == 'Plano de Ação'">
      <v-select
        label="Selecionar Líder"
        variant="underlined"
      ></v-select>

      <v-select
        label="Selecionar Monitor"
        variant="underlined"
      ></v-select>
    </v-card-text>
    <v-card-text v-else>
      <v-select
        label="Selecionar Responsáveis"
        variant="underlined"
        multiple
      ></v-select>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  props: {
    i: {
      type: Number,
      required: true,
    },
    stepCompliance: {
      type: Number,
      required: true,
    },
    item: {
      type: Object,
      required: true,
    },
  },

  data: () => ({}),
};
</script>

<style scoped>
.timeline__opossitive {
  background-color: #59a2b5;
  color: white;
}
</style>
