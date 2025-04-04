/* eslint-disable @typescript-eslint/no-unused-vars */
import { algo } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

export async function keysAndSigning() {
  const { algorand, randomAccountA, randomAccountB, randomAccountC } = await setupLocalnetEnvironment()

  // example: DEFAULT_SIGNER
  /**
   * Set up a default signer for transactions.
   * This will be used when no specific signer is provided.
   */
  algorand.account.setDefaultSigner(randomAccountA)
  // example: DEFAULT_SIGNER

  // example: MULTIPLE_SIGNERS
  /**
   * Register multiple transaction signers at once.
   * Demonstrates the fluent interface for registering signers.
   */
  algorand.account
    .setSignerFromAccount(randomAccountA)
    .setSignerFromAccount(randomAccountB)
    .setSignerFromAccount(randomAccountC)
  // example: MULTIPLE_SIGNERS

  // example: GET_SIGNER
  /**
   * Retrieve a transaction signer for a specific address.
   * Returns the registered signer or throws if none is found.
   */
  const signer = algorand.account.getSigner('ACCOUNT_ADDRESS')
  // example: GET_SIGNER

  // example: OVERRIDE_SIGNER
  /**
   * Create an unsigned payment transaction and manually sign it.
   */

  const accountASigner = algorand.account.getSigner('ACCOUNT_ADDRESS')

  const paymentTxn = await algorand.createTransaction.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algo(1),
    note: 'Payment from A to B',
  })

  // The transaction signer can be overridden in the second argument to `addTransaction`
  const txnGroup = algorand.newGroup().addTransaction(paymentTxn, accountASigner)
  await txnGroup.send()

  // example: OVERRIDE_SIGNER
}

keysAndSigning()
