import { algo } from "@algorandfoundation/algokit-utils";
import { setupLocalnetEnvironment } from "@/algokit-utils-ts/setup-localnet-environment";

async function signingTransactions() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment();

  // example: SIGN_TRANSACTION
  // Set up a default signer for transactions
  // This will be used when no specific signer is provided
  algorand.account.setDefaultSigner(randomAccountA);

  // Register multiple transaction signers at once using the fluent interface
  algorand.account.setSignerFromAccount(randomAccountA).setSignerFromAccount(randomAccountB);

  // Create and send a transaction - it will be automatically signed
  // using the registered signer for randomAccountA
  await algorand.send.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algo(1),
  });
  // example: SIGN_TRANSACTION

  // example: SIGN_TRANSACTION_GROUP
  // Create and send a transaction group - each transaction will be
  // automatically signed using the registered signer for each sender
  await algorand
    .newGroup()
    .addPayment({
      sender: randomAccountA,
      receiver: randomAccountB,
      amount: algo(1),
    })
    .addPayment({
      sender: randomAccountB,
      receiver: randomAccountA,
      amount: algo(0.5),
    })
    .send();
  // example: SIGN_TRANSACTION_GROUP
}

signingTransactions();
