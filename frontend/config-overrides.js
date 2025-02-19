const { override, addWebpackAlias } = require("customize-cra");
const path = require("path");

module.exports = override(
  addWebpackAlias({
    ["@components"]: path.resolve(__dirname, "src/components/"),
    ["@models"]: path.resolve(__dirname, "src/models/"),
    ["@utils"]: path.resolve(__dirname, "src/utils/"),
    ["@lib"]: path.resolve(__dirname, "src/lib/"),
    ["@services"]: path.resolve(__dirname, "src/services/"),
    ["@tests"]: path.resolve(__dirname, "src/tests/"),
  })
);
