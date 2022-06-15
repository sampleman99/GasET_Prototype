const ROK = artifacts.require("ROK");
const web3 = require('web3');
contract("ROK", async(accounts) => {
  var object;
  var owner = accounts[0];
  before(async function() {
    // set contract instance into a variable
    object = await ROK.new({from:owner});
  })

  it("mintSaleNFT_success", async function() {

    var result = await object.setSaleStatus(true, {from:owner});

    // first except
    result = await object.mintSaleNFT(1, {from:owner});

    var gasUsed = result.receipt.gasUsed;

    console.log('#GASET_GAS#' + gasUsed + '#GASET_GAS#');
  })
});


