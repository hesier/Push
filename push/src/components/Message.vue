<template>
  <v-snackbar
      v-model="showMessage"
      :timeout="timeout"
      right
      top
      :color="color"
  >
    {{ message }}

    <template v-slot:action="{ attrs }">
      <v-icon v-bind="attrs" class="mr-2" @click="showMessage = false">
        mdi-close
      </v-icon>
    </template>

  </v-snackbar>
</template>

<script>
export default {

  name: "Message",

  data: () => ({
    message: '',
    showMessage: false,
    timeout: 3000,
    color: ''
  }),

  methods: {
    success(message) {
      this.color = 'success'
      this.message = message
      this.showMessage = true
    },
    error(message) {
      this.color = 'error'
      this.message = message
      this.showMessage = true
    }
  },

}
</script>

<style scoped>

</style>
