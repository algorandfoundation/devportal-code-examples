import { algo } from "@algorandfoundation/algokit-utils";
import { setupLocalnetEnvironment } from "@/algokit-utils-ts/setup-localnet-environment";

async function leases() {
  const { algorand, randomAccountA, randomAccountB, randomAccountC } = await setupLocalnetEnvironment();

  // example: LEASE
  // Create a lease value - this could be any unique string or Uint8Array
  const lease: string | Uint8Array = "unique-lease-value";

  // Send a payment transaction with a lease
  // If another transaction with the same lease and sender tries to execute within the validity window,
  // it will be rejected
  await algorand.send.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algo(1),
    lease: lease,
    // Optional: Set a custom validity window for the lease
    validityWindow: 100, // Number of rounds the lease is valid for
  });

  // Attempting to send another transaction with the same lease and sender within the validity window
  // will cause the transaction to be rejected
  try {
    await algorand.send.payment({
      sender: randomAccountA, // Same sender as first transaction
      receiver: randomAccountC,
      amount: algo(10),
      lease: lease,
      suppressLog: true, // Prevent AlgoKit Utils from logging the expected error
    });
  } catch (error) {
    console.log("Transaction rejected due to active lease");
  }
  // example: LEASE
}

leases();
