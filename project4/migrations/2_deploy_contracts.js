const SniperZuki = artifacts.require("SniperZuki.sol");

module.exports = function(deployer) {
  deployer.deploy("sample1", SniperZuki);
};
