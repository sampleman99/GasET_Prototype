module.exports = {
  networks: {
    development: {
      host: "localhost",
      port: 8545,
      network_id: "*" // Match any network id
    },
  },
  compilers: {
    solc: {
      version: "^0.8.9",    // Fetch exact version from solc-bin (default: truffle's version)
    }
  }
};
