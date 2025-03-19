import { Config } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '../setup-localnet-environment'

async function AccountAssetReferenceExampleMethod1() {
  const { referenceAccount, accountAssetReferenceAppClient, referenceAssetId, algorand } =
    await setupLocalnetEnvironment()

  await algorand.send.assetOptIn({
    sender: referenceAccount,
    assetId: referenceAssetId,
  })

  // example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_1
  // Configure automatic resource population per app call
  const result1 = await accountAssetReferenceAppClient.send.getAssetBalance({
    args: {},
    // populateAppCallResources: true,
  })

  console.log('Method #1 Asset Balance', result1)

  // Or set the default value for populateAppCallResources to true globally and apply to all app calls
  Config.configure({
    populateAppCallResources: true,
  })

  const result2 = await accountAssetReferenceAppClient.send.getAssetBalance({
    args: {},
  })

  console.log('Method #1 Asset Balance', result2)
  // example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_1
}

AccountAssetReferenceExampleMethod1().catch(console.error)

async function AccountAssetReferenceExampleMethod2() {
  const { accountAssetReferenceAppClient, referenceAssetId } = await setupLocalnetEnvironment()

  // example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_2
  // Include the account and asset references in the app call arguments to be populated automatically
  const result = await accountAssetReferenceAppClient.getAssetBalanceWithArg({
    args: {
      account: 'R3J76MDPEXQEWBV2LQ6FLQ4PYC4QXNHHPIL2BX2KSFU4WUNJJMDBTLRNEM',
      asset: referenceAssetId,
    },
  })

  console.log('Method #2 Asset Balance', result)
  // example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_2
}

AccountAssetReferenceExampleMethod2().catch(console.error)

async function AccountAssetReferenceExampleMethod3() {
  const { accountAssetReferenceAppClient, referenceAssetId } = await setupLocalnetEnvironment()

  // example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_3
  // Manually provide both account and asset references in the respective arrays
  const result = await accountAssetReferenceAppClient.getAssetBalance({
    args: {},
    accountReferences: ['R3J76MDPEXQEWBV2LQ6FLQ4PYC4QXNHHPIL2BX2KSFU4WUNJJMDBTLRNEM'],
    assetReferences: [referenceAssetId],
  })

  console.log('Method #3 Asset Balance', result)
  // example: ACCOUNT_ASSET_REFERENCE_EXAMPLE_METHOD_3
}

AccountAssetReferenceExampleMethod3().catch(console.error)
