const merge = require('webpack-merge');
const baseConfig = require('./core.webpack.js');


module.exports = merge(baseConfig, {
    mode: 'development',
    devtool: 'eval',
    watch: true,
    output: {
        filename: '[name].bundle.js',
        path: __dirname + '../server/core/static/js/',
    },
    devServer: {
        host: '0.0.0.0',
        port: 3000,
        inline: true,
        hot: true,
        historyApiFallback: true,
        proxy: {
            '/api':  'http://server:9000'
        }
    },
})
