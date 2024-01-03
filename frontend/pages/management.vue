<template>
  <v-card>
    <div class="d-flex flex-row">
      <!-- TABS LATERAIS -->
      <v-tabs v-model="audit" color="primary" direction="vertical">
        <p class="text-center text-overline ma-2 audit__p">Auditorias</p>
        <v-divider class="mx-4"></v-divider>
        <v-tab
          v-for="n in auditsRaw?.audits"
          :key="n.id"
          :value="n"
          :style="{ 'max-width': '15vw' }"
        >
          {{ n.process?.description }}
        </v-tab>
        <v-row justify="center"
          ><v-col class="text-center">
            <!-- CAIXA DE CRIAÇÃO DE AUDITORIA -->
            <v-dialog persistent max-width="800">
              <template v-slot:activator="{ props }">
                <v-btn
                  :loading="auditLoading"
                  variant="text"
                  icon="mdi-plus"
                  class="text-center"
                  color="primary"
                  v-bind="props"
                >
                </v-btn>
              </template>
              <template v-slot:default="{ isActive }">
                <v-card>
                  <v-card-title class="text-center">Auditoria</v-card-title>
                  <v-card-text>
                    <v-row justify="center" class="align-center">
                      <v-col cols="6" class="d-flex flex-column align-center">
                        <div class="text-overline">Áreas</div>
                        <!-- SELECIONAR AREA -->
                        <v-select
                          v-model="newAudit.processId"
                          :items="processRaw?.processs"
                          item-title="description"
                          item-value="id"
                          variant="outlined"
                          label="Escolha uma área"
                          class="select__box"
                        ></v-select>
                        <div class="text-overline">Turno</div>
                        <!-- SELECIONAR TURNO -->
                        <v-select
                          v-model="newAudit.shifts"
                          :disabled="!newAudit.processId"
                          :items="shiftRaw?.shifts"
                          multiple
                          item-title="description"
                          item-value="id"
                          variant="outlined"
                          label="Escolha uma turno"
                          class="select__box"
                        ></v-select> </v-col
                      ><v-divider vertical></v-divider>
                      <!-- DATE PICKER -->
                      <v-col cols="6" class="text-center"
                        ><v-card
                          :disabled="
                            newAudit.shifts ? !newAudit.shifts.length > 0 : true
                          "
                          variant="flat"
                          ><v-row justify="center"
                            ><v-col cols="auto" class="text-center"
                              ><n-date-picker
                                panel
                                type="date"
                                clearable
                                format="dd/MM/yyyy"
                                value-format="yyyy-MM-dd"
                                v-model:formatted-value="newAudit.forecast"
                                class="text-center date__picker" /></v-col></v-row></v-card
                      ></v-col>
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
                        :disabled="
                          newAudit.shifts
                            ? newAudit.shifts.length > 0
                              ? !newAudit.forecast
                              : true
                            : true
                        "
                        @click="
                          insertAudit();
                          isActive.value = false;
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
      </v-tabs>
      <!-- CONTEUDO DE CADA AUDITORIA -->

      <v-card
        flat
        width="100vw"
        class="card__content"
        rounded="0"
        :disabled="!audit.id"
      >
        <!-- STEPS DA SITUAÇÃO ATUAL DA AUDITORIA -->
        <v-stepper rounded="0" :model-value="stepper" flat>
          <v-stepper-header>
            <v-stepper-item
              :complete="stepper > 0 ? true : false"
              :color="stepper > 0 ? 'green' : ''"
              title="Não iniciada"
              :value="0"
            ></v-stepper-item>

            <v-divider></v-divider>

            <v-stepper-item
              :complete="stepper > 1 ? true : false"
              :color="stepper > 1 ? 'green' : ''"
              title="Aguardando o relatório"
              :value="1"
            ></v-stepper-item>

            <v-divider></v-divider>

            <v-stepper-item
              title="Concluído"
              :value="2"
              :complete="stepper > 2 ? true : false"
              :color="stepper > 2 ? 'green' : ''"
            ></v-stepper-item>
          </v-stepper-header>
        </v-stepper>

        <!-- CONTEUDO  -->

        <v-card-text>
          <!-- DATA PREVISTA -->
          <v-row justify="center" class="mb-3"
            ><v-col cols="6">
              <q-date-picker
                @date-completed="refetchAudit()"
                session="audit"
                :father="audit"
                :children="audit.dateEnd"
                :customField="{ title: 'Relatório', value: 'reportDateId' }"
              ></q-date-picker>
            </v-col>

            <v-divider></v-divider>
          </v-row>

          <v-card>
            <!-- TABS RELATÓRIO E NÃO CONFORMIDADES -->

            <v-tabs v-model="tabAuditView" bg-color="primary" grow>
              <v-tab
                v-for="n in tabContent"
                :key="n"
                :value="n.value"
                :disabled="n.value == 1 && !audit.reportDate?.effective"
              >
                {{ n.name }}
              </v-tab>
            </v-tabs>
            <div class="pa-2" v-if="tabAuditView == 0">
              <!-- STATUS RELATÓRIO -->
              <v-row
                data-aos="fade-up"
                data-aos-duration="800"
                justify="space-around"
                class="ma-3 align-center"
                ><v-col cols="5" class="text-center text-h6"
                  ><v-progress-circular
                    size="250"
                    width="25"
                    :model-value="
                      audit.reportDate?.effective ? 100 : daysRemaining * 10
                    "
                    :color="audit.reportDate ? 'green-darken-4' : '#000'"
                    :bg-color="
                      daysRemaining == 0
                        ? 'yellow-accent-4'
                        : daysRemaining < 0
                        ? '#000'
                        : audit.reportDate
                        ? 'red-accent-4'
                        : '#000'
                    "
                  >
                    <v-row v-if="audit.reportDate"
                      ><v-col class="progress"
                        ><div v-if="audit.reportDate?.effective">Concluído</div>
                        <div v-else-if="daysRemaining >= 0">
                          Faltam: <br />
                          {{ daysRemaining }} dias
                        </div>
                        <div v-else>
                          Prazo <br />
                          Esgotado
                        </div>
                      </v-col></v-row
                    >
                  </v-progress-circular> </v-col
                ><v-divider :thickness="3" vertical></v-divider
                ><v-col cols="5">
                  <q-date-picker
                    @date-completed="refetchAudit()"
                    session="audit"
                    :father="audit"
                    :children="audit.reportDate ? audit.reportDate : null"
                  ></q-date-picker>
                </v-col>
              </v-row>
            </div>

            <!-- STATUS NAO CONFORMIDADES -->
            <div
              v-if="tabAuditView == 1"
              data-aos="fade-up"
              data-aos-duration="800" 
              class="ma-3"
            >
              <nonCompliance
                :audit="audit"
              />
            </div>
          </v-card> </v-card-text
      ></v-card>
    </div>
  </v-card>
