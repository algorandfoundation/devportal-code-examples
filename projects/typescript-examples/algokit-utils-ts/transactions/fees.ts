import { microAlgos, algos } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '../setup-localnet-environment'

import { InnerTransactionsFactory } from '../../contracts/artifacts/clients/InnerTransactions/InnerTransactionsClient'
import { OnSchemaBreak, OnUpdate } from '@algorandfoundation/algokit-utils/types/app'

export async function fees() {
  const { algorand, dispenser, randomAccountA, randomAccountB } = await setupLocalnetEnvironment()

  // example: SUGGESTED_PARAMS
  /**
   * Get the suggested parameters for a transaction
   *
   * Returns an object with the following attributes:
   * - consensusVersion: The consensus version of the network
   * - fee: The fee per byte for the transaction
   * - firstValid: The first valid block round
   * - flatFee: Whether the fee is a flat fee
   * - genesisID: The genesis name of the network
   * - genesisHash: The genesis hash of the network
   * - lastValid: The last valid block round
   * - minFee: The minimum fee for the transaction
   */

  const sp = await algorand.getSuggestedParams()

  console.log('Minimum Fee: ', sp.minFee)
  console.log('Fee: ', sp.fee)
  console.log('Flat Fee: ', sp.flatFee)
  // example: SUGGESTED_PARAMS

  // Get all attributes and print them
  console.log(JSON.stringify(sp, null, 2))

  // example: MAX_FEE
  /**
   * The Algorand client automatically gets the suggested parameters and cache them.
   * This transaction will use the suggested fee from algod and it will fluctuate when
   * the network is congested. Ensure to set a max fee to avoid paying more than expected.
   */
  await algorand.createTransaction.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algos(1),
    maxFee: microAlgos(Number(sp.minFee) * 3), // set the max fee to 3 times the minimum fee
  })
  // example: MAX_FEE

  // example: FLAT_FEE
  /**
   * Set a static fee to the transaction.
   * This transaction will use 2000 microAlgo no matter the network conditions
   * and may fail if the network is congested.
   */
  await algorand.createTransaction.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algos(1),
    staticFee: microAlgos(2000), // set the fee to 2000 microAlgo
  })

  /**
   * Or get the suggested parameters and directly configure the flat fee to true
   * and set the fee to 2000 microAlgo.
   */
  const sp2 = await algorand.getSuggestedParams()

  sp2.flatFee = true
  sp2.fee = 2000

  // Cache the configured suggested parameters and use it for future transactions
  algorand.setSuggestedParamsCache(sp2)
  // example: FLAT_FEE

  // example: FEE_POOLING
  // Transaction A will not pay any fees
  const transactionA = await algorand.createTransaction.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algos(2),
    staticFee: algos(0), // fee is set to 0
  })

  // Transaction B has the extra fee field set to cover the fee of transactionA
  const transactionB = await algorand.createTransaction.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algos(1),
    extraFee: microAlgos(
      Math.max(
        Number(sp.fee) * 1000, // estimating size as 1000 bytes
        Number(sp.minFee),
      ),
    ), // extra fee covers the fee of transactionA
  })

  /**
   * transactionA and transactionB are added to the same atomic group.
   * The extra fee of transactionB covers the fee of transactionA.
   * Therefore, the total fee sum for the group is enough to cover the fee of both transactions.
   */
  const group = algorand.newGroup().addTransaction(transactionA).addTransaction(transactionB)

  const result = await group.send()
  console.log(result.txIds)
  // example: FEE_POOLING

  // example: INNER_TXN_FEE

  const factory = algorand.client.getTypedAppFactory(InnerTransactionsFactory, {
    defaultSender: randomAccountA.addr,
    defaultSigner: randomAccountA.signer,
  })

  const { appClient } = await factory.deploy({
    onUpdate: OnUpdate.ReplaceApp,
    onSchemaBreak: OnSchemaBreak.Fail,
  })

  await algorand.account.ensureFunded(appClient.appAddress, dispenser, algos(1))

  /**
   * By setting `coverAppCallInnerTransactionFees` to true, this transaction will
   * pay extra fees to cover the fees for any inner transactions in the contract method.
   */
  await appClient.send.payment({ args: {}, coverAppCallInnerTransactionFees: true })

  /**
   * You can also set the `extraFee` in the method call parameters to cover the fees for
   * one inner transaction in the contract method. This would fail if the contract method
   * has more than one inner transaction.
   */
  await appClient.send.payment({ args: {}, extraFee: microAlgos(1000) })
  // example: INNER_TXN_FEE
}

fees()
