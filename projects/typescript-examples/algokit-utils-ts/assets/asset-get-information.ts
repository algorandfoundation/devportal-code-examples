import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function getAssetInformation() {
  const { algorand } = await setupLocalnetEnvironment()

  // example: GET_ASSET_INFORMATION

  /**
   * Get information about an Algorand Standard Asset (ASA).
   *
   * - assetId: The ID of the asset
   * - creator: The address of the account that created the asset
   * - total: The total amount of the smallest divisible units that were created of the asset
   * - decimals: The amount of decimal places the asset was created with
   * - defaultFrozen: Whether the asset was frozen by default for all accounts, defaults to undefined
   * - manager: The address of the optional account that can manage the configuration of the asset and destroy it,
   *     defaults to undefined
   * - reserve: The address of the optional account that holds the reserve (uncirculated supply) units of the asset,
   *     defaults to undefined
   * - freeze: The address of the optional account that can be used to freeze or unfreeze holdings of this asset,
   *     defaults to undefined
   * - clawback: The address of the optional account that can clawback holdings of this asset from any account,
   *     defaults to undefined
   * - unitName: The optional name of the unit of this asset (e.g. ticker name), defaults to undefined
   * - unitNameAsBytes: The optional name of the unit of this asset as bytes, defaults to undefined
   * - assetName: The optional name of the asset, defaults to undefined
   * - assetNameAsBytes: The optional name of the asset as bytes, defaults to undefined
   * - url: Optional URL where more information about the asset can be retrieved, defaults to undefined
   * - urlAsBytes: Optional URL where more information about the asset can be retrieved as bytes, defaults to undefined
   * - metadataHash: 32-byte hash of some metadata that is relevant to the asset and/or asset holders,
   *     defaults to undefined
   */
  const assetInfo = await algorand.asset.getById(1234n)

  console.log(assetInfo.assetName)
  console.log(assetInfo.total)

  // example: GET_ASSET_INFORMATION
}

getAssetInformation().catch(console.error)
