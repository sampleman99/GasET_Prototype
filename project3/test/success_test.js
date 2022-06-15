const BADPANDAS = artifacts.require("BADPANDAS");
const web3 = require('web3');
contract("BADPANDAS", async(accounts) => {
  var object;
  var owner = accounts[0];
  before(async function() {
    // set contract instance into a variable
    object = await BADPANDAS.new("sample1", "sample2", "sample3", "sample4", {from:owner});
  })

  it("mint_success", async function() {

    var result = await object.pause(false, {from:owner});

    // first except
    result = await object.mint(1, {from:owner});

    var gasUsed = result.receipt.gasUsed;

    console.log('#GASET_GAS#' + gasUsed + '#GASET_GAS#');
  })
});


