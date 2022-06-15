const GELON = artifacts.require("GELON");
const web3 = require('web3');
contract("GELON", async(accounts) => {
  var object;
  var owner = accounts[0];
  before(async function() {
    // set contract instance into a variable
    object = await GELON.new({from:owner});
  })

  it("manualBurnLiquidityPairTokens_success", async function() {

    // first except

    var result = await object.anualBurnLiquidityPairTokens(50, {from:owner});

    var gasUsed = result.receipt.gasUsed;

    console.log('#GASET_GAS#' + gasUsed + '#GASET_GAS#');
  })
});


