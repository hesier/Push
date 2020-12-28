<template>

  <v-card>

    <v-card-title>添加推送</v-card-title>

      <v-form ref="form" v-model="valid" lazy-validation>

        <v-container>

          <v-text-field
              v-model="openId"
              :rules="rules.openId"
              label="微信 openId"
              required></v-text-field>

          <v-row>

            <v-col cols="12" sm="11">

              <v-text-field
                  v-model="wechat.message"
                  :rules="rules.message"
                  :counter="400"
                  label="推送内容"
                  required></v-text-field>
            </v-col>

            <v-col cols="12" sm="1">
              <v-btn color="success" class="pa-2" @click="pushNow">
                立即推送
              </v-btn>
            </v-col>
          </v-row>


          <v-radio-group v-model="pushType" row>
            <v-radio label="单次推送" value="one"></v-radio>
            <v-radio label="cron 推送" value="cron"></v-radio>
          </v-radio-group>


          <v-row v-show="pushType === 'one'">

            <v-col cols="12" sm="6">

              <v-dialog
                  ref="dateDialog"
                  v-model="dateModal"
                  :return-value.sync="wechat.date"
                  persistent
                  width="290px">

                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                      v-model="wechat.date"
                      label="选择日期"
                      prepend-icon="mdi-calendar"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                  ></v-text-field>
                </template>
                <v-date-picker
                    v-model="wechat.date"
                    :first-day-of-week="1"
                    locale="zh-cn"
                >
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="dateModal = false">
                    取消
                  </v-btn>
                  <v-btn text color="primary" @click="$refs.dateDialog.save(wechat.date)">
                    确定
                  </v-btn>
                </v-date-picker>
              </v-dialog>

            </v-col>
            <v-col cols="12" sm="6">

              <v-dialog
                  ref="timeDialog"
                  v-model="timeModal"
                  :return-value.sync="wechat.time"
                  persistent
                  width="290px"
              >
                <template v-slot:activator="{ on, attrs }">
                  <v-text-field
                      v-model="wechat.time"
                      label="选择时间"
                      prepend-icon="mdi-clock-time-four-outline"
                      readonly
                      v-bind="attrs"
                      v-on="on"
                  ></v-text-field>
                </template>
                <v-time-picker
                    v-if="timeModal"
                    v-model="wechat.time"
                    format="24hr"
                    full-width
                >
                  <v-spacer></v-spacer>
                  <v-btn text color="primary" @click="timeModal = false">
                    取消
                  </v-btn>
                  <v-btn text color="primary" @click="$refs.timeDialog.save(wechat.time)">
                    确定
                  </v-btn>
                </v-time-picker>
              </v-dialog>

            </v-col>

          </v-row>

          <v-text-field v-show="pushType === 'cron'"
              v-model="wechat.cron"
              label="cron 表达式"
              readonly
              @click="cronClick(wechat.cron)"
              required></v-text-field>

          <Crontab ref="cronModal" @modalOk="cronModalOk"/>

          <v-btn color="success" class="mr-4" @click="submit">
            提交
          </v-btn>

          <v-btn color="error" class="mr-4" @click="restore">
            清空
          </v-btn>

        </v-container>
      </v-form>


    <v-container>

      <v-card-title>cron 推送列表</v-card-title>

      <v-btn class="mr-4" @click="refreshCronList">
        刷新
      </v-btn>
      <br>

      <cron-list ref="cronList" @error="errorMessage" @success="successMessage" />

    </v-container>

    <Message ref="message"/>

  </v-card>

</template>

<script>
import Crontab from '@/components/Crontab'
import Message from '@/components/Message'
import CronList from '@/views/CronList'

export default {
  name: 'WechatFrom',

  components: {
    Crontab,
    Message,
    CronList,
  },

  data: () => ({

    pushType: 'one',

    dateModal: false,
    timeModal: false,

    openId: '',

    valid: false,
    wechat: {
      message: '',
      date: '',
      time: '',
      cron: '',
    },

    rules: {
      openId: [
        v => !!v || "微信 openId 不能为空",
      ],
      message: [
        v => !!v || "推送内容不能为空",
      ],
    },

    url: {
      addTime: '/push/time/',
      addNow: '/push/now/',
      addCron: '/push/cron/',
    }
  }),

  mounted() {
    this.openId = this.$route.params.openId!==undefined?this.$route.params.openId:''
  },

  methods: {
    submit() {

      if (!this.$refs.form.validate()) {
        return
      }

      let url = this.openId
      let params = { message: this.wechat.message }
      if (this.pushType === 'one') {  // 单次推送
        url = this.url.addTime + url
        if (this.wechat.date !== '' && this.wechat.time !== '') {
          params.time = this.wechat.date + ' ' + this.wechat.time + ':00'
        } else {
          this.errorMessage('请选择日期和时间！');
          return;
        }
      } else {  // cron 推送
        url = this.url.addCron + url
        if (this.wechat.cron !== '') {
          params.cron = this.wechat.cron
        } else {
          this.errorMessage('请选择cron 表达式！');
          return;
        }
      }

      this.$axios.post(url, params).then(res => {
        if (res.data.code === 0) {
          this.successMessage('添加推送成功');
          if (this.pushType === 'cron') {
            this.refreshCronList()
          }
        } else {
          this.errorMessage(res.data.msg);
        }
      }).catch(() => {
        this.errorMessage('服务出错！');
      })

    },

    pushNow() {

      this.$axios.get(this.url.addNow + this.openId + '/' + encodeURIComponent(this.wechat.message)).then(res => {
        if (res.data.code === 0) {
          this.successMessage('推送成功');
        } else {
          this.errorMessage(res.data.msg);
        }
      }).catch(() => {
        this.errorMessage('服务出错！');
      })

    },

    restore() {
      this.wechat = {
        message: '',
        date: '',
        time: '',
        cron: '',
      }
    },

    cronModalOk(cron) {
      this.wechat.cron = cron
    },

    refreshCronList() {
      this.$refs.cronList.openId = this.openId;
      this.$refs.cronList.refreshList()
    },

    cronClick(value) {
      this.$refs.cronModal.show = true;
      console.log(value)
      this.$refs.cronModal.cronExpression = value;
    },

    successMessage(message) {
      this.$refs.message.success(message)
    },
    errorMessage(message) {
      this.$refs.message.error(message)
    },
  },

}
</script>
