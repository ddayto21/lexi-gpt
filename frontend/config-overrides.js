const { override, addWebpackAlias } = require("customize-cra");
const path = require("path");

module.exports = override(
  addWebpackAlias({
    ["@components"]: path.resolve(__dirname, "src/components/"),
    ["@utils"]: path.resolve(__dirname, "src/utils/"),
    ["@services"]: path.resolve(__dirname, "src/services/"),
    ["@tests"]: path.resolve(__dirname, "src/tests/"),
  })
);
