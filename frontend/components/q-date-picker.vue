<template>
  <div class="ma-3" v-if="obj">
    <!-- FORECAST -->
    <div class="box" v-if="obj.forecast">
      <v-card-title class="text-center"> {{ items[0].title }} </v-card-title>
      <v-divider class="mx-6"></v-divider>
      <v-row justify="center"
        ><v-col class="text-center text-h6 my-3">{{
          formatDate(obj.forecast)
        }}</v-col></v-row
      >
    </div>
    <!-- REPROGRAM -->
    <div class="box" v-if="dateUpdates.length > 0">
      <v-card-title class="text-center"> {{ items[1].title }} </v-card-title>
      <v-divider class="mx-6"></v-divider>
      <v-row justify="center"
        ><v-col class="text-center text-h6 my-3">
          {{ formatDate(getMaxIdObject(dateUpdates).newDate) }}
        </v-col></v-row
      >
    </div>
    <!-- EFFECTIVE -->
    <div class="box" v-if="obj.effective">
      <v-card-title class="text-center"> {{ items[2].title }} </v-card-title>
      <v-divider class="mx-6"></v-divider>
      <v-row justify="center"
        ><v-col class="text-center text-h6 my-3">{{
          formatDate(obj.effective)
        }}</v-col></v-row
      >
    </div>

    <!-- BUTTONS -->
    <v-row justify="center" v-if="!obj.effective"
      ><v-col cols="12" class="text-center"
        ><v-btn color="reprog" class="mt-2 mx-2" @click="boxReprog = true">
          Reprogramar
        </v-btn>
        <v-btn color="success" width="120" class="mt-2 mx-2" @click="boxSave = true">
          Concluir
        </v-btn></v-col
      ></v-row
    >
  </div>
  <div v-else class="text-center">
    <img src="../no_data.jpg" width="200" alt="Sem dados" />
  </div>

  <!-- ALTERAÇÃO DO PRAZO MÁXIMO PARA ENVIO DO RELATÓRIO E AUDITORIA -->
  <v-dialog v-model="boxReprog" persistent max-width="600">
    <v-card>
      <v-card-title class="text-center"></v-card-title>
      <v-card-text>
        <v-row justify="center" no-gutters
          ><v-col cols="auto" class="text-center">
            <n-date-picker
              panel
              clearable
              type="date"
              format="dd/MM/yyyy"
              :is-date-disabled="disableDate"
              value-format="yyyy-MM-dd"
              v-model:formatted-value="dateReprog.newDate"
              class="text-center date__picker" /></v-col
          ><v-col cols="11" class="text-center"
            ><p class="text-overline">Motivo do Reajuste</p>
            <v-text-field
              variant="outlined"
              label="Descreva o porquê necessita de reajuste"
              v-model="dateReprog.reason"
            ></v-text-field></v-col
        ></v-row>
      </v-card-text>
      <!-- SAVE BUTTON -->
      <v-card-actions class="end__card__save">
        <v-row justify="end" class="mx-3"
          ><v-btn color="white" @click="saveReprog()">Salvar</v-btn></v-row
        >
      </v-card-actions>
    </v-card>
  </v-dialog>

  <!-- CAIXA DE CONCLUSÃO -->
  <v-dialog v-model="boxSave" persistent max-width="600">
    <v-card>
      <v-card-title class="text-center text-h5 mt-3">Data Efetiva</v-card-title>

      <v-card-text>
        <v-row justify="center"
          ><v-col cols="auto" class="text-center">
            <v-divider></v-divider>
            <n-date-picker
              panel
              type="date"
              clearable
              format="dd/MM/yyyy"
              :is-date-disabled="disablePastDate"
              value-format="yyyy-MM-dd"
              v-model:formatted-value="dateSave.effectiveDate"
              class="text-center date__picker"
          /></v-col>
          <v-col
            cols="12"
            class="text-center"
            v-if="
              obj.dateUpdates
                ? getMaxIdObject(obj.dateUpdates).newDate < new Date()
                  ? true
                  : obj.forecast < new Date()
                  ? true
                  : false
                : false
            "
            ><p class="text-overline">Motivo do Atraso</p>
            <v-text-field
              variant="outlined"
              label="Descreva o porquê houve atraso"
              v-model="dateSave.reason"
            ></v-text-field> </v-col
          ><v-col cols="auto" class="text-center"
            ><v-card-title class="text-center text-h5">{{ customField }}</v-card-title>
            <p v-if="customField == 'Relatório' && dateSave.effectiveDate">
              Escolha uma data acrescidos <br />
              10 dias úteis apartir de
              {{ formatDate(dateSave.effectiveDate) }}
            </p>
            <v-divider></v-divider>
            <n-date-picker
              panel
              type="date"
              clearable
              format="dd/MM/yyyy"
              :is-date-disabled="disableDate"
              value-format="yyyy-MM-dd"
              v-model:formatted-value="dateSave.customDate"
              class="text-center date__picker" /></v-col
        ></v-row>
      </v-card-text>
      <!-- SAVE BUTTON -->
      <v-card-actions class="end__card__save">
        <v-row justify="end" class="mx-3"
          ><v-btn color="white" @click="saveEffective('save')">Salvar</v-btn>
          <v-btn color="red" @click="saveEffective('cancel')">Cancelar</v-btn>
          </v-row
        >
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script>
import mutationDateUpdate from "~/queries/putDateUpdates.gql";
import mutationDate from "~/queries/putDate.gql";

