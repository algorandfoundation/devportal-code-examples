import { AlgorandClient, algo } from "@algorandfoundation/algokit-utils";

async function fundingAccounts() {
  /** Initialize an Algorand client instance configured for LocalNet */
  const algorand = AlgorandClient.defaultLocalNet();

  // example: LOCALNET_DISPENSER
  /**
   * Get the default LocalNet dispenser account that can be used to fund other accounts
   */
  const localNetDispenser = await algorand.account.localNetDispenser();
  // example: LOCALNET_DISPENSER

  // example: DISPENSER_ACCOUNT
  /**
   * Get a dispenser account from environment variables.
   */
  const environmentDispenser = await algorand.account.dispenserFromEnvironment();
  // example: DISPENSER_ACCOUNT

  // example: ENSURE_FUNDED
  /**
   * Ensure an account has sufficient funds by transferring
   * Algos from a dispenser account if needed
   */
  await algorand.account.ensureFunded("ACCOUNTADDRESS", localNetDispenser, algo(1));
  // example: ENSURE_FUNDED

  // example: ENSURE_FUNDED_FROM_ENV
  /**
   * Ensure an account has sufficient funds using a dispenser account
   * loaded from environment variables
   */
  await algorand.account.ensureFundedFromEnvironment("ACCOUNTADDRESS", algo(1));
  // example: ENSURE_FUNDED_FROM_ENV

  // example: ENSURE_FUNDED_TESTNET
  /**
   * Ensure an account has sufficient funds using the TestNet Dispenser API
   * The dispenser client uses the `ALGOKIT_DISPENSER_ACCESS_TOKEN` environment variable
   * to authenticate with the dispenser API.
   */
  const dispenserClient = algorand.client.getTestNetDispenserFromEnvironment();
  await algorand.account.ensureFundedFromTestNetDispenserApi("ACCOUNTADDRESS", dispenserClient, algo(1));
  // example: ENSURE_FUNDED_TESTNET

  // example: TESTNET_DISPENSER_FUND
  /**
   * Directly fund an account using the TestNet Dispenser API
   */
  const testnetDispenser = algorand.client.getTestNetDispenserFromEnvironment();
  await testnetDispenser.fund("ACCOUNTADDRESS", 1_000_000);
  // example: TESTNET_DISPENSER_FUND
}

fundingAccounts();
