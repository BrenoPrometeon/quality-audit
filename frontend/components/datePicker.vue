<template>
  <v-row
    justify="center"
    v-for="type in [
      { text: 'Data', value: 'Date' }
    ]"
    class="mx-10"
  >
    <v-col cols="12" class="text-center text-overline">{{ type.text }}</v-col>
    <v-col
      class="text-overline text-center"
      cols="4"
      v-for="d in [{title: 'Previsão', value: 'prev'}, {title: 'Efetivo', value: 'effective'}]"
      ><v-row justify="center"> {{ d.title }}</v-row
      ><v-row justify="center"
        ><v-col class="text-h6"
          ><n-date-picker
            v-model:formatted-value="value[d['value'] + type.value]"
            type="date"
            value-format="dd/MM/yyyy"
            size="large"
            clearable
            placeholder="Selecione uma data" /></v-col
      ></v-row> </v-col
    >
  </v-row>
</template>
<script setup>
import { reactive } from "vue";


const props = defineProps({
    modelValue: { required: false },
});

var value = reactive(props.modelValue);

watch(
    () => ({ ...value }),
    (newValue, oldValue) => {
      if (oldValue.prevDate != newValue.prevDate) value.effectiveDate = null;
      console.log(newValue, oldValue)
      // if(newValue.prevDate === null && newValue.effectiveDate === null)  console.log('Hello')
      emit("update:modelValue", newValue);
    },
    { deep: true }
);

const emit = defineEmits(["update:modelValue", "value"]);

defineExpose({
  value,
});


</script>
