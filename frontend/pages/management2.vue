<template>
  <v-row justify="center"
    ><v-col>
      <v-card class="pb-5">
        <v-card class="pa-3 select_card" rounded="0"
          ><v-row justify="center"
            ><v-col class="text-center">Auditoria</v-col></v-row
          ></v-card
        >

        <v-row justify="center" class="ma-1"
          ><v-col class="text-end"
            ><v-btn
              :color="btnNewAudit.color"
              width="200"
              :disabled="rowAudit"
              @click="newAudit()"
              >{{ btnNewAudit.text }}</v-btn
            ></v-col
          ></v-row
        >
        <v-row justify="center" no-gutters>
          <v-col class="mx-4"
            ><p-data-table
              :columns="columns"
              :data="dataAudit"
              :id="['id']"
              :height="false"
              :selectable="selectable"
              v-model="rowAudit"
            >
            </p-data-table></v-col
        ></v-row>

        <v-divider class="mx-10 my-2"></v-divider>
        <!-- DATE PICKERS PDG AND PLANEJADO -->

        <div v-if="editSaveAudit || rowAudit">
          <datePicker v-model="auditDates" />

          <!-- SELECT AREA  -->

          <v-row justify="space-around"
            ><v-col cols="5">
              <v-row justify="center" no-gutters
                ><v-col cols="4" class="text-overline text-center"
                  >Área</v-col
                ></v-row
              ><v-select
                v-model="auditDesc.area"
                label="Selecione uma área"
                variant="outlined"
                :items="areas"
                clearable
              ></v-select
            ></v-col>
            <v-col
              cols="2"
              class="text-center d-flex justify-center align-center"
            >
              <v-btn
                color="#212b59"
                width="200"
                size="large"
                >reprogramar</v-btn
              ></v-col
            >
            <v-col
              cols="2"
              class="text-start d-flex justify-center align-center"
            >
              <v-btn
                :color="btnSaveAudit.color"
                width="200"
                @click="editAudit()"
                size="large"
                >{{ btnSaveAudit.text }}</v-btn
              ></v-col
            ></v-row
          >
        </div>

        <v-divider class="mx-10 my-3"></v-divider>

        <v-card
          class="pa-3 select_card"
          rounded="0"
          @click="ViewDataCompliance()"
          :disabled="!rowAudit"
          ><v-row justify="center"
            ><v-col class="text-center">Não conformidades</v-col></v-row
          ></v-card
        >

        <div v-if="complianceView">
          <v-row justify="center" class="ma-1"
            ><v-col class="text-end"
              ><v-btn
                :color="btnNewCompliance.color"
                width="200"
                :disabled="rowCompliance"
                @click="newCompliance()"
                >{{ btnNewCompliance.text }}</v-btn
              ></v-col
            >
          </v-row>
          <v-row justify="center">
            <v-col class="mx-4 my-2"
              ><p-data-table
                :columns="columnsCompliance"
                :data="dataCompliance"
                :id="['id']"
                :height="false"
                :selectable="selectableCompliance"
                v-model="rowCompliance"
              >
              </p-data-table></v-col
          ></v-row>

          <div v-if="editCompliance || rowCompliance">
            <v-row justify="center"
              ><v-col class="text-overline text-center">Descrição</v-col></v-row
            >

            <v-textarea
              v-model="auditDesc.description"
              class="mx-5"
              label="Escreva uma descrição"
              variant="outlined"
            ></v-textarea>

            <datePicker v-model="compliance" />

            <v-row justify="center"
              ><v-col class="text-end"
                ><v-btn
                  color="#E8EAF6"
                  @click="show = true"
                  append-icon="mdi-message"
                >
                  Comentários</v-btn
                >
                <n-drawer v-model:show="show" :width="600" height="500">
                  <n-drawer-content title="Comentários" :native-scrollbar="false" closable trigger="none">
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
              ><v-col class="text-start"
                ><v-btn
                  :color="btnSaveCompliance.color"
                  width="200"
                  @click="editSaveCompliance()"
                  >{{ btnSaveCompliance.text }}</v-btn
                ></v-col
              ></v-row
            >
          </div>
        </div>
      </v-card>
    </v-col></v-row
  >
