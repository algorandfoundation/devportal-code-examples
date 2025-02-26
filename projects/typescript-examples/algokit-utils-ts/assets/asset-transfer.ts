import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function assetTransfer() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment()

  // example: ASSET_TRANSFER_TRANSACTION

  /**
   * Send an asset transfer transaction of 1 asset with asset id 1234 from randomAccountA to randomAccountB
   *
   * Parameters for an asset transfer transaction:
   * - sender: The address of the account that will send the asset
   * - assetId: The asset id of the asset to transfer
   * - amount: Amount of the asset to transfer (smallest divisible unit)
   * - receiver: The address of the account to send the asset to
   */
  const transferResult = await algorand.send.assetTransfer({
    sender: randomAccountA.addr,
    assetId: 1234n,
    receiver: randomAccountB.addr,
    amount: 1n,
  })

  console.log('Asset transfer transaction ID:', transferResult.transaction.txID)

  // example: ASSET_TRANSFER_TRANSACTION
}

assetTransfer().catch(console.error)
