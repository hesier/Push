module.exports = {
  productionSourceMap: false,  // 不生成 js.map 文件
  devServer: {
    disableHostCheck: true,  // Invalid Host header
    port: 8080,
    proxy: {
      '/push': {
        target: 'http://localhost:5000', //请求后台
        changeOrigin: true,
        pathRewrite: {
          '^/push': ''
        }
      },
    }
  },
  "transpileDependencies": [
    "vuetify"
  ]
}
