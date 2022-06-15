// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./ERC721A.sol";
import "./Ownable.sol";

contract Coomers is ERC721A, Ownable {
    using Strings for uint256;

    string public baseURI;
    uint256 public price = 0.002 ether;
    uint256 public maxPerTx = 10;
    uint256 public totalFree = 2000;
    uint256 public maxSupply = 7777;
    uint256 public maxPerWallet = 80;
    uint256 public maxFreePerWallet = 20;
    bool public mintEnabled = true;
    mapping(address => uint256) private _mintedFreeAmount;

    constructor() ERC721A("Red Candle Heros", "Coomers") {
        _safeMint(msg.sender, 5);
    }

    function mint(uint256 amt) external payable {
        uint256 cost = price;
        bool isFree = (totalSupply() + amt < totalFree + 1) &&
            (_mintedFreeAmount[msg.sender] + amt <= maxFreePerWallet);
        if (isFree) {
            cost = 0;
        }

        require(msg.value >= amt * cost, "Please send the exact amount.");
        require(totalSupply() + amt < maxSupply + 1, "No more Coomers");
        require(mintEnabled, "Minting is not live yet, hold on Coomers.");
        require(amt < maxPerTx + 1, "Max per TX reached.");
        require(_numberMinted(msg.sender) + amt <= maxPerWallet,"Too many per wallet!");

        if(isFree) {
            _mintedFreeAmount[msg.sender] += amt;
        }

        _safeMint(msg.sender, amt);
    }

    function _baseURI() internal view virtual override returns (string memory) {
        return baseURI;
    }

    function tokenURI(uint256 tokenId)
        public
        view
        virtual
        override
        returns (string memory)
    {
        require(
            _exists(tokenId),
            "ERC721Metadata: URI query for nonexistent token"
        );
        return string(abi.encodePacked("https://gateway.pinata.cloud/ipfs/QmQfZZcYhMKcEWe9GYS5g6oKjnAXEsCtGHz7CytRiX2aVZ/", tokenId.toString()));
    }

    function setBaseURI(string memory uri) public onlyOwner {
        baseURI = uri;
    }

    function setFreeAmount(uint256 amount) external onlyOwner {
        totalFree = amount;
    }

    function setPrice(uint256 _newPrice) external onlyOwner {
        price = _newPrice;
    }

    function flipSale() external onlyOwner {
        mintEnabled = !mintEnabled;
    }

    function withdraw() external onlyOwner {
        (bool success, ) = payable(msg.sender).call{
            value: address(this).balance
        }("");
        require(success, "Transfer failed.");
    }
}
