<template>
  <v-card>
    <div class="d-flex flex-row">
      <!-- TABS LATERAIS -->

      <v-tabs v-model="audit" :color="prometeon" direction="vertical">
        <v-tab
          v-for="n in audits"
          :key="n.mpDate ? n.mpDate : n.reprogDate"
          :value="n"
        >
          {{ n.name }}
        </v-tab>
        <v-row justify="center"
          ><v-col class="text-center"
            ><v-btn
              variant="text"
              @click="openBoxAudit()"
              icon="mdi-plus"
              class="text-center"
              :color="prometeon"
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

          <v-row justify="space-around" class="my-3"
            ><v-col
              cols="3"
              class="d-flex justify-center flex-columns align-center text-center"
              ><v-card class="pa-10" elevation="14"
                ><p class="text-h6 font-weight-bold">Previsto</p>
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
                        { title: 'Reprogramado', value: 'reprog' },
                        { title: 'Efetivo', value: 'effective' },
                      ]"
                      ><v-row justify="center"> {{ d.title }}</v-row
                      ><v-row justify="center"
                        ><v-col class="text-h6"
                          ><n-date-picker
                            v-model:formatted-value="
                              auditDates[d['value'] + type.value]
                            "
                            :is-date-disabled="disablePreviousDate"
                            type="date"
                            clearable
                            value-format="dd/MM/yyyy"
                            size="large"
                            :disabled="pickerDisable[d['value'] + type.value]"
                            placeholder="Selecione uma data" /></v-col
                      ></v-row>
                    </v-col>
                  </v-row>
                </v-col>
                <v-col class="text-center"
                  ><div v-if="!btnSave && !audit.effectiveDate">
                    <v-btn
                      color="orange"
                      class="mr-3"
                      @click="alternableBtn('reprogram')"
                      >Reprogramar</v-btn
                    ><v-btn
                      color="green"
                      class="ml-3"
                      @click="alternableBtn('finishAudit')"
                      >Concluir</v-btn
                    >
                  </div>
                  <div v-if="btnSave && !audit.effectiveDate">
                    <v-btn
                      color="green"
                      class="mr-3"
                      :disabled="
                        (auditDates.reprogDate == audit.reprogDate &&
                          btnSaveDict.call == 'reprogram') ||
                        (auditDates.effectiveDate == null &&
                          btnSaveDict.call == 'finishAudit')
                      "
                      @click="alternableBtn('save')"
                      >Salvar</v-btn
                    ><v-btn
                      color="red"
                      class="ml-3"
                      @click="alternableBtn('cancel')"
                      >Cancelar</v-btn
                    >
                  </div></v-col
                ></v-row
              ></v-col
            >
          </v-row>

          <v-card elevation="4">
            <!-- TABS RELATÓRIO E NÃO CONFORMIDADES -->

            <v-tabs v-model="tabAuditView" :bg-color="prometeon" grow>
              <v-tab v-for="n in tabContent" :key="n" :value="n.value">
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
                    <v-col
                      v-if="!dateReportReceive"
                      cols="12"
                      class="text-center"
                      ><v-btn
                        :disabled="!dateReport"
                        color="orange"
                        class="mr-3"
                        @click="reportSubmitted('reprog')"
                        >Reprogramar</v-btn
                      ><v-btn
                        color="green"
                        :disabled="
                          !this.audit.effectiveDate || this.reportFinished
                        "
                        @click="reportSubmitted('save')"
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
                <!-- NEW BUTTON -->
                <v-row justify="center" class="ma-1"
                  ><v-col class="text-end"
                    ><v-btn
                      :color="btnNewCompliance.color"
                      :disabled="!this.reportFinished"
                      width="200"
                      @click="OpenBoxCompliance()"
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
                      :on-update:checked-row-keys="
                        setStepTimeline(rowCompliance)
                      "
                      v-model="rowCompliance"
                    >
                    </p-data-table></v-col
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
                        ><v-divider class="mb-2"></v-divider
                        >{{
                          dataCompliance[rowCompliance - 1].description
                        }}</v-col
                      ></v-row
                    >
                  </v-card>

                  <v-timeline align="start">
                    <v-timeline-item
                      v-for="(item, i) in timelineItems"
                      :key="i"
                      :dot-color="i < stepCompliance ? 'green' : prometeon"
                      :icon="item.icon"
                      width="450"
                      fill-dot
                    >
                      <!-- CONTEUDO TIMELINE DE CADA ITEM -->
                      <!-- <template v-slot:opposite>
                        <v-card elevation="8"><v-card-text>TESTANDO</v-card-text></v-card>
                      </template> -->
                      <v-card elevation="8" :disabled="!(i == stepCompliance)">
                        <v-card
                          rounded="0"
                          :class="[
                            'text-h6',
                            'timeline',
                            'text-center',
                            'pa-2',
                          ]"
                        >
                          {{ item.title }}
                        </v-card>
                        <v-card-text class="bg-white text--primary text-center">
                          <v-row
                            ><v-col
                              cols="12"
                              class="text-center"
                              v-for="picker in [
                                {
                                  title: 'Previsto',
                                  value: 'prev',
                                },
                                {
                                  title: 'Reprogramado',
                                  value: 'reprog',
                                },
                                {
                                  title: 'Efetivo',
                                  value: 'Eff',
                                },
                              ]"
                            >
                              <div
                                v-if="!(picker.title == 'Previsto' && i == 0)"
                              >
                                <div class="text-overline">
                                  {{ picker.title }}
                                </div>
                                <n-date-picker
                                  type="date"
                                  placeholder="Selecione uma Data"
                                  value-format="dd/MM/yyyy"
                                  v-model:formatted-value="
                                    complianceDates[
                                      item['value'] + picker.value
                                    ]
                                  "
                                  class="text-center date__picker"
                                />
                              </div>
                              <div
                                v-else
                                class="card__plan bg-indigo-lighten-5"
                              >
                                <v-card-title> Agendado </v-card-title>
                                <v-divider class="mx-6"></v-divider>
                                <v-row justify="center"
                                  ><v-col class="text-center text-h6 my-3">{{
                                    dataCompliance[rowCompliance - 1].actionPlan
                                  }}</v-col></v-row
                                >
                              </div>
                            </v-col></v-row
                          >
                          <div v-if="dataUpdates.reason && stepCompliance == i">
                          <v-row justify="center"><v-col cols="12" class="text-center">
                          <v-btn
                              color="green"
                              class="mr-3"
                              @click=""
                              >Salvar</v-btn
                            ><v-btn
                              color="red"
                              class="ml-3"
                              @click=""
                              >Cancelar</v-btn
                            ></v-col></v-row>
                            
                          </div>
                          <div v-else>
                            <v-row justify="center"
                              ><v-col cols="12" class="text-center"
                                ><v-btn
                                  color="orange"
                                  class="mt-2 mx-2"
                                  @click="showReason=true"
                                >
                                  Reprogramar
                                </v-btn>
                                <v-btn
                                  :color="prometeon"
                                  width="100"
                                  class="mt-2 mx-2"
                                  @click="stepCompliance++"
                                >
                                  Ok
                                </v-btn></v-col
                              ></v-row
                            >
                          </div>
                        </v-card-text>
                      </v-card>
                    </v-timeline-item>
                  </v-timeline>
                </div>

                <!-- COMMENTS -->
                <v-row justify="center"
                  ><v-divider
                    :thickness="2"
                    class="mt-4 mx-8"
                    :color="prometeon"
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
                    <n-drawer v-model:show="showDrawer" width="30vw">
                      <n-drawer-content
                        title="Comentários"
                        :native-scrollbar="false"
                        closable
                        trigger="none"
                      >
                        <div id="comments-container">
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
                                  ><v-col
                                    cols="6"
                                    class="text-end font-italic"
                                    >{{ item.date }}</v-col
                                  >
                                  <v-divider class="mx-3"></v-divider>
                                  <v-col>{{ item.comment }}</v-col>
                                </v-row>
                              </div>
                            </n-grid-item>
                          </n-grid>
                        </div>
                        <div id="fixed-div">
                          <v-divider class="my-2"></v-divider>

                          <v-text-field
                            v-model="comment"
                            label="Novo Comentário"
                            variant="outlined"
                            append-icon="mdi-send"
                            @click:append="saveComment()"
                            @keydown.enter="saveComment()"
                          ></v-text-field>
                        </div>
                      </n-drawer-content> </n-drawer></v-col
                ></v-row>
              </div>
            </div>
          </v-card> </v-card-text
      ></v-card>
    </div>

    <!-- CREATE BOX -->

    <!-- CAIXA DE CRIAÇÃO DE AUDITORIA -->
    <v-dialog v-model="showBoxAudit" persistent max-width="800">
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
                multiple
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
                  clearable
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

    <!-- ALTERAÇÃO DO PRAZO MÁXIMO PARA ENVIO DO RELATÓRIO -->
    <v-dialog v-model="showBoxEditReport" persistent max-width="600">
      <v-card>
        <v-card-title class="text-center">Entrega do Relatório</v-card-title>
        <v-card-text>
          <v-row justify="center"
            ><v-col cols="auto" class="text-center"
              ><p>Escolha uma nova data</p>
              <n-date-picker
                panel
                clearable
                type="date"
                value-format="dd/MM/yyyy"
                :is-date-disabled="disablePastDates"
                v-model:formatted-value="dateReport"
                class="text-center date__picker" /></v-col
            ><v-col cols="11" class="text-center"
              ><p class="text-overline">Motivo do Reajuste</p>
              <v-text-field
                :disabled="!dateReport"
                variant="outlined"
                label="Descreva o porquê necessita de reajuste"
                v-model="reasonEditReport"
                @keydown.enter="showBoxEditReport = false"
              ></v-text-field></v-col
          ></v-row>
        </v-card-text>
        <!-- SAVE BUTTON -->
        <v-card-actions class="end__card__save">
          <v-row justify="end" class="mx-3"
            ><v-btn
              color="white"
              @click="finishAudit('nonCompliance')"
              :disabled="!reasonEditReport"
              >Salvar</v-btn
            ></v-row
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- DEFINIÇÃO DO DIA DA ENTREGA DO RELATÓRIO -->
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
          <v-row justify="end" class="mx-3"
            ><v-btn
              color="white"
              @click="showBoxReportDate = false"
              :disabled="!dateReportReceive"
              >Salvar</v-btn
            ></v-row
          >
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- CAIXA DE CRIAÇÃO DE NÃO CONFORMIDADE -->
    <v-dialog v-model="showBoxCompliance" max-width="500">
      <v-card>
        <v-card-title class="text-center">Não Conformidade</v-card-title>
        <v-card-text>
          <v-row justify="center" class="text-center">
            <v-col cols="8">
              <div class="text-overline">prioridade</div>
              <!-- SELECIONAR AREA -->
              <v-select
                v-model="complianceDialog.priority"
                :items="prioritys"
                variant="outlined"
                item-value="value"
                item-title="name"
                label="Escolha uma prioridade"
              ></v-select>
              <div class="text-overline">descrição</div>
              <!-- SELECIONAR TURNO -->
              <v-textarea
                v-model="complianceDialog.description"
                variant="outlined"
                placeholder="Descrição da Não Conformidade"
              ></v-textarea>
            </v-col>
          </v-row>
        </v-card-text>
        <!-- SAVE BUTTON -->
        <v-card-actions class="end__card__save">
          <v-row justify="end" class="mx-3"
            ><v-btn color="white" @click="newCompliance()">Salvar</v-btn></v-row
          >
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
          <v-btn @click="reason('cancel')" width="45%" color="red"
            >Cancelar</v-btn
          ><v-btn
            @click="reason('save')"
            width="45%"
            :disabled="!dataUpdates.reason"
            :color="prometeon"
            >Salvar</v-btn
          ></v-row
        >
      </n-card>
    </n-modal>

    <!-- CAIXA DE JUSTIFICATIVA DE ATRASO DO RELATÓRIO -->
    <n-modal v-model:show="showReasonReport" :mask-closable="false">
      <n-card
        title="Motivo do Atraso"
        :bordered="false"
        size="huge"
        role="dialog"
        aria-modal="true"
        style="width: 600px"
      >
        <v-textarea
          variant="outlined"
          v-model="reasonReport"
          label="Descreva o que levou ao atraso!"
        ></v-textarea>
        <v-row justify="space-around">
          <v-btn
            @click="showReasonReport = false"
            width="95%"
            :disabled="!reasonReport"
            :color="prometeon"
            >Salvar</v-btn
          ></v-row
        >
      </n-card>
    </n-modal>
  </v-card>
