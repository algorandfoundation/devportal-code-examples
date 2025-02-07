import { AlgorandClient, algo } from "@algorandfoundation/algokit-utils";

async function fundingAccounts() {
  /** Initialize an Algorand client instance configured for LocalNet */
  const algorand = AlgorandClient.defaultLocalNet();

  // example: DISPENSER_ACCOUNT
  /**
   * Get a dispenser account from environment variables.
   */
  const dispenser = await algorand.account.dispenserFromEnvironment();
  // example: DISPENSER_ACCOUNT

  // example: ENSURE_FUNDED
  /**
   * Ensure an account has sufficient funds by transferring
   * Algos from a dispenser account if needed
   */
  await algorand.account.ensureFunded("ACCOUNTADDRESS", dispenser.addr, algo(1));
  // example: ENSURE_FUNDED
}