export default {
  props: {
    obj: {
      required: false,
    },
    customField: { required: false },
  },
  data: () => ({
    boxSave: false,
    boxReprog: false,
    dateUpdates: [],
    dateReprog: {},
    dateSave: {},
    items: [
      {
        title: "Previsto",
        value: "forecast",
      },
      {
        title: "Reprogramado",
        value: "newDate",
      },
      {
        title: "Efetivo",
        value: "effective",
      },
    ],
  }),
  methods: {
    disableDate(ts) {
      return ts < Date.now();
    },
    disablePastDate(ts) {
      return ts > Date.now();
    },
    getMaxIdObject(dateUpdate) {
      if (!dateUpdate || dateUpdate.length === 0) {
        return { newDate: null };
      }

      return dateUpdate.reduce((prev, current) =>
        prev.id > current.id ? prev : current
      );
    },
    formatDate(dateString) {
      const dateObject = dateString ? new Date(dateString) : null;

      return dateObject ? this.$options.filters.dateFormat(dateObject, "dd-MM-yyyy") : "";
    },
    saveReprog() {
      const { mutate: mutation } = useMutation(mutationDateUpdate);
      mutation({
        dateId: this.obj.id,
        newDate: this.dateReprog.newDate,
        reason: this.dateReprog.reason,
      }).then(({ data }) => {
        message.info("Data Reprogramada!");
        this.dateUpdates = [...this.dateUpdates, this.dateReprog];
        this.dateReprog = {};
      });
      this.boxReprog = false;
    },
    saveEffective(action) {
      if(action === 'save'){
      const { mutate: mutation } = useMutation(mutationDate);
      mutation({
        id: this.obj.id,
        effective: this.dateSave.effectiveDate,
        forecast: this.obj.forecast,
        reason: this.dateSave.reason,
      }).then(({ data }) => {
        message.info("Data Efetiva Inserida!");
        this.dateSave = {};
      });
      this.boxSave = false;
    }
    else {
      this.boxSave = false;
      this.dateSave = {};
    }
  }
  },
  filters: {
    dateFormat(date, format) {
      if (!date) return "";

      const day = date.getDate();
      const month = date.getMonth() + 1;
      const year = date.getFullYear();

      const formattedMonth = month < 10 ? `0${month}` : `${month}`;
      const formattedDay = day < 10 ? `0${day}` : `${day}`;
      return `${formattedDay}/${formattedMonth}/${year}`;
    },
  },
  created() {},
  watch: {
    obj: {
      handler(newValue, oldValue) {
        if (newValue.dateUpdates) this.dateUpdates = newValue.dateUpdates;
        else this.dateUpdates = [];
      },
    },
  },
};
</script>
<style scoped>
.box {
  font-family: "Lucida Sans", "Lucida Sans Regular", "Lucida Grande",
    "Lucida Sans Unicode", Geneva, Verdana, sans-serif;
}

.date__picker {
  border: 1px solid #000;
}
.end__card__save {
  background-color: #212b59;
  margin-top: 0.3rem;
}
</style>
