import {
  Account,
  Application,
  Asset,
  Contract,
  Global,
  Txn,
  arc4,
  itxn,
  Bytes,
} from '@algorandfoundation/algorand-typescript'
import type { uint64 } from '@algorandfoundation/algorand-typescript'

/**
 * InnerTransactions contract demonstrates various inner transaction patterns
 * in Algorand smart contracts.
 */
export default class InnerTransactions extends Contract {
  // example: PAYMENT
  /**
   * Demonstrates a simple payment inner transaction.
   * The fee is set to 0 by default. Manually set here for demonstration purposes.
   * The `Sender` for the payment is implied to be Global.currentApplicationAddress.
   * If a different sender is needed, it'd have to be an account that has been
   * rekeyed to the application address.
   * @returns The amount of the payment
   */
  public payment(): uint64 {
    const result = itxn
      .payment({
        amount: 5000,
        receiver: Txn.sender,
        fee: 0,
      })
      .submit()

    return result.amount
  }
  // example: PAYMENT

  // example: ASSET_CREATE
  /**
   * Creates a fungible asset (token)
   * @returns The ID of the created asset
   */
  public fungibleAssetCreate(): uint64 {
    const itxnResult = itxn
      .assetConfig({
        total: 100_000_000_000,
        decimals: 2,
        unitName: 'RP',
        assetName: 'Royalty Points',
      })
      .submit()

    return itxnResult.createdAsset.id
  }

  /**
   * Creates a non-fungible asset (NFT).
   * Following the ARC3 standard, the total supply must be 1 for a non-fungible asset.
   * If you want to create fractional NFTs, `total` * `decimals` point must be 1.
   * ex) total=100, decimals=2, 100 * 0.01 = 1
   * The fee is set to 0 by default for inner transactions.
   * The Sender is implied to be Global.currentApplicationAddress.
   * @returns The ID of the created asset
   */
  public nonFungibleAssetCreate(): uint64 {
    const itxnResult = itxn
      .assetConfig({
        total: 100,
        decimals: 2,
        unitName: 'ML',
        assetName: 'Mona Lisa',
        url: 'https://link_to_ipfs/Mona_Lisa',
        manager: Global.currentApplicationAddress,
        reserve: Global.currentApplicationAddress,
        freeze: Global.currentApplicationAddress,
        clawback: Global.currentApplicationAddress,
        fee: 0,
      })
      .submit()

    return itxnResult.createdAsset.id
  }
  // example: ASSET_CREATE

  // example: ASSET_OPT_IN
  /**
   * Opts the application into an asset.
   * A zero amount asset transfer to one's self is a special type of asset transfer
   * that is used to opt-in to an asset.
   * To send an asset transfer, the asset must be an available resource.
   * @param asset The asset to opt into
   */
  public assetOptIn(asset: Asset): void {
    itxn
      .assetTransfer({
        assetReceiver: Global.currentApplicationAddress,
        xferAsset: asset,
        assetAmount: 0,
        fee: 0,
      })
      .submit()
  }
  // example: ASSET_OPT_IN

  // example: ASSET_TRANSFER
  /**
   * Transfers an asset from the application to another account.
   * For a smart contract to transfer an asset, the app account must be opted into the asset
   * and be holding non zero amount of assets.
   * To send an asset transfer, the asset must be an available resource.
   * @param asset The asset to transfer
   * @param receiver The account to receive the asset
   * @param amount The amount to transfer
   */
  public assetTransfer(asset: Asset, receiver: Account, amount: uint64): void {
    itxn
      .assetTransfer({
        assetReceiver: receiver,
        xferAsset: asset,
        assetAmount: amount,
        fee: 0,
      })
      .submit()
  }

  // example: ASSET_TRANSFER

  // example: ASSET_FREEZE
  /**
   * Freezes an asset for a specific account.
   * To freeze an asset, the asset must be a freezable asset
   * by having an account with freeze authority.
   * @param acctToBeFrozen The account to freeze the asset for
   * @param asset The asset to freeze
   */
  public assetFreeze(acctToBeFrozen: Account, asset: Asset): void {
    itxn
      .assetFreeze({
        freezeAccount: acctToBeFrozen, // account to be frozen
        freezeAsset: asset,
        frozen: true,
        fee: 0,
      })
      .submit()
  }
  // example: ASSET_FREEZE

