import { algo } from "@algorandfoundation/algokit-utils";
import { setupLocalnetEnvironment } from "@/setup-localnet-environment";

async function rekeyingAccounts() {
  const { algorand, dispenser, randomAccountA, randomAccountB, randomAccountC } = await setupLocalnetEnvironment();

  // example: REKEY_ACCOUNT
  /**
   * Rekey an account to use a different address for signing.
   * This allows account A to be controlled by account B's private key.
   */
  await algorand.account.rekeyAccount(randomAccountA, randomAccountB);

  // Send a payment transaction from account A
  // which will automatically sign the transaction with account B's private key
  await algorand.send.payment({
    sender: randomAccountA,
    receiver: randomAccountC,
    amount: algo(1),
  });

  // example: REKEY_ACCOUNT
}

rekeyingAccounts();
