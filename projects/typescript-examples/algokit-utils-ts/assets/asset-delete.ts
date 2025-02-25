import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function assetDelete() {
  const { algorand, randomAccountA } = await setupLocalnetEnvironment()

  // example: ASSET_DESTROY_TRANSACTION

  /**
   * Send an asset destroy transaction destroying an asset with asset id 1234
   * All of the assets must be owned by the creator of the asset before the asset can be deleted.
   *
   * Parameters for destroying an asset:
   * - sender: The address of the account that will send the transaction
   * - assetId: ID of the asset
   */
  const destroyResult = await algorand.send.assetDestroy({
    sender: randomAccountA.addr,
    assetId: 1234n,
  })

  console.log('Asset destroy transaction ID:', destroyResult.transaction.txID)

  // example: ASSET_DESTROY_TRANSACTION
}

assetDelete().catch(console.error)
