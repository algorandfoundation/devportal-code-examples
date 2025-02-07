import { AlgorandClient, algo } from "@algorandfoundation/algokit-utils";

async function rekeyingAccounts() {
  /** Initialize an Algorand client instance configured for LocalNet */
  const algorand = AlgorandClient.defaultLocalNet();

  // example: REKEY_ACCOUNT
  /**
   * Rekey an account to use a different address for signing.
   * This allows account A to be controlled by account B's private key.
   */
  const rekeyedAccount = await algorand.account.rekeyAccount("ACCOUNT_ADDRESS", "NEW_SIGNER_ADDRESS");
  // example: REKEY_ACCOUNT
}
