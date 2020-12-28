import Vue from 'vue'
import VueRouter from 'vue-router'

import WechatFrom from '@/views/WechatFrom'
import CronList from '@/views/CronList'

Vue.use(VueRouter)

const router = new VueRouter({
    mode: 'history',
    routes: [
        {
            path:"/",
            component: WechatFrom
        },
        {
            path:"/:openId",
            component: WechatFrom
        },
        {
            path:"/list/:openId",
            component: CronList
        },
    ]
})


export default router
