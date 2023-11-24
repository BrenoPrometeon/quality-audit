<template>
  <v-row justify="center"
    ><v-col>
      <v-card>
        <!-- SELECT AREA  -->

        <v-row justify="center" 
          ><v-col cols="8">
            <v-row justify="center" class="mt-3" no-gutters
              ><v-col class="text-overline text-center">Área</v-col></v-row
            ><v-select
              v-model="auditDesc.area"
              label="Selecione uma área"
              variant="outlined"
              :items="areas"
              clearable
            ></v-select></v-col
        ></v-row>

        <v-divider class="mx-5"></v-divider>

        <!-- DATE PICKERS PDG AND PLANEJADO -->

        <datePicker v-model="auditDates" />

        <v-row justify="center"><v-col cols="9"><n-data-table
        :columns="columns">
        </n-data-table></v-col></v-row>
        <!-- SAVED BUTTON -->

        <v-row justify="center"
          ><v-col cols="4" class="text-center mb-4"
            ><v-btn color="green" @click="saveAudit">Save</v-btn></v-col
          ></v-row
        >
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
    auditDesc: {},
    auditDates: {},
    audit:{},
    columns:[{
      title: 'Hello',
      value: 'hi'
    },
    {
      title:'World',
      value: 'hello'
    }
  ]
  }),

  methods: {
    saveAudit() {
      this.audit = {...this.auditDesc, ...this.auditDates}
      console.log(this.audit)
    },
  },
};
</script>

<style scoped></style>
