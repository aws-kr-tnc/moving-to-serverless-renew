const { BundleAnalyzerPlugin } = require('webpack-bundle-analyzer');

module.exports = {
  configureWebpack: {
    plugins: [new BundleAnalyzerPlugin()],
  },
  //For AWS Cloud9 PREVIEW
  devServer: {
    compress: true,
    disableHostCheck: true,
  },
};
