<template>
  <v-card
    ><v-row justify="center"
      ><v-col>
        <!-- SELECT PLAN  -->
        <v-row justify="center"
          ><v-col cols="8">
            <v-row justify="center" class="mt-3" no-gutters
              ><v-col class="text-overline text-center">Auditoria</v-col></v-row
            ><v-select
              v-model="auditDesc.area"
              label="Selecione uma auditoria"
              variant="outlined"
              :items="audits"
            ></v-select></v-col
        ></v-row>

        <v-divider class="mx-5"></v-divider>

        <!-- INPUT NAME  -->
        <v-row justify="center" color="green"
          ><v-col>
            <v-row justify="center" no-gutters
              ><v-col class="text-overline text-center"
                >Identificação</v-col
              ></v-row
            >
            <v-row justify="center" no-gutters><v-col cols="10"><v-text-field
            
              v-model="auditDesc.complianceName"
              label="Escreva um identificador"
              variant="outlined"
              clearable
            ></v-text-field
          ></v-col></v-row></v-col>
          <v-col>
            <v-row justify="center"
              ><v-col class="text-overline text-center"
                >priority</v-col
              ></v-row
            >
            <v-row justify="center" no-gutters
              ><v-col cols="10" class="text-center"
                ><v-select
                v-model="auditDesc.priority"
                  size="large"
                  label="Choose a priority level"
                  :items="prioritys"
                  variant="underlined"
                >
                </v-select></v-col
            ></v-row> </v-col
        ></v-row>

        <v-divider class="mx-5"></v-divider>

        <!-- DATE PICKERS PDG AND PLANEJADO -->

        <datePicker v-model="auditDates"/>

        <v-divider class="ma-5"></v-divider>

        <!-- DESCRIPTION -->

        <v-row justify="center"
          ><v-col class="text-overline text-center">notes</v-col></v-row
        >

        <v-textarea
        v-model="auditDesc.description"
          class="mx-5"
          label="Description"
          variant="outlined"
        ></v-textarea>

        <v-divider class="ma-5"></v-divider>

        <!-- SAVED BUTTON -->

        <v-row justify="center"
          ><v-col cols="4" class="text-center mb-4"
            ><v-btn color="green" @click="create">Save</v-btn></v-col
          ></v-row
        >
      </v-col></v-row
    ></v-card
  >
</template>
<script>
export default {
  data: () => ({
    auditDesc: {},
    auditDates: {},
    audit: {},
    audits: ["Indoor", "Outdoor"],
    prioritys: ["Major", "Minor", "Improvement Opportunity"],
  }),
  methods: {
    create(){
      this.audit = {...this.auditDesc, ...this.auditDates}
      console.log(this.audit)
    }
  },
};
</script>

<style scoped></style>
