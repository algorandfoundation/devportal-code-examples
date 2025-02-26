import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function assetUpdate() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment()

  // example: ASSET_UPDATE_TRANSACTION

  /**
   * Send an asset config transaction updating four mutable fields of an asset:
   * manager, reserve, freeze, clawback. This operation is only possible if the sender is
   * the asset manager and the asset has all four mutable fields set.
   *
   * Parameters for configuring an existing asset:
   * - sender: The address of the account that will send the transaction
   * - assetId: ID of the asset
   * - manager: The address that can change the manager, reserve, clawback, and freeze addresses, defaults to undefined
   * - reserve: The address that holds the uncirculated supply, defaults to undefined
   * - freeze: The address that can freeze the asset in any account, defaults to undefined
   * - clawback: The address that can clawback the asset from any account, defaults to undefined
   */
  const txnResult = await algorand.send.assetConfig({
    sender: randomAccountA.addr,
    assetId: 1234n,
    manager: randomAccountB.addr,
    reserve: randomAccountB.addr,
    freeze: randomAccountB.addr,
    clawback: randomAccountB.addr,
  })

  console.log('Asset update transaction ID:', txnResult.transaction.txID)

  // example: ASSET_UPDATE_TRANSACTION
}

assetUpdate().catch(console.error)
