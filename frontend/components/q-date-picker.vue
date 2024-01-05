<template>
  <div class="ma-3" v-if="children">
    <!-- FORECAST -->
    <div class="box" v-if="children.forecast">
      <v-card-title class="text-center"> {{ items[0].title }} </v-card-title>
      <v-divider class="mx-6"></v-divider>
      <v-row justify="center"
        ><v-col class="text-center text-h6 my-3">{{
          formatDate(children.forecast)
        }}</v-col></v-row
      >
    </div>
    <!-- REPROGRAM -->
    <div class="box" v-if="children.dateUpdates.length > 0">
      <v-card-title class="text-center"> {{ items[1].title }} </v-card-title>
      <v-divider class="mx-6"></v-divider>
      <v-row justify="center"
        ><v-col class="text-center text-h6 my-3">
          {{ formatDate(getMaxIdObject(children.dateUpdates).newDate) }}
        </v-col></v-row
      >
    </div>
    <!-- EFFECTIVE -->
    <div class="box" v-if="children.effective">
      <v-card-title class="text-center"> {{ items[2].title }} </v-card-title>
      <v-divider class="mx-6"></v-divider>
      <v-row justify="center"
        ><v-col class="text-center text-h6 my-3">{{
          formatDate(children.effective)
        }}</v-col></v-row
      >
    </div>

    <!-- BUTTONS -->
    <v-row justify="center" v-if="!children.effective"
      ><v-col cols="12" class="text-center">
        <!-- ALTERAÇÃO DO PRAZO MÁXIMO PARA ENVIO DO RELATÓRIO E AUDITORIA -->
        <v-dialog persistent max-width="600">
          <template v-slot:activator="{ props }">
            <v-btn color="reprog" class="mt-2 mx-2" v-bind="props">
              Reprogramar
            </v-btn>
          </template>
          <template v-slot:default="{ isActive }">
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
                      :disabled="!dateReprog.newDate"
                      variant="outlined"
                      label="Descreva o porquê necessita de reajuste"
                      v-model="dateReprog.reason"
                    ></v-text-field></v-col
                ></v-row>
              </v-card-text>
              <!-- SAVE BUTTON -->
              <v-card-actions class="end__card__save">
                <v-row justify="end" class="mx-3">
                  <v-btn color="red" @click="isActive.value = false"
                    >Cancelar</v-btn
                  ><v-btn
                    :disabled="!dateReprog.reason"
                    color="white"
                    @click="
                      reprogDate();
                      isActive.value = false;
                    "
                    >Salvar</v-btn
                  ></v-row
                >
              </v-card-actions>
            </v-card>
          </template>
        </v-dialog>

        <!-- CAIXA DE CONCLUSÃO -->
        <v-dialog persistent max-width="600">
          <template v-slot:activator="{ props }">
            <v-btn color="success" width="120" class="mt-2 mx-2" v-bind="props">
              Concluir
            </v-btn>
          </template>
          <template v-slot:default="{ isActive }">
            <v-card>
              <v-card-title class="text-center text-h5 mt-3"
                >Data Efetiva</v-card-title
              >

              <v-card-text>
                <v-row justify="center" no-gutters
                  ><v-col cols="auto" class="text-center">
                    <v-divider></v-divider>
                    <n-date-picker
                      panel
                      type="date"
                      clearable
                      format="dd/MM/yyyy"
                      :is-date-disabled="disablePastDate"
                      value-format="yyyy-MM-dd"
                      v-model:formatted-value="dateEffective.effective"
                      class="text-center date__picker"
                  /></v-col>
                  <v-col
                    cols="10"
                    class="text-center"
                    v-if="
                      children.dateUpdates.length
                        ? new Date(
                            `${
                              getMaxIdObject(children.dateUpdates).newDate
                            }T00:00`
                          ) < new Date()
                        : new Date(`${children.forecast}T00:00`) < new Date()
                    "
                  >
                    <p class="text-overline">Motivo do Atraso</p>
                    <v-text-field
                      variant="outlined"
                      label="Descreva o porquê houve atraso"
                      v-model="dateEffective.reason"
                    ></v-text-field></v-col
                  ><v-col cols="auto" class="text-center" v-if="customField?.title"
                    ><v-card-title class="text-center text-h5">{{
                      customField.title
                    }}</v-card-title>
                    <p
                      v-if="
                        customField.title == 'Relatório' &&
                        dateEffective.effective
                      "
                    >
                      Escolha uma data acrescidos <br />
                      10 dias úteis apartir de
                      {{ formatDate(dateEffective.effective) }}
                    </p>
                    <v-divider></v-divider>
                    <n-date-picker
                      panel
                      type="date"
                      clearable
                      format="dd/MM/yyyy"
                      :is-date-disabled="disableDate"
                      value-format="yyyy-MM-dd"
                      v-model:formatted-value="dateCustom.forecast"
                      class="text-center date__picker" /></v-col
                ></v-row>
              </v-card-text>
              <!-- SAVE BUTTON -->
              <v-card-actions class="end__card__save">
                <v-row justify="end" class="mx-3">
                  <v-btn color="red" @click="isActive.value = false"
                    >Cancelar</v-btn
                  >
                  <v-btn
                    color="white"
                    :disabled="
                      !(props.customField?.value
                        ? dateCustom.forecast
                        : dateEffective.effective)
                    "
                    @click="
                      effectiveDate();
                      isActive.value = false;
                      customField?.value ? createDate() : '';
                    "
                    >Salvar</v-btn
                  >
                </v-row>
              </v-card-actions>
            </v-card>
          </template>
        </v-dialog>
      </v-col></v-row
    >
  </div>
  <div v-else class="text-center">
    <img src="../no_data.jpg" width="200" alt="Sem dados" />
  </div>
