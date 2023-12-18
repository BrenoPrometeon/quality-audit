<template>
  <!-- STATUS NAO CONFORMIDADES -->
  <div v-if="tabAuditView == 1" data-aos="fade-up" data-aos-duration="800">
    <!-- NEW BUTTON -->
    <v-row justify="center" class="ma-1"
      ><v-col class="text-end"
        ><v-btn
          color="success"
          :disabled="!this.reportFinished"
          width="200"
          @click="showBoxCompliance = true"
          >Novo</v-btn
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
    <div
      v-if="rowCompliance"
      class="d-flex flex-column justify-center align-center"
    >
      <v-card variant="tonal" width="50vw" class="my-3">
        <v-card-title class="text-center">Descrição</v-card-title>
        <v-row justify="center" class="pa-3"
          ><v-col class="text-center"
            ><v-divider class="mb-2"></v-divider
            >{{ dataCompliance[rowCompliance - 1].description }}</v-col
          ></v-row
        >
      </v-card>

      <v-timeline align="start" data-aos="fade-up" data-aos-duration="1000">
        <v-timeline-item
          v-for="(item, i) in timelineItems"
          :key="i"
          :dot-color="i < stepCompliance ? 'green' : prometeon"
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
              rounded="0"
              :class="['text-h6', 'timeline', 'text-center', 'pa-2']"
              >{{ item.title }}</v-card
            ><q-date-picker :obj="obj" />
          </v-card>
        </v-timeline-item>
      </v-timeline>
    </div>
  </div>

  <!-- CAIXA DE CRIAÇÃO DE NÃO CONFORMIDADE -->
  <v-dialog v-model="boxReprog" max-width="500">
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
</template>
<script>
export default {
  props: {
    tabAuditView: {
      type: Number,
      required: true,
    },
    reportFinished: {
      type: Boolean,
      required: true,
    },
    stepCompliance: {
      type: Number,
      required: true,
    },
    dateReportReceive: { required: true },
  },
  data: () => ({
    complianceDialog: {},
    showBoxCompliance: false,
    rowCompliance: null,
    prometeon: "#212b59",
    obj: {
      prev: "22/10/2023",
      reprog: "23/12/2023",
      eff: "22/10/2023",
      customField: "Entrega do Relatório",
    },
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
  methods: {
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
  },
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
