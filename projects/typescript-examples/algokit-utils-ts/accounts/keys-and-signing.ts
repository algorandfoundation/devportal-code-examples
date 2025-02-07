import { AlgorandClient, algo } from "@algorandfoundation/algokit-utils";

async function keysAndSigning() {
  /** Initialize an Algorand client instance configured for LocalNet */
  const algorand = AlgorandClient.defaultLocalNet();

  /** Create 3 random accounts */
  const randomAccount = algorand.account.random();
  const randomAccount2 = algorand.account.random();
  const randomAccount3 = algorand.account.random();

  // example: DEFAULT_SIGNER
  /**
   * Set up a default signer for transactions.
   * This will be used when no specific signer is provided.
   */
  algorand.account.setDefaultSigner(randomAccount);
  // example: DEFAULT_SIGNER

  // example: MULTIPLE_SIGNERS
  /**
   * Register multiple transaction signers at once.
   * Demonstrates the fluent interface for registering signers.
   */
  algorand.account.setSignerFromAccount(randomAccount).setSignerFromAccount(randomAccount2).setSignerFromAccount(randomAccount3);
  // example: MULTIPLE_SIGNERS

  // example: GET_SIGNER
  /**
   * Retrieve a transaction signer for a specific address.
   * Returns the registered signer or throws if none is found.
   */
  const signer = algorand.account.getSigner("ACCOUNT_ADDRESS");
  // example: GET_SIGNER
}
