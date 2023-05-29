// SPDX-License-Identifier: MIT
pragma solidity >0.5.0;

    contract Greeter3 {
        string public greeting = "ciao";
        string public prova = "ciao";

        constructor(){
            greeting = 'Hello';
        }

        function setGreeting( string calldata setString, int x, uint32 y, address z) public {
            greeting = setString;
        }

        function greet() view public returns (string memory) {
            return greeting;
        }
    }