</template>

<script setup>
const props = defineProps({
  session: { required: true },
  father: { required: true },
  children: { required: true },
  customField: { required: false },
});
const emit = defineEmits(["refreshFields"]);

const dateReprog = ref({});
const dateEffective = ref({});
const dateCustom = ref({});

// FUNÇÃO PARA REPROGRAMAÇÃO
const {
  mutate: reprogDate,
  loading: reprogLoading,
  onDone: reprogOnDone,
} = useMutation(mutationDateUpdate, {
  refetchQueries: [{ query: queryAudit }],
  variables: dateReprog.value,
});
reprogOnDone((data) => {
  message.info("Reprogramação concluída!");
  emit("refreshFields");
});

// FUNÇÃO PARA DATA EFETIVA
const {
  mutate: effectiveDate,
  loading: effectiveLoading,
  onDone: effectiveOnDone,
} = useMutation(mutationDate, {
  refetchQueries: [{ query: queryAudit }],
  variables: dateEffective.value,
});
effectiveOnDone((data) => {
  message.info("Data Efetiva inserida com sucesso!");
  if(Object.keys(props.customField).length === 0)
    emit("refreshFields");
});

// FUNÇÃO PARA CRIAR A DATA DO PRÓXIMO CAMPO
const {
  mutate: createDate,
  loading: createDateLoading,
  onDone: createDateOnDone,
} = useMutation(mutationDate, {
  variables: dateCustom.value,
});

createDateOnDone(({ data }) => {
  let mutationVariables = {};
  let validation = null;
  let deployment = null;
  if (props.session === "audit") {
    mutationVariables = {
      reportDateId: data.putDate.id,
      dateId: props.father.dateEnd?.id,
      processId: props.father.process?.id,
      id: props.father.id,
    };
    
    const { mutate: mutationFatherAudit, onDone: auditOnDone } = useMutation(
      mutationAudit,
      {
        variables: mutationVariables,
      }
    );

    mutationFatherAudit();

    auditOnDone(({ data }) => {
      emit("refreshFields");
    });
  } else if (props.session === "nonCompliance") {
    if (props.customField.value === "validation") {
      validation = data.putDate.id;
    } else if (props.customField.value === "deployment") {
      deployment = data.putDate.id;
    }
    mutationVariables = {
      identifier: props.father?.identifier,
      actionPlan: props.father?.actionPlan,
      auditId: props.father?.auditId,
      description: props.father?.description,
      id: props.father?.id,
      priorityId: props.father?.priorityId,
      validation: props.father?.validation? props.father.validation: validation,
      deployment: props.father?.deployment? props.father.deployment: deployment,
    };
    const { mutate: mutationFatherCompliance, onDone: nonComplianceOnDone } = useMutation(
      mutationNonCompliance,
      {
        variables: mutationVariables,
      }
    );
    mutationFatherCompliance();
    nonComplianceOnDone(({ data }) => {
      emit("refreshFields");
    });

  }
});

watch(
  () => props.children,
  (newValue, oldValue) => {
    if (newValue && newValue.id && newValue.forecast) {
      dateEffective.value.id = dateReprog.value.dateId = newValue.id;
      dateEffective.value.forecast = newValue.forecast;
    }
  },
  { immediate: true }
);
watch(
  () => props.father,
  (newValue, oldValue) => {
    if (newValue && newValue.id) {

    }
  },
  { immediate: true }
);
</script>

<script>
import mutationDateUpdate from "~/queries/putDateUpdates.gql";
import mutationNonCompliance from "~/queries/putNonCompliance.gql";
import mutationDate from "~/queries/putDate.gql";
import mutationAudit from "~/queries/putAudit.gql";

import queryAudit from "~/queries/audit.gql";

export default {
  data: () => ({
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
    getMaxIdObject(dateUpdate) {
      if (!dateUpdate || dateUpdate.length === 0) {
        return { newDate: null };
      }

      return dateUpdate.reduce((prev, current) =>
        prev.id > current.id ? prev : current
      );
    },
    disableDate(ts) {
      return ts < Date.now();
    },
    disablePastDate(ts) {
      return ts > Date.now();
    },
    formatDate(dateString) {
      const dateObject = dateString
        ? new Date(dateString + "T00:00:00Z")
        : null;

      return dateObject
        ? this.$options.filters.dateFormat(
            new Date(dateObject.setDate(dateObject.getDate() + 1)),
            "dd-MM-yyyy"
          )
        : "";
    },
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
