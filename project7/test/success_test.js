const UwUNinjas = artifacts.require("UwUNinjas");
const web3 = require('web3');
contract("UwUNinjas", async(accounts) => {
  var object;
  var owner = accounts[0];
  before(async function() {
    // set contract instance into a variable
    object = await UwUNinjas.new({from:owner});
  })

  it("mint_success", async function() {

    // first except
    var result = await object.mint(1, {from:owner});

    var gasUsed = result.receipt.gasUsed;

    console.log('#GASET_GAS#' + gasUsed + '#GASET_GAS#');
  })
});


