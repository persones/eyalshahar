const path = require("path");

module.exports = {
  outputDir: path.resolve(__dirname, "dist"), // public_html for ML server
  //assetsDir: "../../static/SPA"
  publicPath: process.env.NODE_ENV === 'production'
    ? '/eyalshahar/' // was /website/
    : '/'
};
