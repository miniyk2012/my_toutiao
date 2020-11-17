const glob = require('glob')
const path = require('path')
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const config = {
    plugins: [new MiniCssExtractPlugin()],
    entry: glob.sync('./src/**/*.js').reduce(
        (entries, entry) => Object.assign(entries, {[entry.split('/').pop().replace('.js', '')]: entry}), {}),

    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                test: /\.css$/i,
                use: [MiniCssExtractPlugin.loader, 'css-loader'],
            },
            {
                test: /\.scss$/,
                use: [
                    "style-loader",
                    "css-loader",
                    "sass-loader"
                ]
            }
        ]
    },

    output: {
        filename: '[name].js',
        path: path.join(__dirname, 'static/dist')
    }
}

module.exports = config
