// example: GET_ASSET_REFERENCE_EXAMPLE
import { Contract, Asset, readonly } from '@algorandfoundation/algorand-typescript'

/**
 * A contract that demonstrates how to use resource usage in a contract using an asset reference
 */
export default class ReferenceAsset extends Contract {
  /**
   * Returns the total supply of the asset
   * @returns The total supply of the asset
   */
  @readonly
  public getAssetTotalSupply() {
    return Asset(1005).total // Replace with your asset id
  }

  /**
   * Returns the total supply of the asset
   * @param asset The asset to get the total supply of
   * @returns The total supply of the asset
   */
  @readonly
  public getAssetTotalSupplyWithArgument(asset: Asset) {
    return asset.total
  }
}
// example: GET_ASSET_REFERENCE_EXAMPLE
