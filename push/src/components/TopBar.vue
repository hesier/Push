<template>
  <v-app-bar app color="primary" dark>

    <div class="d-flex align-center">
      <v-toolbar-title>{{ title }}</v-toolbar-title>
    </div>

  </v-app-bar>

</template>
<script>
export default {
  data() {
    return {
      title: 'Push'
    }
  },
}
</script>
