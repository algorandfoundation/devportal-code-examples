import { Config } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '../setup-localnet-environment'

async function AssetReferenceExampleMethod1() {
  const { referenceAssetAppClient } = await setupLocalnetEnvironment()

  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_1
  // Configure automatic resource population per app call
  const result1 = await referenceAssetAppClient.send.getAssetTotalSupply({
    args: {},
    populateAppCallResources: false,
  })

  console.log('Method #1 Asset Total Supply', result1.return)

  // Or set the default value for populateAppCallResources to true globally and apply to all app calls
  Config.configure({
    populateAppCallResources: true,
  })

  const result2 = await referenceAssetAppClient.send.getAssetTotalSupply({
    args: {},
  })

  console.log('Method #1 Asset Total Supply', result2.return)
  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_1
}

AssetReferenceExampleMethod1().catch(console.error)

async function AssetReferenceExampleMethod2() {
  const { referenceAssetAppClient, referenceAssetId } = await setupLocalnetEnvironment()

  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_2
  // Include the account reference in the app call argument to be populated automatically
  const result = await referenceAssetAppClient.send.getAssetTotalSupplyWithArgument({
    args: {
      asset: referenceAssetId,
    },
  })

  console.log('Method #2 Asset Total Supply', result.return)
  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_2
}

AssetReferenceExampleMethod2().catch(console.error)

async function AssetReferenceExampleMethod3() {
  const { referenceAssetAppClient, referenceAssetId } = await setupLocalnetEnvironment()

  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_3
  // Include the account reference in the accountReferences array to be populated
  const result = await referenceAssetAppClient.send.getAssetTotalSupply({
    args: {},
    assetReferences: [referenceAssetId],
  })

  console.log('Method #3 Asset Total Supply', result.return)
  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_3
}

AssetReferenceExampleMethod3().catch(console.error)
