<template>
  <!-- COMMENTS -->
  <v-row justify="center"
    ><v-divider :thickness="2" class="mt-4 mx-8" :color="prometeon"></v-divider
    ><v-col class="text-center ma-3"
      ><v-btn
        :disabled="!rowCompliance"
        color="#E8EAF6"
        @click="showDrawer = true"
        append-icon="mdi-message"
      >
        Comentários</v-btn
      >
      <n-drawer v-model:show="showDrawer" width="40vw">
        <n-drawer-content
          title="Comentários"
          :native-scrollbar="false"
          closable
          trigger="none"
        >
          <div id="comments__container">
            <n-grid :y-gap="8" :cols="1">
              <n-grid-item v-for="item in comments">
                <div
                  @click="toggleCommentSelection(item)"
                  :class="{
                    'selected-comment': selectedComment === item,
                  }"
                  class="box text-center d-flex justify-center align-center"
                >
                  <v-row justify="center"
                    ><v-col cols="6" class="text-start font-weight-black">{{
                      item.name
                    }}</v-col
                    ><v-col cols="6" class="text-end font-italic">{{
                      item.date
                    }}</v-col>
                    <v-divider class="mx-3"></v-divider>
                    <v-col>{{ item.comment }}</v-col>
                  </v-row>
                </div>
                <div>
                  <v-btn
                    v-if="selectComment(item)"
                    @click="deleteComment(item)"
                    icon
                  >
                    <v-icon color="red">mdi-delete</v-icon>
                  </v-btn>
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
</template>
<script>
export default {
  props: {
    rowCompliance: {
      type: Number,
      required: true,
    },
  },
  data: () => ({
    prometeon: "#212b59",
    showDrawer: false,
    selectedComment: null,
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
  }),
  methods: {
    toggleCommentSelection(comment) {
      if (this.selectComment(comment)) {
        this.selectedComment = null;
      } else {
        this.selectedComment = comment;
      }
    },
    selectComment(comment) {
      return this.selectedComment === comment;
    },
    deleteComment(comment) {
      const index = this.comments.findIndex((c) => c.id === comment.id);
      if (index !== -1) {
        this.comments.splice(index, 1);
        this.selectedComment = null;
      }
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
  }
};
</script>
<style scoped>
.selected-comment {
  background-color: #cfd8dc !important;
}
</style>