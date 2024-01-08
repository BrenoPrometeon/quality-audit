<template>
  <!-- STATUS NAO CONFORMIDADES -->
  <div data-aos="fade-up" data-aos-duration="800">
    <!-- NEW BUTTON -->
    <v-row justify="center" class="ma-1"
      ><v-col class="text-end">
        <!-- CAIXA DE CRIAÇÃO DE NÃO CONFORMIDADE -->
        <v-dialog max-width="500">
          <template v-slot:activator="{ props }">
            <v-btn
              color="success"
              width="200"
              v-bind="props"
              :loading="createDateLoading"
              >Novo</v-btn
            >
          </template>
          <template v-slot:default="{ isActive }">
            <v-card>
              {{ dateNonCompliance }}
              <v-card-title class="text-center">Não Conformidade</v-card-title>
              <v-card-text>
                <v-row justify="center" class="text-center">
                  <v-col cols="8">
                    <div class="text-overline">prioridade</div>
                    <!-- SELECIONAR AREA -->
                    <v-select
                      v-model="dateNonCompliance.priorityId"
                      :items="prioritiesRaw?.prioritiess"
                      variant="outlined"
                      item-value="id"
                      item-title="description"
                      label="Escolha uma prioridade"
                    ></v-select>
                    <div class="text-overline">descrição</div>
                    <!-- SELECIONAR TURNO -->
                    <v-textarea
                      v-model="dateNonCompliance.description"
                      variant="outlined"
                      placeholder="Descrição da Não Conformidade"
                    ></v-textarea>
                  </v-col>
                </v-row>
              </v-card-text>
              <!-- SAVE BUTTON -->
              <v-card-actions class="end__card__save">
                <v-row justify="end" class="mx-3">
                  <v-btn color="red" @click="isActive.value = false"
                    >Cancelar</v-btn
                  >
                  <v-btn
                    color="white"
                    @click="
                      newCompliance();
                      isActive.value = false;
                    "
                    >Salvar</v-btn
                  ></v-row
                >
              </v-card-actions>
            </v-card>
          </template>
        </v-dialog>
      </v-col></v-row
    >

    <!-- DATA TABLE AND TIMELINE -->
    <v-row justify="center"
      ><v-col class="text-center">
        <!-- DATA TABLE -->

        <p-data-table
          :columns="columnsCompliance"
          :data="dataCompliance?.length ? dataCompliance : []"
          :id="['id']"
          :height="false"
          :loading="nonComplianceTable"
          selectable
          v-model="rowCompliance"
        >
        </p-data-table> </v-col
    ></v-row>

    <!-- TIMELINE -->
    <div
      v-if="rowCompliance"
      class="d-flex flex-column justify-center align-center"
    >
      <v-card variant="tonal" width="50vw" class="my-3">
        <v-card-title class="text-center">Descrição</v-card-title>
        <v-row justify="center" class="pa-3"
          ><v-col class="text-center"
            ><v-divider class="mb-2"></v-divider>{{ dataCompliance?.find(item => item.id == rowCompliance).description }}</v-col
          ></v-row
        >
      </v-card>

      <v-timeline align="start" data-aos="fade-up" data-aos-duration="1000">
        <v-timeline-item
          v-for="(item, i) in timelineItems"
          :key="i"
          :dot-color="i < stepCompliance ? 'green' : 'primary'"
          :icon="item.icon"
          fill-dot
        >
          <!-- CONTEUDO TIMELINE DE CADA ITEM -->
          <template v-slot:opposite v-if="i <= 1"
            ><OppositiveCard
              :stepCompliance="stepCompliance"
              :i="i"
              :item="item"
          /></template>
          <v-card elevation="8" :disabled="!(i == stepCompliance)">
            <v-card
              :loading="nonComplianceTable"
              rounded="0"
              :class="['text-h6', 'timeline', 'text-center', 'pa-2']"
              >{{ item.title }}</v-card
            >
            <q-date-picker
              @refresh-fields="refetch()"
              session="nonCompliance"
              :father="father"
              :children="getNextChildField(i)"
              :customField="getNextCustomField(i)"
            />
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </div>
  </div>
</template>
<script setup>
const props = defineProps({
  audit: { required: true },
});

const dataCompliance = ref([]);
const dateNonCompliance = ref({});
const dateNewField = ref({});
const rowCompliance = ref(null);
const father = ref(null);
const stepCompliance = ref(0);

const {
  loading: nonComplianceTable,
  onResult,
  refetch,
} = useQuery(queryNonCompliance);

onResult(({ data }) => {
  const filteredData = data?.noncompliances.filter(
    (item) => item.auditId === props.audit?.id
  );
  dataCompliance.value = filteredData;
});

