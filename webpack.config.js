const autoprefixer = require('autoprefixer');

/*** Main General Bundle ***/

// Creates the general bundle
var wpBundle = new Object({
    entry: [
        './instance/js/swing_firebase-api-init.js',
        './static/css/swing_app.scss',
        './static/js/swing_firebase.js',
        './static/js/swing_app.js'
    ],
    output: {
        filename: 'static/js/bundle/swing-bundle.js',
        library: 'swcms',
        libraryTarget: 'var',
        path: __dirname
    },
    module: {
        rules: [
            {
                test: /\.js$/,
                loader: 'babel-loader',
                query: {
                    presets: [
                        [
                            '@babel/preset-env', {
                                'useBuiltIns': 'entry',
                                'corejs': {'version': '3', 'proposals': true},
                            }
                        ]
                    ],
                },
            },
            {
                test: /\.scss$/,
                use: [
                    { loader: 'file-loader',
                        options: {
                            name: 'static/css/bundle/swing-bundle.css',
                        },
                    },
                    { loader: 'extract-loader' },
                    { loader: 'css-loader' },
                    { loader: 'postcss-loader',
                        options: {
                            plugins: () => [autoprefixer()]
                        },
                    },
                    { loader: 'sass-loader',
                        options: {
                            // Prefer Dart Sass
                            implementation: require('sass'),
                            sassOptions: {
                                includePaths: ['./node_modules'],
                            },
                            webpackImporter: false,
                        }
                    }
                ]
            }
        ]
    }
});

/*** Specific Bundles ***/

/*** Compilation of Bundles ***/

// Compile all modules
module.exports = [
    wpBundle
];
