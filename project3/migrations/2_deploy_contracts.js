const BADPANDAS = artifacts.require("BADPANDAS.sol");

module.exports = function(deployer) {
  deployer.deploy("sample1", "sample2", "sample3", "sample4", BADPANDAS);
};
