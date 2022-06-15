const FullMoonbirdsContract = artifacts.require("FullMoonbirdsContract.sol");

module.exports = function(deployer) {
  deployer.deploy(FullMoonbirdsContract, 10, 10);
};
