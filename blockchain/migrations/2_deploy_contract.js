const HealthCompute = artifacts.require("HealthCompute");

module.exports = function (deployer) {
  deployer.deploy(HealthCompute);
};
