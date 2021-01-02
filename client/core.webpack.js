const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CleanWebpackPlugin = require('clean-webpack-plugin');


const outputDirectory = 'core/static';


module.exports = {
    entry: {
        app: ['babel-polyfill', './index.js'],
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            "@babel/preset-env",
                            "@babel/preset-react",
                        ],
                        plugins: ["@babel/plugin-transform-react-jsx"]
                    }
                }
            },
            {
                test: /\.(scss)$/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                        options: {
                            modules: true,
                            camelCase: true,
                            localIdentName: '[name]__[local]--[hash:base64:5]',
                        }
                    },
                    {
                        loader: 'postcss-loader', // Run post css actions
                        options: {
                            plugins: [
                                require('precss'),
                                require('autoprefixer')
                            ]
                        }
                    },
                    {
                        loader: 'sass-loader'
                    },
                    {
                        loader: 'sass-resources-loader',
                        options: {
                            resources: ['./app/global.scss']

                        }
                    },
                ]
            },
            {
                test: /\.(css)$/,
                use: [
                    'style-loader',
                    {
                        loader: 'css-loader',
                    },
                ]
            },
            {
                test: /\.(png|woff|woff2|eot|ttf|svg)$/,
                loader: 'url-loader?limit=100000'
            }
        ]
    },
    resolve: {
        extensions: ['.jsx', '.js'],
        alias: {
            services: path.resolve(__dirname, 'services/'),
            actions: path.resolve(__dirname, 'redux/actions/'),
            app: path.resolve(__dirname, 'app/'),

        }
    },
    plugins: [
        // new CleanWebpackPlugin([outputDirectory]),
        // new HtmlWebpackPlugin({
        //     template: './src/react/index.html',
        //     favicon: './src/react/static/favicon.ico'
        // })
    ]
};
