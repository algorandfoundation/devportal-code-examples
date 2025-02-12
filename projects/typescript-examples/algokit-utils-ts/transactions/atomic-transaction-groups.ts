import { algo } from "@algorandfoundation/algokit-utils";
import { setupLocalnetEnvironment } from "@/setup-localnet-environment";

async function atomicTransactionGroups() {
  const { algorand, randomAccountA, randomAccountB, randomAccountC } = await setupLocalnetEnvironment();

  // example: ATOMIC_GROUP
  // Create a transaction group that will execute atomically
  // Either all transactions succeed, or they all fail
  await algorand
    .newGroup()
    // First transaction: Payment from A to B
    .addPayment({
      sender: randomAccountA,
      receiver: randomAccountB,
      amount: algo(1),
      note: "First payment in atomic group",
    })
    // Second transaction: Payment from B to C
    .addPayment({
      sender: randomAccountB,
      receiver: randomAccountC,
      amount: algo(0.5), // B sends half of what they received to C
      note: "Second payment in atomic group",
    })
    // Send the atomic group of transactions
    .send();
  // example: ATOMIC_GROUP

  // example: ATOMIC_GROUP_SIMULATE
  // Create a transaction group to simulate
  // Simulation allows you to test the transaction without committing it to the chain
  const group = algorand
    .newGroup()
    .addPayment({
      sender: randomAccountA,
      receiver: randomAccountB,
      amount: algo(1),
    })
    .addPayment({
      sender: randomAccountB,
      receiver: randomAccountC,
      amount: algo(0.5),
    });

  // Simulate the transaction group to:
  // - Verify it will succeed
  // - Understand its effects
  // - Get execution costs
  // - Debug any issues
  const simulateResult = await group.simulate();
  const txnGroup = simulateResult.simulateResponse.txnGroups[0];

  console.log("Simulation results:", {
    round: simulateResult.simulateResponse.lastRound,
    success: !txnGroup.failureMessage,
    error: txnGroup.failureMessage || "None",
  });

  // If simulation succeeds, send the actual transaction
  await group.send();
  // example: ATOMIC_GROUP_SIMULATE
}

atomicTransactionGroups();