</template>
<script>
export default {
  data: () => ({
    areas: [
      "OE Sales",
      "PMS",
      "Procurement",
      "QMS",
      "ICT",
      "Production Planning",
    ],
    rowAudit: null,
    rowCompliance: null,
    show: false,
    editSaveAudit: false,
    auditDesc: {},
    auditDates: {},
    audit: {},
    selectable: true,
    selectableCompliance: true,
    btnNewAudit: { color: "green", text: "Novo" },
    btnSaveAudit: { color: "#212b59", text: "Editar" },
    btnNewCompliance: {
      color: "green",
      text: "Novo",
    },
    btnSaveCompliance: {
      color: "#212b59",
      text: "Editar",
    },
    complianceView: false,
    editCompliance: false,
    compliance: {},
    columns: [
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
    columnsCompliance: [
      {
        title: "Não Conformidade",
        key: "compliance",
      },
      {
        title: "Data",
        key: "date",
      },
    ],
    dataAudit: [
      { id: 3, audit: "Wonderwall", length: "4:18", date: 1 },
      { id: 4, audit: "Don't Look Back in Anger", length: "4:48", date: 2 },
      { id: 12, audit: "Champagne Supernova", length: "7:27", date: 3 },
    ],
    dataCompliance: [
      { id: 9, compliance: "Wonderwall", length: "4:18", date: 1 },
      {
        id: 5,
        compliance: "Don't Look Back in Anger",
        length: "4:48",
        date: 2,
      },
      { id: 15, compliance: "Champagne Supernova", length: "7:27", date: 3 },
    ],
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
  }),

  methods: {
    newAudit() {
      this.editSaveAudit = !this.editSaveAudit;
      this.selectable = !this.selectable;
      this.btnNewAudit.color =
        this.btnNewAudit.color === "red" ? "green" : "red";

      this.btnNewAudit.text =
        this.btnNewAudit.text === "Novo" ? "Cancelar" : "Novo";
    },
    editAudit() {
      this.btnSaveAudit.color =
        this.btnSaveAudit.color === "#212b59" ? "green" : "#212b59";

      this.btnSaveAudit.text =
        this.btnSaveAudit.text === "Salvar" ? "Editar" : "Salvar";
    },
    saveAudit() {
      this.audit = { ...this.auditDesc, ...this.auditDates };
      console.log(this.audit);
    },
    ViewDataCompliance() {
      this.complianceView = !this.complianceView;
    },
    newCompliance() {
      this.btnNewCompliance.color =
        this.btnNewCompliance.color === "red" ? "green" : "red";

      this.btnNewCompliance.text =
        this.btnNewCompliance.text === "Novo" ? "Cancelar" : "Novo";
      this.editCompliance = !this.editCompliance;
      this.selectableCompliance = !this.selectableCompliance;
    },
    editSaveCompliance() {
      this.btnSaveCompliance.color =
        this.btnSaveCompliance.color === "#212b59" ? "green" : "#212b59";

      this.btnSaveCompliance.text =
        this.btnSaveCompliance.text === "Salvar" ? "Editar" : "Salvar";
    },
  },
  watch: {
    rowAudit() {
      if (this.rowAudit) {
        if (!this.complianceView) this.complianceView = true;
      } else {
        if (this.complianceView) this.complianceView = false;
      }
    },
  },
};
</script>

<style scoped>
.select_card {
  background-color: #ccc;
  text-transform: uppercase;
  font-weight: bold;
  color: #212b59;
}
.box {
  background-color: #f5f5f5;
  padding: 1rem;
  border: 1px solid #212b59;
}
</style>
