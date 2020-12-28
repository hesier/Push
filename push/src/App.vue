<template>
  <v-app>
    <top-bar/>

    <v-main>
      <v-container class="lighten-5 mb-6">
        <router-view></router-view>
      </v-container>
    </v-main>

  </v-app>
</template>

<script>
import TopBar from './components/TopBar';

export default {
  name: 'App',

  components: {
    TopBar,
  },

  data: () => ({
    //
  }),
};
</script>
