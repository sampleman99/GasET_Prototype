# GasET_Prototype

## ASE_2022 NIER

### Project1 ~ 10

Example of Optimized Contract

### Unoptimized Smart Contract 
```
	function mintSaleNFT(uint256 _count) public payable{
		uint256 totalSupply = totalSupply();                                                                 
		require(saleEnable, "Sale is not enable");                                                            // exception 1
    		require(SALE_MINTED + _count <= SALE_NFT, "Exceeds max limit");                                       // exception 2
		require(_count <= MAX_BY_MINT_IN_TRANSACTION,"Exceeds max mint limit per tnx");                       // exception 3
		require(users[msg.sender].salemint + _count <= MAX_MINT_SALE,"Exceeds max mint limit per wallet");    // exception 4
		require(msg.value >= SALE_PRICE * _count,"Value below price");                                        // exception 5
		for (uint256 i = 0; i < _count; i++) {
      			_safeMint(msg.sender, totalSupply + i);
			SALE_MINTED++;
    		}
		users[msg.sender].salemint = users[msg.sender].salemint + _count;
  	}
```

------------

### Optimized Smart Contract
```
	function mintSaleNFT(uint256 _count) public payable{
	    require(_count <= MAX_BY_MINT_IN_TRANSACTION,"Exceeds max mint limit per tnx");                      // exception 3 (2126 gas)
	    require(saleEnable, "Sale is not enable");                                                           // exception 1 (2153 gas)
	    require(msg.value >= SALE_PRICE * _count,"Value below price");                                       // exception 5 (2335 gas)
	    require(SALE_MINTED + _count <= SALE_NFT, "Exceeds max limit");                                      // exception 2 (2420 gas)
	    require(users[msg.sender].salemint + _count <= MAX_MINT_SALE,"Exceeds max mint limit per wallet");   // exception 4 (2515 gas)
	    uint256 totalSupply = totalSupply();                                                             // 24521 gas
		
		for (uint256 i = 0; i < _count; i++) {
      			_safeMint(msg.sender, totalSupply + i);
			SALE_MINTED++;
    		}
		users[msg.sender].salemint = users[msg.sender].salemint + _count;
  	}

```
Optimized Smart Contract located to above (uint256 totalSupply = totalSupply()) and relocated among them

As a result,

### In case of Unoptimized 
totalSupply -> Exception1 -> Exception2 -> Exception3 -> Exception 4-> Exception 5

### In case of Optimized
Exception3 -> Exception 1-> Exception 5-> Exception 2-> Exception 4 -> totalSupply
