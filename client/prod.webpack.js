const path = require('path');
const merge = require('webpack-merge');
const CleanWebpackPlugin = require('clean-webpack-plugin');

const baseConfig = require('./core.webpack.js');


const outputDirectory = 'dist';


module.exports = merge(baseConfig, {
    mode: 'production',
    devtool: 'source-map',
    optimization: {
        minimize: false
    },
    output: {
        path: path.join(__dirname, outputDirectory),
        filename: 'bundle.js'
    },
    plugins: [
        new CleanWebpackPlugin([outputDirectory]),
    ]
})
