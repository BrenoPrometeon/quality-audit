<template>
  <div class="ma-3">
    <div class="box" v-for="i in items.filter((i) => obj[i.value])">
      <v-card-title class="text-center"> {{ i.title }} </v-card-title>
      <v-divider class="mx-6"></v-divider>
      <v-row justify="center"
        ><v-col class="text-center text-h6 my-3">{{
          obj[i.value]
        }}</v-col></v-row
      >
    </div>

    <v-row justify="center"
      ><v-col cols="12" class="text-center"
        ><v-btn color="reprog" class="mt-2 mx-2" @click="boxReprog = true">
          Reprogramar
        </v-btn>
        <v-btn
          color="success"
          width="120"
          class="mt-2 mx-2"
          @click="boxSave = true"
        >
          Concluir
        </v-btn></v-col
      ></v-row
    >
  </div>

  <!-- ALTERAÇÃO DO PRAZO MÁXIMO PARA ENVIO DO RELATÓRIO E AUDITORIA -->
  <v-dialog v-model="boxReprog" persistent max-width="600">
    <v-card>
      <v-card-title class="text-center">{{}}</v-card-title>
      <v-card-text>
        <v-row justify="center" no-gutters
          ><v-col cols="auto" class="text-center">
            <n-date-picker
              panel
              clearable
              type="date"
              format="dd/MM/yyyy"
              value-format="dd/MM/yyyy"
              :is-date-disabled="disableDate"
              v-model:formatted-value="dateReport"
              class="text-center date__picker" /></v-col
          ><v-col cols="11" class="text-center"
            ><p class="text-overline">Motivo do Reajuste</p>
            <v-text-field
              variant="outlined"
              label="Descreva o porquê necessita de reajuste"
              v-model="reasonEditReport"
            ></v-text-field></v-col
        ></v-row>
      </v-card-text>
      <!-- SAVE BUTTON -->
      <v-card-actions class="end__card__save">
        <v-row justify="end" class="mx-3"
          ><v-btn color="white" @click="boxReprog = false">Salvar</v-btn></v-row
        >
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- CAIXA DE CONCLUSÃO -->
  <v-dialog v-model="boxSave" persistent max-width="600">
    <v-card>
      <v-card-title class="text-center text-h5 my-3">Conclusão</v-card-title>

      <v-card-text>
        <v-row justify="center"
          ><v-col cols="auto" class="text-center">
            <v-divider></v-divider>
            <n-date-picker
              panel
              type="date"
              clearable
              format="dd/MM/yyyy"
              :is-date-disabled="disableDate"
              value-format="dd/MM/yyyy"
              v-model:formatted-value="dateReport"
              class="text-center date__picker" /></v-col
          ><v-col cols="auto" class="text-center"
            ><v-card-title class="text-center text-h5">{{
              obj.customField
            }}</v-card-title>
            <v-divider></v-divider>
            <n-date-picker
              panel
              type="date"
              clearable
              format="dd/MM/yyyy"
              :is-date-disabled="disableDate"
              value-format="dd/MM/yyyy"
              v-model:formatted-value="dateReport"
              class="text-center date__picker" /></v-col
        ></v-row>
      </v-card-text>
      <!-- SAVE BUTTON -->
      <v-card-actions class="end__card__save">
        <v-row justify="end" class="mx-3"
          ><v-btn color="white" @click="boxSave = false">Salvar</v-btn></v-row
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import queryPriority from "~/queries/priorities.gql";
import mutationDateUpdate from "~/queries/putDateUpdates.gql";

export default {
  props: {
    obj: {
      required: false,
      default: { prev: "22/10/2023", eff: "22/10/2023" },
    },
  },
  data: () => ({
    boxSave: false,
    boxReprog: false,
    dateReport: null,
    reasonEditReport: null,
    items: [
      {
        title: "Previsto",
        value: "prev",
      },
      {
        title: "Reprogramado",
        value: "reprog",
      },
      {
        title: "Efetivo",
        value: "eff",
      },
    ],
  }),
  methods: {
    disableDate(ts) {
      return ts < Date.now();
    },
    teste() {
      // useAsyncQuery(queryPriority, {id:1}).then(({data})=>{
      //   console.log(data)
      // })
      const { mutate: mutation } = useMutation(mutationDateUpdate);
      mutation({
        reason: "Testando",
        newDate: "2023-10-22",
        dateId: 1,
      }).then((response) => console.log("Hello"));
    },
  },
};
</script>
<style scoped>
.box {
  font-family: "Lucida Sans", "Lucida Sans Regular", "Lucida Grande",
    "Lucida Sans Unicode", Geneva, Verdana, sans-serif;
}
.end__card__save {
  background-color: #212b59;
  margin-top: 0.3rem;
}
</style>
