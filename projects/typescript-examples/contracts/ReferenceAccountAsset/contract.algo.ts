// example: REFERENCE_ACCOUNT_ASSET_EXAMPLE

import { Contract, readonly, Account, Asset, assert } from '@algorandfoundation/algorand-typescript'
import { Address } from '@algorandfoundation/algorand-typescript/arc4'

/**
 * A contract that demonstrates how to reference both accounts and assets in a smart contract
 */
export default class ReferenceAccountAsset extends Contract {
  /**
   * Returns the balance of a specific asset in a hardcoded account
   * @returns The asset balance of the account
   */
  @readonly
  public getAssetBalance() {
    const address = new Address('R3J76MDPEXQEWBV2LQ6FLQ4PYC4QXNHHPIL2BX2KSFU4WUNJJMDBTLRNEM') // Replace with your account address
    const addressBytes = address.bytes
    const account = Account(addressBytes)
    const asset = Asset(1472) // Replace with your asset ID

    assert(account.isOptedIn(asset), 'Account is not opted in to the asset')

    return asset.balance(account)
  }

  /**
   * Returns the balance of a specific asset in a provided account
   * @param account The account to check the asset balance for
   * @param asset The asset to check the balance of
   * @returns The asset balance of the account
   */
  @readonly
  public getAssetBalanceWithArg(account: Account, asset: Asset) {
    assert(account.isOptedIn(asset), 'Account is not opted in to the asset')
    // Get the asset balance
    return asset.balance(account)
  }
}
// example: REFERENCE_ACCOUNT_ASSET_EXAMPLE
