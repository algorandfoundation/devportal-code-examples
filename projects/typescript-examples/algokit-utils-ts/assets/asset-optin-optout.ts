import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function assetOptInOptOut() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment()

  // example: ASSET_OPT_IN_TRANSACTION

  /**
   * Send an asset opt in transaction for randomAccountA opting in to asset with asset id 1234
   *
   * Parameters for an asset opt in transaction:
   * - sender: The address of the account that will opt in to the asset
   * - assetId: ID of the asset
   */
  const optInResult = await algorand.send.assetOptIn({
    sender: randomAccountA.addr,
    assetId: 1234n,
  })

  console.log('Asset opt-in transaction ID:', optInResult.transaction.txID)

  // example: ASSET_OPT_IN_TRANSACTION

  // example: ASSET_OPT_OUT_TRANSACTION

  /**
   * Send an asset opt out transaction for randomAccountA opting out of asset with asset id 1234
   *
   * Parameters for an asset opt out transaction:
   * - sender: The address of the account that will opt out of the asset
   * - assetId: ID of the asset
   * - creator: The creator address of the asset
   * - ensureZeroBalance: Check if account has zero balance before opt-out, defaults to true
   */
  const optOutResult = await algorand.send.assetOptOut({
    sender: randomAccountA.addr,
    assetId: 1234n,
    creator: randomAccountB.addr,
    ensureZeroBalance: true,
  })

  console.log('Asset opt-out transaction ID:', optOutResult.transaction.txID)

  // example: ASSET_OPT_OUT_TRANSACTION
}

assetOptInOptOut().catch(console.error)
