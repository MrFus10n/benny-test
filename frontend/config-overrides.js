// noinspection NodeCoreCodingAssistance

// noinspection JSUnresolvedFunction
const BundleTracker = require('webpack-bundle-tracker')
// noinspection JSUnresolvedFunction
const path = require('path')

// noinspection JSUnusedGlobalSymbols
module.exports = {
  webpack: (config, env) => {
    // BundleTracker makes django able to dynamically load bundles
    config.plugins.push(new BundleTracker({
      path: path.join(__dirname, 'build'),
      filename: 'webpack-stats.json',
    }));

    if (env === 'development') {
      // HMR setup
      config.output.publicPath = `http://${process.env.IP}:3000/`

    } else if (env === 'production') {
      config.output.publicPath = '/'
    }
    return config
  },
  devServer: function(configFunction) {
    return function(proxy, allowedHost) {
      const config = configFunction(proxy, allowedHost)
      config.headers = {'Access-Control-Allow-Origin': '*'}
      return config
    }
  },
}
