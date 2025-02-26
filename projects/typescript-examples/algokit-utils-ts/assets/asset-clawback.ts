import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function assetClawback() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment()

  // example: ASSET_CLAWBACK_TRANSACTION

  /**
   * An asset clawback transaction is an asset transfer transaction with the
   * `clawbackTarget` set to the account that is being clawed back from.
   *
   * Parameters for an asset transfer transaction:
   * - sender: The address of the account that will send the transaction
   * - assetId: ID of the asset
   * - amount: Amount of the asset to transfer (smallest divisible unit)
   * - receiver: The account to send the asset to
   * - clawbackTarget: The account to take the asset from, defaults to undefined
   */
  const txnResult = await algorand.send.assetTransfer({
    sender: randomAccountA.addr, // Must be the clawback address for the asset
    assetId: 1234n,
    amount: 1n,
    receiver: randomAccountA.addr,
    clawbackTarget: randomAccountB.addr, // account that is being clawed back from
  })

  console.log('Asset clawback transaction ID:', txnResult.transaction.txID)

  // example: ASSET_CLAWBACK_TRANSACTION
}

assetClawback().catch(console.error)
