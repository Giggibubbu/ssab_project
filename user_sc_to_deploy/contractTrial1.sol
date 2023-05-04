// SPDX-License-Identifier: MIT
pragma solidity >0.5.0;

    contract Greeter3 {
        string public greeting;
        string public prova;

        constructor(){
            greeting = 'Hello';
        }

        function setGreeting(string memory _greeting) private {
            greeting = _greeting;
        }

        function greet() view public returns (string memory) {
            return greeting;
        }
    }