const { result: prioritiesRaw, loading: prioritiesLoading } =
  useQuery(queryPriority);

const {
  mutate: nonComplianceDate,
  loading: nonComplianceloading,
  onDone: nonComplianceOnDone,
} = useMutation(mutationNonCompliance, {
  refetchQueries: [{ query: queryNonCompliance }],
  variables: dateNonCompliance.value
});

nonComplianceOnDone(({data})=>{
  message.info('Não conformidade criada!')
})

const {
  mutate: createDate,
  loading: createDateLoading,
  onDone: createDateOnDone,
} = useMutation(mutationDate, {
  variables: dateNewField.value,
});

const getNextChildField = (index) => {
  const childFields = ["dateActionPlan", "dateDeployment", "dateValidation"];
  return father?.value[childFields[index]] || "";
};

const getNextCustomField = (index) => {
  const customFields = [
    { title: "Implementação", value: "deployment" },
    { title: "Verificação de Eficácia", value: "validation" },
    {},
  ];
  return customFields[index];
};

function obterDataHojeFormatada() {
  const data = new Date();
  const dia = adicionarZero(data.getDate());
  const mes = adicionarZero(data.getMonth() + 1);
  const ano = data.getFullYear();
  const formatadaComum = `${dia}/${mes}/${ano}`;
  const formatadaName = `${ano}${dia}${mes}`;
  return [formatadaComum, formatadaName];
}

function adicionarZero(numero) {
  return numero < 10 ? `0${numero}` : numero;
}


function somarDias(dataString, days) {
  const data = new Date(dataString);
  data.setDate(data.getDate() + days);
  const diaNovo = String(data.getDate()).padStart(2, "0");
  const mesNovo = String(data.getMonth() + 1).padStart(2, "0");
  const anoNovo = data.getFullYear();
  return `${anoNovo}-${mesNovo}-${diaNovo}`;
}

function newCompliance() {
  let pt = prioritiesRaw.value?.prioritiess.find(
    item => item.id == dateNonCompliance.value.priorityId
  ).description;

  const dataFormatada = obterDataHojeFormatada();

  let name = `${dataFormatada[1]}#${props.audit?.id}${pt}`;
  dateNonCompliance.value["identifier"] = name;

  let forecastDays = dateNonCompliance.value.priorityId === 2 ? 20 : 60;
  dateNewField.value["forecast"] = somarDias(
    props.audit.reportDate.effective,
    forecastDays
  );
  
  createDate();
}
createDateOnDone(({ data }) => {
  dateNonCompliance.value["actionPlan"] = data.putDate.id;
  nonComplianceDate();
});

function updateFatherFromRowCompliance() {
  if (rowCompliance.value) {
    const selectedObject = dataCompliance.value.find(
      (item) => String(item.id) === String(rowCompliance.value)
    );
    father.value = selectedObject;
  }
}

watch(
  () => rowCompliance.value,
  () => {
    updateFatherFromRowCompliance();
  }
);

watch(
  () => dataCompliance.value,
  () => {
    updateFatherFromRowCompliance();
  }
);
watch(
  () => father.value,
  (newValue, oldValue) => {
    if (newValue.dateValidation?.effective) stepCompliance.value = 3;
    else if (newValue.dateDeployment?.effective) stepCompliance.value = 2;
    else if (newValue.dateActionPlan?.effective) stepCompliance.value = 1;
    else stepCompliance.value = 0;
  }
);

watch(
  () => props.audit,
  (newValue, oldValue) => {
    if (newValue && newValue.id && newValue.reportDate) {
      dateNonCompliance.value.auditId = newValue.id;
    }
  },
  { immediate: true }
);
</script>
<script>
import mutationNonCompliance from "~/queries/putNonCompliance.gql";
import mutationDate from "~/queries/putDate.gql";

import queryNonCompliance from "~/queries/nonCompliance.gql";
import queryPriority from "~/queries/priorities.gql";

export default {
  data: () => ({
    columnsCompliance: [
      {
        title: "Identificador",
        key: "identifier",
      },
      {
        title: "Descrição",
        key: "description",
      },
    ],
    timelineItems: [
      {
        title: "Plano de Ação",
        textOppositive: "Seleção de Líder e Monitor",
        icon: "mdi-note",
        value: "action",
      },
      {
        title: "Implementação",
        icon: "mdi-arrow-up-bold-outline",
        textOppositive: "Seleção dos Responsáveis",
        value: "deploy",
      },
      {
        title: "Verificação da Eficácia",
        icon: "mdi-layers-triple",
        value: "validation",
      },
    ],
  }),
  methods: {},
};
</script>
<style scoped>
.end__card__save {
  background-color: #212b59;
  margin-top: 0.3rem;
}

.timeline {
  background-color: #212b59;
  color: white;
}
</style>
