<template>
  <v-card>
    <div class="d-flex flex-row">
      <!-- TABS LATERAIS -->

      <v-tabs v-model="audit" color="primary" direction="vertical">
        <p class="text-center text-overline ma-2 audit__p">Auditorias</p>
        <v-divider class="mx-4"></v-divider>
        <v-tab
          v-for="n in audits"
          :key="n.id"
          :value="n"
          :style="{ 'max-width': '15vw' }"
        >
        {{ getProcessDescription(n.processId) }}
        </v-tab>
        {{ audit }}
        <v-row justify="center"
          ><v-col class="text-center"
            ><v-btn
              variant="text"
              @click="openBoxAudit()"
              icon="mdi-plus"
              class="text-center"
              color="primary"
            >
            </v-btn></v-col
        ></v-row>
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
              :color="stepper > 1 ? (reportFinished ? 'green' : '') : ''"
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

          <v-row justify="center" class="my-3"
            ><v-col cols="6">
              <q-date-picker></q-date-picker>
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
                :disabled="n.value == 1 && !reportFinished"
              >
                {{ n.name }}
              </v-tab>
            </v-tabs>
            <div class="pa-2">
              <!-- STATUS RELATÓRIO -->
              <v-row
                v-if="tabAuditView == 0"
                data-aos="fade-up"
                data-aos-duration="800"
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
                            v-if="!dateReport"
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
                    <v-col v-if="stepper < 2" cols="12" class="text-center"
                      ><v-btn
                        :disabled="!dateReport"
                        color="#b55921"
                        class="mr-3"
                        @click="reportSubmitted('reprog')"
                        >Reprogramar</v-btn
                      ><v-btn
                        color="green"
                        :disabled="
                          !this.audit.effectiveDate || this.reportFinished
                        "
                        @click="reportSubmitted('send')"
                        >Entregar</v-btn
                      ></v-col
                    ><v-col v-else cols="12" class="text-center"
                      ><n-statistic
                        label="Data final da entrega"
                        :value="dateReportReceive"
                        class="text-center my-6"
                      >
                      </n-statistic></v-col></v-row></v-col
              ></v-row>

              <!-- STATUS NAO CONFORMIDADES -->
              <div
                v-if="tabAuditView == 1"
                data-aos="fade-up"
                data-aos-duration="800"
              >
                <nonCompliance
                  :stepCompliance="stepCompliance"
                  :reportFinished="reportFinished"
                  :tabAuditView="tabAuditView"
                  :dateReportReceive="dateReportReceive"
                />
              </div>
            </div>
          </v-card> </v-card-text
      ></v-card>
    </div>

    <!-- CREATE BOX -->

    <!-- CAIXA DE CRIAÇÃO DE AUDITORIA -->
    <v-dialog v-model="showBoxAudit" persistent max-width="800">
      <v-card>
        {{ auditDialog }}
        <v-card-title class="text-center">Auditoria</v-card-title>
        <v-card-text>
          <v-row justify="center" class="align-center">
            <v-col cols="6" class="d-flex flex-column align-center">
              <div class="text-overline">Áreas</div>
              <!-- SELECIONAR AREA -->
              <v-select
                v-model="auditDialog.process_id"
                :items="areas"
                item-title="description"
                item-value="id"
                variant="outlined"
                label="Escolha uma área"
                class="select__box"
              ></v-select>
              <div class="text-overline">Turno</div>
              <!-- SELECIONAR TURNO -->
              <v-select
                v-model="auditDialog.shift_id"
                :disabled="!auditDialog.process_id"
                :items="shifts"
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
                  auditDialog.shift_id ? !auditDialog.shift_id.length > 0 : true
                "
                variant="flat"
                ><v-row justify="center"
                  ><v-col cols="auto" class="text-center"
                    ><n-date-picker
                      panel
                      type="date"
                      clearable
                      format="dd/MM/yyyy"
                      value-format="dd/MM/yyyy"
                      v-model:formatted-value="pickerDate"
                      class="text-center date__picker" /></v-col></v-row></v-card
            ></v-col>
          </v-row>
        </v-card-text>
        <!-- SAVE BUTTON -->
        <v-card-actions class="end__card__save">
          <v-row justify="end" class="mx-3">
            <v-btn color="red" @click="showBoxAudit = false">Cancelar</v-btn>
            <v-btn
              color="white"
              :disabled="
                auditDialog.shift_id
                  ? auditDialog.shift_id.length > 0
                    ? !pickerDate
                    : true
                  : true
              "
              @click="saveAudit()"
              >Salvar</v-btn
            >
          </v-row>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- DEFINIÇÃO DO PRAZO MÁXIMO PARA ENVIO DO RELATÓRIO -->
    <v-dialog v-model="showBoxReport" persistent max-width="600">
      <v-card>
        <v-card-title class="text-center">Entrega do Relatório</v-card-title>
        <v-card-text>
          <v-row justify="center"
            ><v-col cols="auto" class="text-center"
              ><p>
                Escolha uma data prevista que seja <br />
                pelo menos 10 dias úteis após {{ auditDates.effectiveDate }}
              </p>
              <n-date-picker
                panel
                type="date"
                clearable
                format="dd/MM/yyyy"
                :is-date-disabled="disablePastDates"
                value-format="dd/MM/yyyy"
                v-model:formatted-value="dateReport"
                class="text-center date__picker" /></v-col
          ></v-row>
        </v-card-text>
        <!-- SAVE BUTTON -->
        <v-card-actions class="end__card__save">
          <v-row justify="end" class="mx-3"
            ><v-btn
              color="white"
              @click="finishAudit('audit')"
              :disabled="!dateReport"
              >Salvar</v-btn
            ></v-row
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- DEFINIÇÃO DO DIA DA ENTREGA DO RELATÓRIO COM/SEM JUSTIFICATIVA DE ATRASO-->
    <v-dialog v-model="showBoxReportDate" persistent max-width="600">
      <v-card>
        <v-card-title class="text-center">Efetuação da Entrega</v-card-title>
        <v-card-text>
          <v-row justify="center"
            ><v-col cols="auto" class="text-center">
              <n-date-picker
                panel
                type="date"
                clearable
                format="dd/MM/yyyy"
                value-format="dd/MM/yyyy"
                v-model:formatted-value="dateReportReceive"
                class="text-center date__picker" /></v-col
            ><v-col v-if="daysRemaining < 0" cols="11" class="text-center"
              ><p class="text-overline">Motivo do Atraso</p>
              <v-text-field
                variant="outlined"
                label="Descreva o que ocasionou o atraso"
              ></v-text-field
            ></v-col>
          </v-row>
        </v-card-text>
        <!-- SAVE BUTTON -->
        <v-card-actions class="end__card__save">
          <v-row justify="end" class="mx-3">
            <v-btn color="red" @click="showBoxReportDate = false"
              >Cancelar</v-btn
            >
            <v-btn
              color="white"
              @click="reportSubmitted('save')"
              :disabled="!dateReportReceive"
              >Salvar</v-btn
            >
          </v-row>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- CAIXA DE JUSTIFICATIVA DE REPROGRAMAÇÃO -->
    <n-modal v-model:show="showReason" :mask-closable="false">
      <n-card
        title="Justificativa"
        :bordered="false"
        size="huge"
        role="dialog"
        aria-modal="true"
        style="width: 600px"
      >
        <v-textarea
          variant="outlined"
          v-model="dataUpdates.reason"
          label="Descreva a razão da reprogramação"
        ></v-textarea>
        <v-row justify="space-around">
          <v-btn @click="reason('cancel', secondReason)" width="45%" color="red"
            >Cancelar</v-btn
          ><v-btn
            @click="reason('save', secondReason)"
            width="45%"
            :disabled="!dataUpdates.reason"
            color="primary"
            >Salvar</v-btn
          ></v-row
        >
      </n-card>
    </n-modal>
  </v-card>
