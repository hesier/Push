<template>

  <div>
    <v-data-table
        :headers="headers"
        :items="desserts"
        class="elevation-1"
        :loading="tableLoading"
        loading-text="正在加载..."
        hide-default-footer
        no-data-text="暂无数据"
    >
      <template v-slot:item.status="{ item }">

        <v-chip v-if="item.status === 'on'" color="green" dark>
          {{ item.status }}
        </v-chip>
        <v-chip v-else color="red" dark>
          {{ item.status }}
        </v-chip>
      </template>

      <template v-slot:item.actions="{ item }">
        <v-icon  v-if="item.status === 'off'" class="mr-2" @click="startJob(item.uid)">
          mdi-play
        </v-icon>
        <v-icon  v-if="item.status === 'on'" class="mr-2" @click="stopJob(item.uid)">
          mdi-stop
        </v-icon>
        <v-icon  @click="removeConfirm(item.uid)">
          mdi-delete
        </v-icon>


      </template>

    </v-data-table>

    <Message ref="message" />

    <v-dialog v-model="removeDialog" max-width="290">
      <v-card>
        <v-card-title class="headline">警告</v-card-title>
        <v-card-text>确定要删除此任务吗？</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue darken-1" text @click="removeDialog = false">取消</v-btn>
          <v-btn color="red darken-1" text @click="removeJob()">确定</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

  </div>
</template>
<script>

import Message from '@/components/Message'

export default {

  name: "CronList",

  components: {
    Message,
  },

  data () {
    return {

      tableLoading: false,

      removeUid: '',
      removeDialog: false,

      openId: '',

      headers: [
        // { text: 'id', align: 'start', sortable: false, value: 'uid', width: '200' },
        { text: '添加时间', sortable: false, value: 'create_time', width: '150' },
        { text: '上次推送时间', sortable: false, value: 'run_time', width: '150' },
        { text: 'cron 表达式', sortable: false, value: 'cron', width: '100'  },
        { text: '状态', sortable: false, value: 'status', width: '80'  },
        { text: '内容', sortable: false, value: 'content' },
        { text: '操作', sortable: false, value: 'actions', width: '100'  },
      ],
      desserts: [],

      url: {
        list: '/push/get/',
        start: '/push/resume/',
        stop: '/push/pause/',
        remove: '/push/remove/',
      }
    }
  },

  mounted() {
    this.openId = this.$route.params.openId!==undefined?this.$route.params.openId:''
    if (this.openId !== '') {
      this.refreshList()
    }
  },

  methods: {
    refreshList() {
      if (this.openId !== '') {
        this.tableLoading = true
        this.$axios.get(this.url.list + this.openId).then(res => {
          if (res.data.code === 0) {
            this.desserts = res.data.data
          } else {
            this.$emit('error', res.data.msg);
          }
        }).catch(() => {
          this.$emit('error', '服务出错！');
        }).then(() => {
          this.tableLoading = false
        });

      } else {
        this.$emit('error', '当前用户 openId 不存在！');
      }
    },

    startJob(uid) {

      this.$axios.post(this.url.start + this.openId, {uid: uid}).then(res => {
        if (res.data.code === 0) {
          this.$emit('success', '开启任务成功');
          this.refreshList()
        } else {
          this.$emit('error', res.data.msg);
        }
      }).catch(() => {
        this.$emit('error', '服务出错！');
      })

    },
    stopJob(uid) {
      this.$axios.post(this.url.stop + this.openId, {uid: uid}).then(res => {
        if (res.data.code === 0) {
          this.$emit('success', '停止任务成功');
          this.refreshList()
        } else {
          this.$emit('error', res.data.msg);
        }
      }).catch(() => {
        this.$emit('error', '服务出错！');
      })
    },

    removeConfirm(uid) {
      this.removeUid = uid
      this.removeDialog = true
    },

    removeJob() {

      this.removeDialog = false

      this.$axios.post(this.url.remove + this.openId, {uid: this.removeUid}).then(res => {
        if (res.data.code === 0) {
          this.$emit('success', '删除任务成功');
          this.refreshList()
        } else {
          this.$emit('error', res.data.msg);
        }
      }).catch(() => {
        this.$emit('error', '服务出错！');
      })
    },
  }



}
</script>



<style scoped>

</style>
