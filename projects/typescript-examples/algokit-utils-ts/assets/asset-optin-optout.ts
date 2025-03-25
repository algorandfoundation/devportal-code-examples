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

  // example: ASSET_BULK_OPT_IN_TRANSACTION

  /**
   * Opt an account out of a list of Algorand Standard Assets.
   *
   * Transactions will be sent in batches of 16 as transaction groups.
   *
   * @param account The account to opt-in
   * @param assetIds The list of asset IDs to opt-out of
   * @param options Any parameters to control the transaction or execution of the transaction
   *
   * @returns An array of records matching asset ID to transaction ID of the opt in
   */
  const bulkOptInResult = await algorand.asset.bulkOptIn(randomAccountA.addr, [1234n, 5678n])

  console.log(
    'Asset bulk opt-in transaction IDs:',
    bulkOptInResult.map((r) => r.transactionId),
  )

  // example: ASSET_BULK_OPT_IN_TRANSACTION

  // example: ASSET_BULK_OPT_OUT_TRANSACTION

  /**
   * Opt an account out of a list of Algorand Standard Assets.
   *
   * Transactions will be sent in batches of 16 as transaction groups.
   *
   * @param account The account to opt-in
   * @param assetIds The list of asset IDs to opt-out of
   * @param options Any parameters to control the transaction or execution of the transaction
   *
   * @returns An array of records matching asset ID to transaction ID of the opt out
   */
  const bulkOptOutResult = await algorand.asset.bulkOptOut(randomAccountA.addr, [1234n, 5678n])

  console.log(
    'Asset bulk opt-out transaction IDs:',
    bulkOptOutResult.map((r) => r.transactionId),
  )

  // example: ASSET_BULK_OPT_OUT_TRANSACTION
}

assetOptInOptOut().catch(console.error)
