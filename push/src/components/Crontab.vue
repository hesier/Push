<template>
  <v-dialog
      v-model="show"
      persistent
      max-width="800px"
  >
    <v-card>

      <v-card-title>
        <span class="headline">cron 表达式</span>
      </v-card-title>

      <v-container>

        <VueCronEditorBuefy
            v-model="cronExpression"
            locale="zh_CN"
            :preserveStateOnSwitchToAdvanced="true"
            :custom-locales="{zh_CN :zh_CN}"
        />

        <br>
        <p> cron 表达式：{{cronExpression}}</p>
        <p> 执行计划：{{cronResult}}</p>

      </v-container>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="blue darken-1" text @click="show = false">
          取消
        </v-btn>
        <v-btn color="blue darken-1" text @click="handleOk">
          确定
        </v-btn>
      </v-card-actions>
    </v-card>

  </v-dialog>

</template>

<script>
import VueCronEditorBuefy from 'vue-cron-editor-buefy';
import cronstrue from 'cronstrue/i18n';

export default {
  name: 'Crontab',
  components: {
    VueCronEditorBuefy
  },
  data: () => ({

    cronResult: '',

    show: false,

    zh_CN: {
      every: "每隔",
      mminutes: "分钟",
      hoursOnMinute: "小时，在：",
      daysAt: "天，在",
      at: "在",
      onThe: "在",
      dayOfEvery: "日，每隔",
      monthsAt: "月，在",
      everyDay: "每周",
      mon: "一",
      tue: "二",
      wed: "三",
      thu: "四",
      fri: "五",
      sat: "六",
      sun: "日",
      hasToBeBetween: "位于",
      and: "和",
      minutes: "分",
      hourly: "时",
      daily: "天",
      weekly: "周",
      monthly: "月",
      advanced: "自定义",
      cronExpression: "cron 表达式:"
    },
    cronExpression: "*/1 * * * *"
  }),

  watch: {

    'cronExpression': function (val) {
      if (val === null || val === '' || val === undefined) {
        this.cronResult = ''
      } else {
        this.cronResult = cronstrue.toString(val, { locale: "zh_CN", use24HourTimeFormat: true })
      }
    }

  },

  methods: {
    handleOk() {
      this.$emit('modalOk', this.cronExpression);
      this.show = false
    }

  },

};
</script>
