<template>
  <v-card>
    <div class="d-flex flex-row">
      <!-- TABS LATERAIS -->

      <v-tabs v-model="audit" color="#212b59" direction="vertical">
        <v-tab
          v-for="n in audits"
          :key="n.mpDate ? n.mpDate : n.prevDate"
          :value="n"
        >
          {{ n.name }}
        </v-tab>
        <v-row justify="center"
          ><v-col class="text-center"
            ><v-btn
              variant="text"
              @click="openBox()"
              icon="mdi-plus"
              class="text-center"
              color="#212b59"
            >
            </v-btn></v-col
        ></v-row>
      </v-tabs>

      <!-- CONTEUDO DE CADA AUDITORIA -->

      <v-card flat width="100vw" class="card__content" rounded="0">
        <!-- STEPS DA SITUAÇÃO ATUAL DA AUDITORIA -->

        <v-stepper rounded="0" :model-value="stepper">
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
          <!-- DATA MP -->

          <v-row justify="space-around" class="my-3"
            ><v-col
              cols="3"
              class="d-flex justify-center flex-columns align-center text-center"
              ><v-card class="pa-10" elevation="14"
                ><p class="text-h6 font-weight-bold">Master Plan</p>
                <v-divider></v-divider
                ><n-statistic :value="audit.mpDate" class="text-center">
                  <template #prefix
                    ><v-icon
                      v-if="!audit.mpDate"
                      icon="mdi-calendar-alert"
                    ></v-icon></template></n-statistic></v-card
            ></v-col>

            <v-divider vertical></v-divider>

            <!-- DATE PICKER AND BUTTONS -->
            <v-col
              ><v-row justify="center"
                ><v-col cols="12">
                  <v-row
                    justify="center"
                    v-for="type in [{ text: 'Data', value: 'Date' }]"
                    class="mx-10"
                  >
                    <v-col cols="12" class="text-center text-overline">{{
                      type.text
                    }}</v-col>
                    <v-col
                      class="text-overline text-center"
                      cols="4"
                      v-for="d in [
                        { title: 'Previsão', value: 'prev' },
                        { title: 'Efetivo', value: 'effective' },
                      ]"
                      ><v-row justify="center"> {{ d.title }}</v-row
                      ><v-row justify="center"
                        ><v-col class="text-h6"
                          ><n-date-picker
                            v-model:formatted-value="
                              auditDates[d['value'] + type.value]
                            "
                            type="date"
                            value-format="dd/MM/yyyy"
                            size="large"
                            clearable
                            placeholder="Selecione uma data" /></v-col
                      ></v-row>
                    </v-col>
                  </v-row>
                </v-col>
                <v-col class="text-center"
                  ><v-btn
                    color="orange"
                    class="mr-3"
                    @click="reprogram()"
                    :disabled="audit.prevDate == auditDates.prevDate"
                    >Reprogramar</v-btn
                  ><v-btn
                    color="green"
                    class="ml-3"
                    :disabled="
                      !auditDates.effectiveDate ||
                      audit.effectiveDate == auditDates.effectiveDate
                    "
                    @click="finishAudit()"
                    >Concluir</v-btn
                  ></v-col
                ></v-row
              ></v-col
            >
          </v-row>

          <v-card elevation="4">
            <!-- TABS RELATÓRIO E NÃO CONFORMIDADES -->

            <v-tabs v-model="tabAuditView" bg-color="#212b59" grow>
              <v-tab v-for="n in tabContent" :key="n" :value="n.value">
                {{ n.name }}
              </v-tab>
            </v-tabs>
            <div class="pa-2">
              <!-- STATUS RELATÓRIO -->
              <v-row
                v-if="tabAuditView == 0"
                justify="space-around"
                class="ma-3"
                ><v-col cols="5" class="text-center text-h6"
                  ><v-progress-circular
                    size="200"
                    width="23"
                    :model-value="reportFinished ? 100 : daysRemaining * 10"
                    color="green-darken-4"
                    :bg-color="
                      daysRemaining == 0
                        ? 'yellow-accent-4'
                        : daysRemaining < 0
                        ? '#000'
                        : audit.effectiveDate
                        ? 'red-accent-4'
                        : '#000'
                    "
                  >
                    <v-row v-if="audit.effectiveDate"
                      ><v-col class="progress"
                        ><div v-if="reportFinished">Concluído</div>
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
                  <v-row justify="center">
                    <v-col cols="12" class="text-center"
                      ><n-statistic
                        label="Previsão máxima para entrega"
                        :value="dateReport"
                        class="text-center my-6"
                      >
                        <template #prefix
                          ><v-icon
                            v-if="!audit.effectiveDate"
                            icon="mdi-calendar-alert"
                          ></v-icon>
                        </template> </n-statistic
                    ></v-col>
                    <v-col cols="12" class="pa-0 text-center"
                      ><v-icon
                        size="large"
                        :icon="`mdi-${iconReport.icon}`"
                        :color="iconReport.color"
                      ></v-icon
                    ></v-col>
                    <v-col cols="12" class="text-center"
                      ><v-btn color="green" @click="reportSubmitted()"
                        >Entregar relatório</v-btn
                      ></v-col
                    ></v-row
                  ></v-col
                ></v-row
              >

              <!-- STATUS NAO CONFORMIDADES -->
              <div v-if="tabAuditView == 1">
                <!-- NEW BUTTON -->
                <v-row justify="center" class="ma-1"
                  ><v-col class="text-end"
                    ><v-btn
                      :color="btnNewCompliance.color"
                      width="200"
                      @click="newCompliance()"
                      >{{ btnNewCompliance.text }}</v-btn
                    ></v-col
                  ></v-row
                >

                <!-- DATA TABLE AND TIMELINE -->
                <v-row justify="center"
                  ><v-col class="text-center">
                    <!-- DATA TABLE -->

                    <p-data-table
                      :columns="columnsCompliance"
                      :data="dataCompliance"
                      :id="['id']"
                      :height="false"
                      selectable
                      v-model="rowCompliance"
                    >
                    </p-data-table></v-col
                ></v-row>

                <!-- TIMELINE -->

                <v-timeline align="start" v-if="rowCompliance">
                  <v-timeline-item
                    v-for="(item, i) in timelineItems"
                    :key="i"
                    dot-color="#212b59"
                    :icon="item.icon"
                    fill-dot
                  >
                    <!-- CONTEUDO TIMELINE DE CADA ITEM -->

                    <v-card>
                      <v-card
                        rounded="0"
                        :class="['text-h6', 'timeline', 'text-center', 'pa-2']"
                      >
                        {{ item.title }}
                      </v-card>
                      <v-card-text class="bg-white text--primary">
                        <p>...</p>
                        <v-btn color="item.color" variant="outlined">
                          Ok
                        </v-btn>
                      </v-card-text>
                    </v-card>
                  </v-timeline-item>
                </v-timeline>

                <!-- COMMENTS -->
                <v-row justify="center"
                  ><v-divider
                    :thickness="2"
                    class="mt-4 mx-8"
                    color="#212b59"
                  ></v-divider
                  ><v-col class="text-center ma-3"
                    ><v-btn
                      :disabled="!rowCompliance"
                      color="#E8EAF6"
                      @click="showDrawer = true"
                      append-icon="mdi-message"
                    >
                      Comentários</v-btn
                    >
                    <n-drawer
                      v-model:show="showDrawer"
                      :width="600"
                      height="500"
                    >
                      <n-drawer-content
                        title="Comentários"
                        :native-scrollbar="false"
                        closable
                        trigger="none"
                      >
                        <n-grid :y-gap="8" :cols="1">
                          <n-grid-item v-for="item in comments">
                            <div
                              class="box text-center d-flex justify-center align-center"
                            >
                              <v-row justify="center"
                                ><v-col
                                  cols="6"
                                  class="text-start font-weight-black"
                                  >{{ item.name }}</v-col
                                ><v-col cols="6" class="text-end font-italic">{{
                                  item.date
                                }}</v-col>
                                <v-divider class="mx-3"></v-divider>
                                <v-col>{{ item.comment }}</v-col>
                              </v-row>
                            </div>
                          </n-grid-item>
                        </n-grid>
                      </n-drawer-content>
                    </n-drawer></v-col
                  ></v-row
                >
              </div>
            </div>
          </v-card>

          <!-- BUTTON DE CONCLUSÃO DE AUDITORIA -->

          <!-- <v-row justify="center" class="mt-0"
            ><v-col class="text-center"
              ><v-btn color="green" @click="completedAudit()"
                >Concluir</v-btn
              ></v-col
            ></v-row
          > -->
        </v-card-text></v-card
      >
    </div>

    <!-- CREATE BOX -->

    <v-dialog v-model="showBox" max-width="800">
      <v-card>
        <v-card-title class="text-center">Auditoria</v-card-title>
        <v-card-text>
          <v-row justify="center" class="align-center">
            <v-col cols="6" class="d-flex flex-column align-center">
              <div class="text-overline">Áreas</div>
              <!-- SELECIONAR AREA -->
              <v-select
                v-model="auditDialog.name"
                :items="areas"
                variant="outlined"
                label="Escolha uma área"
                class="select__box"
              ></v-select>
              <div class="text-overline">Turno</div>
              <!-- SELECIONAR TURNO -->
              <v-select
                v-model="auditDialog.shift"
                :items="shifts"
                variant="outlined"
                label="Escolha uma turno"
                class="select__box"
              ></v-select>
              <!-- MASTER PLAN -->
              <v-checkbox
                v-model="masterPlan"
                label="Master Plan"
                color="green-darken-2"
                :value="true"
              ></v-checkbox></v-col
            ><v-divider vertical></v-divider>
            <!-- DATE PICKER -->
            <v-col cols="6" class="text-center"
              ><v-row justify="center"
                ><n-date-picker
                  panel
                  type="date"
                  value-format="dd/MM/yyyy"
                  v-model:formatted-value="pickerDate"
                  class="text-center date__picker" /></v-row
            ></v-col>
          </v-row>
        </v-card-text>
        <!-- SAVE BUTTON -->
        <v-card-actions class="end__card__save">
          <v-row justify="end" class="mx-3"
            ><v-btn color="white" @click="saveAudit()">Salvar</v-btn></v-row
          >
        </v-card-actions>
      </v-card>
    </v-dialog>
    {{ auditDates }}
    {{ audit }}
  </v-card>
