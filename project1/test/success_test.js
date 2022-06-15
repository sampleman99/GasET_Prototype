const FullMoonbirdsContract = artifacts.require("FullMoonbirdsContract");
const web3 = require('web3');
contract("FullMoonbirdsContract", async(accounts) => {
  var object;
  var owner = accounts[0];
  before(async function() {
    // set contract instance into a variable
    object = await FullMoonbirdsContract.new(10, 10, {from:owner});
  })

  // 50,245
  it("Claim_success", async function() {
    
    // first except
    var result = await object.Claim(1, {from:owner});

    var gasUsed = result.receipt.gasUsed;

    console.log('#GASET_GAS#' + gasUsed + '#GASET_GAS#');
  })
});


