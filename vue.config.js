const path = require("path");

module.exports = {
  outputDir: path.resolve(__dirname, "public_html"),
  //assetsDir: "../../static/SPA"
  publicPath: process.env.NODE_ENV === 'production'
    ? '/website2021/' // was /website/
    : '/'
};