</template>
<script>
export default {
  data: () => ({
    reportFinished: false,
    stepper: 0,
    dateReport: null,
    daysRemaining: null,
    showBox: false,
    showDrawer: false,
    masterPlan: false,
    pickerDate: null,
    auditDates: {},
    auditDialog: {},
    audits: [
      {
        name: "Procurement",
        value: "4",
        mpDate: "25/12/2021",
        description: "",
      },
      {
        name: "Production Planning",
        value: "5",
        mpDate: "03/09/2023",
        description: "",
      },
      {
        name: "QMS",
        value: "6",
        mpDate: "08/11/2022",
        description: "",
      },
    ],
    timelineItems: [
      {
        title: "Plano de Ação",
        color: "#212b59",
        icon: "mdi-note",
      },
      {
        title: "Implementação",
        color: "indigo-darken-2",
        icon: "mdi-arrow-up-bold-outline",
      },
      {
        title: "Evidência Entregue",
        color: "indigo-lighten-1",
        icon: "mdi-magnify",
      },
      {
        title: "Verificação da Eficácia",
        color: "indigo-lighten-3",
        icon: "mdi-layers-triple",
      },
    ],
    areas: [
      "OE Sales",
      "PMS",
      "Procurement",
      "QMS",
      "ICT",
      "Production Planning",
    ],
    columnsCompliance: [
      {
        title: "ID",
        key: "id",
      },
      {
        title: "Auditoria",
        key: "audit",
      },
      {
        title: "Data",
        key: "date",
      },
    ],
    dataCompliance: [
      { id: 3, audit: "Indoor", length: "4:18", date: 1 },
      { id: 4, audit: "Vulcanização", length: "4:48", date: 2 },
      { id: 12, audit: "R&D", length: "7:27", date: 3 },
    ],
    rowCompliance: null,
    shifts: ["1", "2", "3", "Administrativo"],
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
    tabAuditView: {},
    btnNewCompliance: {
      color: "green",
      text: "Novo",
    },
    comments: [
      {
        name: "Maria Juliani Carminatti, BR",
        comment:
          "Lembrete: O prazo para envio do plano de ação vencerá em 2 dias.",
        date: "October 11, 2023 4:00 PM",
      },
      {
        name: "Maria Juliani Carminatti, BR",
        comment:
          "Task '20230815 #01Minor' assigned to Elias Jamile, BR, Maria Juliani Carminatti, BR, Bracesco Fabiana Alves, BR, Horn Sergio Ricardo, BR, Pacini Rodrigo Gomes (STAG), BR",
        date: "August 22, 2023 2:04 PM",
      },
    ],
    iconReport: {},
  }),

  methods: {
    openBox() {
      this.showBox = true;
    },
    saveAudit() {
      if (this.masterPlan) this.auditDialog["mpDate"] = this.pickerDate;
      else this.auditDialog["prevDate"] = this.pickerDate;
      this.audits.push(this.auditDialog);
      this.auditDialog = {};
      this.showBox = false;
    },
    newCompliance() {
      this.btnNewCompliance.color =
        this.btnNewCompliance.color === "red" ? "green" : "red";

      this.btnNewCompliance.text =
        this.btnNewCompliance.text === "Novo" ? "Cancelar" : "Novo";
    },
    countdown(data) {
      const dataString = data;

      function converterStringParaData(dataString) {
        const partesData = dataString.split("/");

        return new Date(partesData[2], partesData[1] - 1, partesData[0]);
      }

      const dataOriginal = converterStringParaData(dataString);

      const dataCom10Dias = new Date(dataOriginal);
      dataCom10Dias.setDate(dataOriginal.getDate() + 10);

      function formatarData(dataString) {
        const data = new Date(dataString);

        const dia = String(data.getDate()).padStart(2, "0");
        const mes = String(data.getMonth() + 1).padStart(2, "0");
        const ano = data.getFullYear();

        const dataFormatada = `${dia}/${mes}/${ano}`;

        return dataFormatada;
      }
      this.dateReport = formatarData(dataCom10Dias);

      const dataAtual = new Date();

      const diferencaEmMilissegundos = dataCom10Dias - dataAtual;
      const diferencaEmDias = Math.ceil(
        diferencaEmMilissegundos / (1000 * 60 * 60 * 24)
      );

      return diferencaEmDias;
    },
    reprogram() {
      this.audit = { ...this.audit, ...this.auditDates };
    },
    finishAudit() {
      this.audit = { ...this.audit, ...this.auditDates };
      this.daysRemaining = this.countdown(this.auditDates.effectiveDate);
      this.iconReport.icon = "clock-time-eight-outline";
      this.iconReport.color = "black";
      this.stepper = 1;
    },
    reportSubmitted() {
      this.iconReport.color = "green";
      this.iconReport.icon = "check-decagram-outline";
      this.stepper = 2;
      this.reportFinished = true;
    },
    completedAudit() {
      this.stepper = 3;
    },
  },

  computed: {},

  watch: {
    audits(val) {
      this.tab = val - 1;
    },
    // audit() {
    //   if (this.audit.prevDate) {
    //     this.auditDates.prevDate = this.audit.prevDate;
    //   }
    // },
    audit: {
      handler(newAudit, oldAudit) {
        for (const key in newAudit) {
          if (newAudit[key] !== oldAudit[key]) {
            if (key === "name"){
              this.reportFinished = false;
              this.daysRemaining = null;
              this.stepper = 0;
              this.dateReport = null;
              
              if(this.audit.prevDate) this.auditDates = { prevDate: this.audit.prevDate};
              else this.auditDates = {prevDate: null}

              if(this.audit.effectiveDate) this.auditDates = { effectiveDate: this.audit.effectiveDate};
              else this.auditDates.effectiveDate = null;
            } 
          }
        }
      },
      deep: true,
    },
    auditDates() {
      if (this.auditDates.effectiveDate) {
      }
    },
    auditDialog() {
      if (this.auditDialog.mp) {
        this.auditDates.mpDate = this.auditDialog.mp;
      }
    },
    showBox() {
      if (!this.showBox) this.masterPlan = false;
    },
  },
};
</script>
<style scoped>
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
  margin-top: 1rem;
}
.title__report {
  text-transform: uppercase;
}

.box {
  background-color: #f5f5f5;
  padding: 1rem;
  border: 1px solid #212b59;
}

.card__content {
  border-left: 1px solid #949393;
}

.timeline {
  background-color: #212b59;
  color: white;
}
</style>
