import { algo } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function multisignatureAccounts() {
  // Initialize an Algorand client instance and get funded accounts
  const { algorand, dispenser, randomAccountA, randomAccountB, randomAccountC } = await setupLocalnetEnvironment()

  // example: MULTISIG_ACCOUNT
  // Create a 2-of-3 multisig account that requires
  // only 2 signatures from the 3 possible signers to authorize transactions
  const multisigAccountA = algorand.account.multisig(
    { version: 1, threshold: 2, addrs: [randomAccountA, randomAccountB, randomAccountC] },
    [randomAccountA.account, randomAccountB.account, randomAccountC.account],
  )

  // Fund the multisig account
  await algorand.account.ensureFunded(multisigAccountA, dispenser, (10).algo())

  // Send a payment transaction from the multisig account
  // which will automatically collect the required number of signatures
  // from the signing accounts provided when creating the multisig account
  await algorand.send.payment({
    sender: multisigAccountA,
    receiver: randomAccountA,
    amount: algo(1),
  })
  // example: MULTISIG_ACCOUNT;
}

multisignatureAccounts()