</template>
<script>
import AOS from "aos";
import "aos/dist/aos.css";
AOS.init();
export default {
  data: () => ({
    dataUpdates: {},
    stepCompliance: 0,
    showReason: false,
    showReasonReport: false,
    showBoxEditReport: false,
    reasonEditReport: null,
    prometeon: "#212b59",
    btnSave: false,
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
        icon: "mdi-note",
        value: "action",
      },
      {
        title: "Implementação",
        icon: "mdi-arrow-up-bold-outline",
        value: "deploy",
      },
      {
        title: "Verificação da Eficácia",
        icon: "mdi-layers-triple",
        value: "validation",
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
      //   {
      //     id: 2,
      //     name: "20230728#02Minor",
      //     priority: 1,
      //     description: "...",
      //     validation: "",
      //     evidence: "2",
      //     deployment: "",
      //     actionPlan: "",
      //   },
      //   {
      //     id: 3,
      //     name: "20230728#03Minor",
      //     priority: 3,
      //     description: "...",
      //     validation: "",
      //     evidence: "",
      //     deployment: "3",
      //     actionPlan: "",
      //   },
      //   {
      //     id: 4,
      //     name: "20230728#04Minor",
      //     priority: 1,
      //     description: "...",
      //     validation: "",
      //     evidence: "",
      //     deployment: "",
      //     actionPlan: "4",
      //   },
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
    tabAuditView: null,
    btnNewCompliance: {
      color: "green",
      text: "Novo",
    },
    comment: null,
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
    btnSaveDict: {},
  }),

  methods: {
    disablePreviousDate(ts) {
      if (this.pickerDisable.reprogDate) return ts >= Date.now();
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
    saveAudit() {
      if (this.masterPlan) this.auditDialog["mpDate"] = this.pickerDate;
      else this.auditDialog["reprogDate"] = this.pickerDate;
      this.audits.push(this.auditDialog);
      this.auditDialog = {};
      this.showBoxAudit = false;
    },
    reason(action) {
      if (action === "cancel") {
        this.dataUpdates.reason = null;
        this.showReason = !this.showReason;
        this.pickerDisable.reprogDate = true;
      }
      if (action === "save") {
        this.btnSave = !this.btnSave;
        this.showReason = !this.showReason;
        this.pickerDisable.reprogDate = false;
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
    alternableBtn(button) {
      if (button === "reprogram") {
        this.pickerDisable.reprogDate = !this.pickerDisable.reprogDate;
        this.showReason = !this.showReason;
      } else {
        this.btnSave = !this.btnSave;
      }
      if (button === "finishAudit")
        this.pickerDisable.effectiveDate = !this.pickerDisable.effectiveDate;

      if (button != "cancel" && button != "save") {
        this.btnSaveDict["call"] = button;
      }

      if (button === "save") {
        if (this.btnSaveDict.call === "reprogram") {
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
    setStepTimeline(key) {
      if (!key) {
      } else if (this.dataCompliance[key - 1].validation)
        this.stepCompliance = 3;
      else if (this.dataCompliance[key - 1].evidence) this.stepCompliance = 2;
      else if (this.dataCompliance[key - 1].deployment) this.stepCompliance = 1;
      else if (this.dataCompliance[key - 1].actionPlan) this.stepCompliance = 0;
    },
    clear() {
      this.reportFinished = false;
      this.daysRemaining = null;
      this.stepper = 0;
      this.dateReport = null;
      this.dateReportReceive = null;
      this.btnSave = false;
      this.pickerDisable.effectiveDate = true;
      this.pickerDisable.reprogDate = true;
      this.tabAuditView = 0;
    },
  },

  computed: {},

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
  border-radius: 5px;
}

.card__content {
  border-left: 1px solid #949393;
}

.timeline {
  background-color: #212b59;
  color: white;
}

.card__plan {
  border: 1px solid #797979;
  border-radius: 5px;
}

#fixed-div {
  position: fixed;
  bottom: 0;
  width: 28vw;
  padding: 10px;
  box-sizing: border-box;
  background-color: #fff;
}

#comments-container {
  max-height: calc(100vh - 180px);
  overflow-y: auto;
  padding: 10px;
  box-sizing: border-box;
}
</style>