</template>
<script setup>
const {
  result: auditsRaw,
  loading: auditLoading,
  refetch: refetchAudit,
} = useQuery(queryAudit, { pollInterval: 500 });
const { result: processRaw, loading: processLoading } = useQuery(queryProcess);
const { result: shiftRaw, loading: shiftLoading } = useQuery(queryShift);

const newAudit = ref({});
const {
  mutate: insertAudit,
  loading,
  onDone,
} = useMutation(addAudit, {
  refetchQueries: [{ query: queryAudit }],
  variables: newAudit.value,
});
onDone((data) => {
  message.info("Auditoria Criada!");
});
</script>
<script>
import queryProcess from "~/queries/process.gql";
import queryShift from "~/queries/shift.gql";
import queryAudit from "~/queries/audit.gql";

import addAudit from "~/queries/addAudit.gql";

import AOS from "aos";
import "aos/dist/aos.css";
AOS.init({ once: true });
export default {
  setup() {},
  data: () => ({
    stepper: 0,
    daysRemaining: null,
    audit: {},
    tabContent: [
      {
        name: "Relatório",
        value: 0,
      },
      {
        name: "Não conformidades",
        value: 1,
      },
    ],
    tabAuditView: null,
  }),

  methods: {
    countdown(data) {
      if (data) {
        const partesData = data.split("-");
        const dataOriginal = new Date(
          partesData[0],
          partesData[1] - 1,
          partesData[2]
        );

        const dataAtual = new Date();

        const diferencaEmMilissegundos = dataOriginal - dataAtual;

        const diferencaEmDias = Math.ceil(
          diferencaEmMilissegundos / (1000 * 60 * 60 * 24)
        );

        return diferencaEmDias;
      }
    },
    getMaxIdObject(dateUpdate) {
      if (!dateUpdate || dateUpdate.length === 0) {
        return { newDate: null };
      }

      return dateUpdate.reduce((prev, current) =>
        prev.id > current.id ? prev : current
      );
    },

    clear() {
      this.daysRemaining = null;
      this.stepper = 0;
      this.tabAuditView = 0;
    },
  },
  watch: {
    audits(val) {
      this.tab = val - 1;
    },
    audit: {
      handler(newAudit, oldAudit) {
        this.clear();
        let dateCountdown;
        if (newAudit.reportDate?.forecast) {
          if (
            newAudit.reportDate.dateUpdates &&
            newAudit.reportDate.dateUpdates.length > 0
          ) {
            dateCountdown = this.getMaxIdObject(
              newAudit.reportDate.dateUpdates
            ).newDate;
          } else {
            dateCountdown = newAudit.reportDate.forecast;
          }
          this.daysRemaining = this.countdown(dateCountdown);
        }
      },
      deep: true,
    },
  },
};
</script>
<style scoped>
.selected-comment {
  background-color: #cfd8dc !important;
}

.progress {
  color: #000;
}
.date__picker {
  border: 1px solid #000;
}

.select__box {
  width: 300px;
}

.end__card__save {
  background-color: #212b59;
  margin-top: 0.3rem;
}
.title__report {
  text-transform: uppercase;
}

.box {
  background-color: #f5f5f5;
  padding: 1rem;
  border: 1px solid #212b59;
  border-radius: 5px;
}

.box:hover {
  cursor: pointer;
}

.card__content {
  border-left: 1px solid #949393;
}

.timeline {
  background-color: #212b59;
  color: white;
}

.timeline__opossitive {
  background-color: #59a2b5;
  color: white;
}

.card__plan {
  border: 1px solid #797979;
  border-radius: 5px;
}

#fixed-div {
  position: fixed;
  bottom: 0;
  width: 38vw;
  padding: 10px;
  box-sizing: border-box;
  background-color: #fff;
}

#comments__container {
  max-height: calc(100vh - 180px);
  overflow-y: auto;
  padding: 10px;
  box-sizing: border-box;
  position: relative;
}

.audit__p {
  color: #212b59;
}
</style>
