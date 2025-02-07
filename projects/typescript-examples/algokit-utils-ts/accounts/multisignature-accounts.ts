import { AlgorandClient, algo } from "@algorandfoundation/algokit-utils";

async function multisignatureAccounts() {
  /** Initialize an Algorand client instance configured for LocalNet */
  const algorand = AlgorandClient.defaultLocalNet();

  // example: MULTISIG_ACCOUNT
  /**
   * Create a 1-of-2 multisig account that requires
   * only 1 signature from the 2 possible signers to authorize transactions
   */
  const randomAccount = algorand.account.random();

  const multisigAccount = algorand.account.multisig({ version: 1, threshold: 1, addrs: [randomAccount.addr, "ADDRESS2..."] }, [
    randomAccount.account,
  ]);
  // example: MULTISIG_ACCOUNT
}
