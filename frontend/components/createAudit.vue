<template>
    <v-dialog v-model="mostrarCaixaFlutuante" max-width="800">
      <v-card>
        <v-card-title class="text-center">Auditoria</v-card-title>
        <v-card-text>
          <v-row justify="center" class="align-center">
            <v-col cols="6" class="d-flex flex-column align-center">
              <div class="text-overline">Áreas</div>
              <v-select
                v-model="auditDialog.name"
                :items="items"
                variant="outlined"
                label="Escolha uma área"
                class="select__box"
              ></v-select>
              <v-checkbox
                v-model="auditDialog.mp"
                label="Master Plan"
                color="green-darken-2"
                value="John"
              ></v-checkbox></v-col
            ><v-divider vertical></v-divider
            ><v-col cols="6" class="text-center"
              ><v-row justify="center"
                ><n-date-picker
                  panel
                  type="date"
                  v-model:value="auditDialog.date"
                  class="text-center date__picker" /></v-row
            ></v-col>
          </v-row>
        </v-card-text>

        <v-card-actions class="end__card__save">
          <v-row justify="end" class="mx-3"
            ><v-btn color="green" @click="saveAudit()">Salvar</v-btn></v-row
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
</template>

<script>
export default {
  data: () => ({
    mostrarCaixaFlutuante: true,
    auditDialog: {},
    length: [
      {
        name: "Umbreon",
        value: "1",
        date: "33/10",
        description: "Esta seção serve para criar e editar pokemons",
      },
      {
        name: "Charizard",
        value: "2",
        date: "15/06",
        description: "Poderoso Pokémon de fogo",
      },
      {
        name: "Bulbasaur",
        value: "3",
        date: "22/04",
        description: "Possui uma planta brotando em suas costas",
      },
      {
        name: "Pikachu",
        value: "4",
        date: "25/12",
        description: "Famoso Pokémon elétrico",
      },
      {
        name: "Squirtle",
        value: "5",
        date: "03/09",
        description: "Conhecido por sua habilidade na água",
      },
      {
        name: "Jigglypuff",
        value: "6",
        date: "08/11",
        description: "Canta uma canção para fazer os outros dormirem",
      },
    ],
    items: [
      "OE Sales",
      "PMS",
      "Procurement",
      "QMS",
      "ICT",
      "Production Planning",
    ],
    selected: null,
    audit: {},
  }),

  methods: {
    abrirCaixa() {
      this.mostrarCaixaFlutuante = true;
    },
    saveAudit() {
      this.length.push(this.auditDialog);
      this.auditDialog = {};
      this.mostrarCaixaFlutuante = false;
    },
  },

  watch: {
    length(val) {
      this.tab = val - 1;
    },
  },
};
</script>
<style scoped>
.date__picker {
  border: 1px solid #000;
}

.select__box {
  width: 300px;
}

.end__card__save{
  background-color: #000;
  margin-top: 1rem;
}
</style>