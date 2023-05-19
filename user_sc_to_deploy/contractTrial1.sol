// SPDX-License-Identifier: MIT
pragma solidity >0.5.0;

    contract Greeter3 {
        string public greeting = "ciao";
        string public prova = "ciao";

        constructor(){
            greeting = 'Hello';
        }

        function setGreeting(address newAddress, string calldata setString, uint ciao, int32 ciao1, uint32 ciao2, bool boolean, string[] memory array) public {
            greeting = setString;
        }

        function greet() view public returns (string memory) {
            return greeting;
        }
    }