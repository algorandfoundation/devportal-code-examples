import { algo } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function rekeyingAccounts() {
  const { algorand, randomAccountA, randomAccountB, randomAccountC } = await setupLocalnetEnvironment()

  // example: REKEY_ACCOUNT
  /**
   * Rekey an account to use a different address for signing.
   * This allows account A to be controlled by account B's private key.
   */
  await algorand.account.rekeyAccount(randomAccountA, randomAccountB)

  // Send a payment transaction from account A
  // which will automatically sign the transaction with account B's private key
  await algorand.send.payment({
    sender: randomAccountA,
    receiver: randomAccountC,
    amount: algo(1),
  })

  const unsigned_payment_txn = await algorand.createTransaction.payment({
    sender: randomAccountA,
    receiver: randomAccountC,
    amount: algo(1),
  })

  /**
   * The unsigned transaction can be signed by the signer when sending with the `add_transaction` method.
   */
  const result = await algorand.newGroup().addTransaction(unsigned_payment_txn, randomAccountB.signer).send()

  console.log(result.txIds)
  // example: REKEY_ACCOUNT
}

rekeyingAccounts()
