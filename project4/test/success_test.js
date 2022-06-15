const SniperZuki = artifacts.require("SniperZuki");
const web3 = require('web3');
contract("SniperZuki", async(accounts) => {
  var object;
  var owner = accounts[0];
  before(async function() {
    // set contract instance into a variable
    object = await SniperZuki.new("sample1", {from:owner});
  })

  it("mintNFTWhitelist_success", async function() {

    var result = await object.togglePresale({from:owner});

    // first except
    result = await object.mintNFTWhitelist(["0xc2cd3dbc8a11e7bd6823890556344c25fd317267fb60b2667163dd7ae133d09d"], {from:owner});

    var gasUsed = result.receipt.gasUsed;

    console.log('#GASET_GAS#' + gasUsed + '#GASET_GAS#');
  })
});