</template>
<script>
import queryProcess from "~/queries/process.gql";
import queryShift from "~/queries/shift.gql";
import queryAudit from "~/queries/audit.gql";

import mutationAudit from "~/queries/putAudit.gql";

import AOS from "aos";
import "aos/dist/aos.css";
AOS.init({ once: true });
export default {
  data: () => ({
    selectedComment: null,
    dataUpdates: {},
    dates: {},
    stepCompliance: 0,
    secondReason: null,
    showReason: false,
    showBoxEditReport: false,
    reasonEditReport: null,
    btnSaveAudit: false,
    btnSaveAuditDict: {},
    btnSaveCompliance: false,
    btnSaveComplianceDict: {},
    reportFinished: false,
    stepper: 0,
    dateReport: null,
    dateReportReceive: null,
    showBoxReportDate: false,
    reasonReport: null,
    daysRemaining: null,
    showBoxCompliance: false,
    showBoxAudit: false,
    showBoxReport: false,
    showDrawer: false,
    masterPlan: false,
    pickerDate: null,
    pickerDisable: { reprogDate: true, effectiveDate: true },
    auditDates: {},
    complianceDates: {},
    auditDialog: {},
    complianceDialog: {},
    audits: [],
    areas: [],
    prioritys: [
      {
        name: "Minor",
        value: 1,
      },
      {
        name: "Major",
        value: 2,
      },
      {
        name: "Oportunidade de Melhoria",
        value: 3,
      },
    ],
    columnsCompliance: [
      {
        title: "Identificador",
        key: "name",
      },
      {
        title: "Prioridade",
        key: "priority",
      },
      {
        title: "Descrição",
        key: "description",
      },
    ],
    dataCompliance: [
      {
        id: 1,
        name: "20230728#01Minor",
        priority: 2,
        description: "...",
        validation: "",
        evidence: "",
        deployment: "",
        actionPlan: "",
      },
    ],
    rowCompliance: null,
    shifts: [],
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
    iconReport: {},
  }),

  methods: {
    disablePreviousDate(ts) {
      if (!this.pickerDisable.effectiveDate) return ts > Date.now();
      if (
        this.timelineDisabledData.actionEff &&
        this.timelineDisabledData.deployEff &&
        this.timelineDisabledData.validationEff
      )
        return ts < Date.now();
      else return ts > Date.now();
    },
    disablePastDates(ts) {
      return ts < Date.now();
    },
    openBoxAudit() {
      this.showBoxAudit = true;
    },
    OpenBoxCompliance() {
      this.showBoxCompliance = true;
    },
    getProcessDescription(processId) {
      const process = this.areas.find((p) => p.id === processId);
      return process ? process.description : null;
    },
    saveAudit() {
      const { mutate: mutation } = useMutation(mutationAudit);
      mutation({
        processId: this.auditDialog.process_id,
      }).then((response) => {
        message.info("Auditoria Criada!");
        this.loadAll();
      });
      this.auditDialog = {};
      this.showBoxAudit = false;
    },
    reason(action, session) {
      if (action === "cancel") {
        if (session === "audit") {
          this.pickerDisable.reprogDate = true;
        } else {
          this.timelineDisabledData.actionReprog = true;
          this.btnSaveCompliance = false;
        }
        this.dataUpdates.reason = null;
        this.showReason = !this.showReason;
      }
      if (action === "save") {
        if (session === "audit") {
          this.btnSaveAudit = !this.btnSaveAudit;
          this.pickerDisable.reprogDate = false;
        }

        this.showReason = !this.showReason;
      }
    },
    newCompliance() {
      var id = this.dataCompliance.length + 1;
      if (id < 10) {
        id = `0${id}`;
      }
      var pt =
        this.complianceDialog.priority === 1
          ? "Minor"
          : this.complianceDialog.priority === 2
          ? "Major"
          : "Ofi";

      function obterDataHojeFormatada() {
        const data = new Date();

        const dia = adicionarZero(data.getDate());
        const mes = adicionarZero(data.getMonth() + 1); // Meses começam do zero
        const ano = data.getFullYear();

        const formatadaComum = `${dia}/${mes}/${ano}`;
        const formatadaName = `${ano}${dia}${mes}`;

        return [formatadaComum, formatadaName];
      }

      function adicionarZero(numero) {
        return numero < 10 ? `0${numero}` : numero;
      }

      function somarDias(dataString, days) {
        const [dia, mes, ano] = dataString.split("/");

        const data = new Date(`${ano}-${mes}-${dia}`);

        data.setDate(data.getDate() + days);

        const diaNovo = String(data.getDate()).padStart(2, "0");
        const mesNovo = String(data.getMonth() + 1).padStart(2, "0");
        const anoNovo = data.getFullYear();

        const novaDataString = `${diaNovo}/${mesNovo}/${anoNovo}`;

        return novaDataString;
      }

      const dataFormatada = obterDataHojeFormatada();

      var name = `${dataFormatada[1]}#${id}${pt}`;
      this.complianceDialog["id"] = id;
      this.complianceDialog["name"] = name;

      if (this.complianceDialog.priority === 2)
        this.complianceDialog["actionPlan"] = somarDias(
          this.dateReportReceive,
          20
        );
      else
        this.complianceDialog["actionPlan"] = somarDias(
          this.dateReportReceive,
          60
        );

      this.dataCompliance.push(this.complianceDialog);
      this.showBoxCompliance = false;
      this.complianceDialog = {
        id: null,
        priority: null,
        description: null,
        name: null,
      };
    },
    countdown(data) {
      const dataString = data;

      function converterStringParaData(dataString) {
        const partesData = dataString.split("/");

        return new Date(partesData[2], partesData[1] - 1, partesData[0]);
      }

      const dataOriginal = converterStringParaData(dataString);

      const dataCom10Dias = new Date(dataOriginal);
      dataCom10Dias.setDate(dataOriginal.getDate());

      const dataAtual = new Date();

      const diferencaEmMilissegundos = dataCom10Dias - dataAtual;
      const diferencaEmDias = Math.ceil(
        diferencaEmMilissegundos / (1000 * 60 * 60 * 24)
      );
      return diferencaEmDias;
    },
    alternableBtnAudit(button) {
      if (button === "reprogram") {
        this.pickerDisable.reprogDate = !this.pickerDisable.reprogDate;
        this.secondReason = "audit";
        this.showReason = !this.showReason;
      } else {
        this.btnSaveAudit = !this.btnSaveAudit;
      }
      if (button === "finishAudit")
        this.pickerDisable.effectiveDate = !this.pickerDisable.effectiveDate;

      if (button != "cancel" && button != "save") {
        this.btnSaveAuditDict["call"] = button;
      }

      if (button === "save") {
        if (this.btnSaveAuditDict.call === "reprogram") {
          this.audit = { ...this.audit, ...this.auditDates };
          this.pickerDisable.reprogDate = true;
        } else {
          this.pickerDisable.effectiveDate = true;
          this.showBoxReport = true;
        }
      }

      if (button === "cancel") {
        this.pickerDisable.effectiveDate = true;
        this.pickerDisable.reprogDate = true;

        this.auditDates.effectiveDate = null;
        if (this.audit.reprogDate) {
          this.auditDates.reprogDate = this.audit.reprogDate;
        } else this.auditDates.reprogDate = null;
      }
    },
    alternableBtnCompliance(button, position, cancel = ["Reprog", "Eff"]) {
      var saveFieldCompliance = null;
      if (button === "Reprog" || button === "Eff") {
        this.btnSaveComplianceDict["call"] = button;
        this.btnSaveComplianceDict["field"] = position + button;
      }
      if (this.stepCompliance == 0) saveFieldCompliance = "actionPlan";
      else if (this.stepCompliance == 1) saveFieldCompliance = "deployment";
      else if (this.stepCompliance == 2) saveFieldCompliance = "validation";

      var date = this.btnSaveComplianceDict.field;
      var disable = position + button;

      this.timelineDisabledData[disable] = !this.timelineDisabledData[disable];

      if (button === "Reprog") {
        this.secondReason = "compliance";
        this.showReason = true;
        this.dataUpdates.reason = null;
      }
      if (button === "Save") {
        if (this.btnSaveComplianceDict["call"] == "Reprog")
          this.dataUpdates.newDate = this.complianceDates[date];
        if (this.btnSaveComplianceDict["call"] == "Eff") {
          this.dataCompliance[this.rowCompliance - 1][saveFieldCompliance] =
            this.complianceDates[date];
          this.stepCompliance++;
        }

        this.timelineDisabledData[position + cancel[0]] = true;
        this.timelineDisabledData[position + cancel[1]] = true;
      }
      if (button === "Cancel") {
        this.timelineDisabledData[position + cancel[0]] = true;
        this.timelineDisabledData[position + cancel[1]] = true;
      }
      this.btnSaveCompliance = !this.btnSaveCompliance;
    },
    finishAudit(step) {
      if (step === "audit") {
        this.audit = { ...this.audit, ...this.auditDates };
        this.daysRemaining = this.countdown(this.dateReport);
        this.iconReport.icon = "clock-time-eight-outline";
        this.iconReport.color = "black";
        this.stepper = 1;
        this.showBoxReport = false;
      } else {
        this.showBoxEditReport = false;
        this.daysRemaining = this.countdown(this.dateReport);
      }
    },
    reportSubmitted(action) {
      if (action === "save") {
        this.iconReport.color = "green";
        this.iconReport.icon = "check-decagram-outline";
        this.stepper = 2;
        this.reportFinished = true;
        this.showBoxReportDate = false;
      } else if (action === "send") {
        this.showBoxReportDate = true;
      } else {
        this.showBoxEditReport = true;
      }
    },
    setDateUpdate(reason, newDate, dateId) {
      console.log(reason, newDate, dateId);
    },
    completedAudit() {
      this.stepper = 3;
    },
    saveComment() {
      var newComment = {};
      newComment["comment"] = this.comment;
      function capturarDataHoraAtual() {
        var dataAtual = new Date();
        var options = {
          day: "numeric",
          month: "long",
          year: "numeric",
          hour: "numeric",
          minute: "numeric",
        };
        var dataFormatada = dataAtual.toLocaleString("pt-BR", options);
        return dataFormatada;
      }
      if (this.comment) {
        newComment["date"] = capturarDataHoraAtual();
        newComment["name"] = "Matheus Doreto";
        this.comments.push(newComment);
      }
      this.comment = null;
    },
    setStep(rowCompliance) {
      if (this.dataCompliance[rowCompliance - 1].actionPlan)
        this.stepCompliance = 0;
      if (this.dataCompliance[rowCompliance - 1].deployment)
        this.stepCompliance = 1;
      if (this.dataCompliance[rowCompliance - 1].validation)
        this.stepCompliance = 2;
    },
    clear() {
      this.reportFinished = false;
      this.daysRemaining = null;
      this.stepper = 0;
      this.dateReport = null;
      this.dateReportReceive = null;
      this.btnSaveAudit = false;
      this.pickerDisable.effectiveDate = true;
      this.pickerDisable.reprogDate = true;
      this.tabAuditView = 0;
    },
    loadAll() {
      useAsyncQuery(queryProcess).then(({ data }) => {
        this.areas = data.value.processs;
      });
      useAsyncQuery(queryShift).then(({ data }) => {
        this.shifts = data.value.shifts;
      });
      useAsyncQuery(queryAudit).then(({ data }) => {
        this.audits = data.value.audits;
      });
    },
  },

  created() {
    this.loadAll();
  },

  watch: {
    audits(val) {
      this.tab = val - 1;
    },
    audit: {
      handler(newAudit, oldAudit) {
        for (const key in newAudit) {
          if (newAudit[key] !== oldAudit[key]) {
            if (key === "name") {
              this.clear();

              if (this.audit.reprogDate)
                this.auditDates = { reprogDate: this.audit.reprogDate };
              else this.auditDates = { reprogDate: null };

              if (this.audit.effectiveDate) {
                this.auditDates = { effectiveDate: this.audit.effectiveDate };
                this.daysRemaining = this.countdown(this.audit.effectiveDate);
                if (this.reportFinished) {
                  this.iconReport.icon = "check-decagram-outline";
                  this.iconReport.color = "green";
                } else {
                  this.iconReport.icon = "clock-time-eight-outline";
                  this.iconReport.color = "black";
                }
              } else {
                this.auditDates.effectiveDate = null;
                this.iconReport.icon = "";
              }
            }
          }
        }
      },
      deep: true,
    },
    auditDates() {
      if (this.auditDates.effectiveDate) {
        this.stepper = 1;
      }
    },
    auditDialog() {
      if (this.auditDialog.mp) {
        this.auditDates.mpDate = this.auditDialog.mp;
      }
    },
    showBoxAudit() {
      if (!this.showBoxAudit) this.masterPlan = false;
    },
    rowCompliance() {
      if (this.rowCompliance) this.setStep(this.rowCompliance);
    },
    complianceDates: {
      handler(newDict, oldDict) {
        if (newDict.deployPrev) this.timelineDisabledData.deployPrev = true;
        if (newDict.validationPrev)
          this.timelineDisabledData.validationPrev = true;
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
