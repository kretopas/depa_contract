const {
  defineConfig
} = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  configureWebpack: {
    module: {
      rules: [{
        test: /\.(jpg|png|gif|svg|pdf)$/,
        loader: 'file-loader',
        options: {
          name: '[name].[ext]',
          outputPath: './assets/'
        }
      }, ]
    }
  }
})