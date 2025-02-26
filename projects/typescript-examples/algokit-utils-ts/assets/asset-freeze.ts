import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function assetFreeze() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment()

  // example: ASSET_FREEZE_TRANSACTION

  /**
   * Send an asset freeze transaction freezing an asset with asset id 1234
   *
   * Parameters for freezing an asset:
   * - sender: The address of the account that will send the transaction
   * - assetId: The ID of the asset
   * - account: The account to freeze or unfreeze
   * - frozen: Whether the assets in the account should be frozen
   */
  const freezeResult = await algorand.send.assetFreeze({
    sender: randomAccountA.addr,
    assetId: 1234n,
    account: randomAccountB.addr, // The account to freeze or unfreeze
    frozen: true,
  })

  console.log('Asset freeze transaction ID:', freezeResult.transaction.txID)

  /**
   * Send an asset unfreeze transaction unfreezing an asset with asset id 1234
   */
  const unfreezeResult = await algorand.send.assetFreeze({
    sender: randomAccountA.addr,
    assetId: 1234n,
    account: randomAccountB.addr, // The account to freeze or unfreeze
    frozen: false,
  })

  console.log('Asset unfreeze transaction ID:', unfreezeResult.transaction.txID)

  // example: ASSET_FREEZE_TRANSACTION
}

assetFreeze().catch(console.error)
