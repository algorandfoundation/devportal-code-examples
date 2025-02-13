# Python Smart Contract Contributing Guide

Each code example should have its own contract folder under the `smart_contracts` directory. So for example, the code examples for inner transactions live in the `./smart_contracts/inner_transactions` folder.

Follow this step to add new code examples:
1. Generate a smart contract folder by running `algokit generate smart-contract` at the root of this repository. 
2. Name the folder relevant to the dev portal page the code examples will go to. 
3. Edit the respective `deploy_config.py` file to only deploy the smart contract.
4. Write robust integration test under the `tests` directory. Name it `{CONTRACT_NAME}.integration.test.py`