  // example: ASSET_REVOKE
  /**
   * Revokes (clawbacks) an asset from an account.
   * To revoke an asset, the asset must be a revocable asset
   * by having an account with clawback authority.
   * The Sender is implied to be current_application_address.
   * @param asset The asset to revoke
   * @param accountToBeRevoked The account to revoke the asset from
   * @param amount The amount to revoke
   */
  public assetRevoke(asset: Asset, accountToBeRevoked: Account, amount: uint64): void {
    itxn
      .assetTransfer({
        assetReceiver: Global.currentApplicationAddress,
        xferAsset: asset,
        assetSender: accountToBeRevoked, // AssetSender is only used in the case of clawback
        assetAmount: amount,
        fee: 0,
      })
      .submit()
  }
  // example: ASSET_REVOKE

  // example: ASSET_CONFIG
  /**
   * Reconfigures an existing asset.
   * For a smart contract to transfer an asset, the app account must be opted into the asset
   * and be holding non zero amount of assets.
   * To send an asset transfer, the asset must be an available resource.
   * Refer the Resource Availability section for more information.
   * @param asset The asset to reconfigure
   */
  public assetConfig(asset: Asset): void {
    itxn
      .assetConfig({
        configAsset: asset,
        manager: Global.currentApplicationAddress,
        reserve: Global.currentApplicationAddress,
        freeze: Txn.sender,
        clawback: Txn.sender,
        fee: 0,
      })
      .submit()
  }
  // example: ASSET_CONFIG

  // example: ASSET_DELETE
  /**
   * Deletes an asset.
   * To delete an asset, the asset must be a deleteable asset
   * by having an account with delete authority.
   * The Sender is implied to be current_application_address.
   * @param asset The asset to delete
   */
  public assetDelete(asset: Asset): void {
    itxn
      .assetConfig({
        configAsset: asset,
        fee: 0,
      })
      .submit()
  }
  // example: ASSET_DELETE

  // example: GROUPED_INNER_TXNS
  /**
   * Demonstrates grouped inner transactions
   * @param appId The application to call
   * @returns A tuple containing the payment amount and the result of the hello world call
   */
  public multiInnerTxns(appId: Application): [uint64, string] {
    // First payment transaction
    const payTxn = itxn
      .payment({
        amount: 5000,
        receiver: Txn.sender,
        fee: 0,
      })
      .submit()

    // Second application call transaction
    const appCallTxn = itxn
      .applicationCall({
        appId: appId.id,
        appArgs: [arc4.methodSelector('sayHello(string,string)string'), new arc4.Str('Jane'), new arc4.Str('Doe')],
        fee: 0,
      })
      .submit()

    // Get result from the log of the app call
    const helloWorldResult = arc4.decodeArc4<string>(appCallTxn.lastLog, 'log')
    return [payTxn.amount, helloWorldResult]
  }
  // example: GROUPED_INNER_TXNS

  // example: DEPLOY_APP
  /**
   * HelloWorld class is a contract class defined in a different file.
   * It would be imported in a real implementation:
   *
   * import HelloWorld from '../HelloWorld/contract.algo'
   */

  /**
   * Deploys a HelloWorld contract using direct application call
   *
   * This method uses the itxn.applicationCall to deploy the HelloWorld contract.
   * @returns The ID of the deployed application
   */
  public deployApp(): uint64 {
    // In a real implementation, we would compile the HelloWorld contract
    // This is a placeholder implementation that mocks the bytecode
    const appTxn = itxn
      .applicationCall({
        approvalProgram: Bytes('approval_program'),
        clearStateProgram: Bytes('clear_state_program'),
        fee: 0,
      })
      .submit()

    return appTxn.createdApp.id
  }

  /**
   * Deploys a HelloWorld contract using arc4
   *
   * This method uses arc4 to deploy the HelloWorld contract.
   * @returns The ID of the deployed application
   */
  public arc4DeployApp(): uint64 {
    // In a real implementation, we would use the SDK to create the app
    // This is a mock implementation that returns a hardcoded ID

    /** @TODO is this implemented in puya-ts?
     * app_txn = arc4.arc4_create(HelloWorld)
     */
    return 1234
  }
  // example: DEPLOY_APP

  // example: NOOP_APP_CALL
  /**
   * Demonstrates calling methods on another application
   * @param appId The application to call
   * @returns A string result from the hello world call
   */
  public noopAppCall(appId: Application): string {
    // First application call - invoke an ABI method
    const callTxn = itxn
      .applicationCall({
        appId: appId.id,
        appArgs: [arc4.methodSelector('sayHello(string,string)string'), new arc4.Str('John'), new arc4.Str('Doe')],
      })
      .submit()

    // Extract result from the log
    return arc4.decodeArc4<string>(callTxn.lastLog, 'log')
  }
  // example: NOOP_APP_CALL
}
