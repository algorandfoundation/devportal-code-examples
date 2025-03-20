import { algo } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'
import { OnApplicationComplete } from 'algosdk'

async function paymentTransactionTypes() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment()

  // example: PAYMENT_TRANSACTION
  /**
   * Create a unsigned payment transaction sending 1 Algo from account_a to account_b
   *
   * Parameters for a payment transaction:
   * - sender: The account or address of the account that will send the Algo
   * - receiver: The account or address of the account that will receive the Algo
   * - amount: Amount to send
   */
  await algorand.createTransaction.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algo(1),
  })

  // example: CLOSE_ACCOUNT_TRANSACTION
  /**
   * Close an Algorand account by transferring all remaining funds to another account
   *
   * Parameters:
   * - sender: The address of the account to close
   * - receiver: The address that will receive the closed account's remaining Algo balance
   * - closeRemainderTo: The address that will receive all remaining Algo balance
   */
  await algorand.createTransaction.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algo(0),
    closeRemainderTo: randomAccountB, // All remaining balance will be sent here
  })
  // example: CLOSE_ACCOUNT_TRANSACTION
}

paymentTransactionTypes()

async function assetTransactionTypes() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment()

  // example: ASSET_CREATE_TRANSACTION
  /**
   * Create an unsigned asset creation transaction to create a new Algorand Standard Asset (ASA)
   *
   * Parameters for asset creation:
   * - sender: The account that will create and manage the asset
   * - total: The total number of base units of the asset to create (e.g., 10_000_000)
   * - decimals: The number of decimals for display purposes. If decimals is 6, then 1_000_000 base units = 1.000000 asset units
   * - defaultFrozen: Whether accounts must be unfrozen by the freeze address before they can receive this asset
   * - manager: The address that can manage the configuration of the asset. Can be permanently disabled by setting to undefined
   * - reserve: The address holding reserve (non-minted) units of the asset. Can be permanently disabled by setting to undefined
   * - freeze: The address that can freeze or unfreeze holder accounts. Can be permanently disabled by setting to undefined
   * - clawback: The address that can clawback holdings of this asset. Can be permanently disabled by setting to undefined
   * - unitName: The name of a unit of this asset (e.g., "MYA")
   * - assetName: The name of the asset (e.g., "My Asset")
   */
  await algorand.createTransaction.assetCreate({
    sender: randomAccountA,
    total: 10_000_000n,
    decimals: 6,
    defaultFrozen: false, // optional
    manager: randomAccountA, // optional. Can be permanently disabled by setting to undefined
    reserve: randomAccountA, // optional. Can be permanently disabled by setting to undefined
    freeze: randomAccountA, // optional. Can be permanently disabled by setting to undefined
    clawback: randomAccountA, // optional. Can be permanently disabled by setting to undefined
    unitName: 'MYA',
    assetName: 'My Asset',
  })
  // example: ASSET_CREATE_TRANSACTION

  // example: ASSET_CONFIG_TRANSACTION
  /**
   * Create an unsigned asset config transaction updating four mutable fields of an asset:
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
  await algorand.createTransaction.assetConfig({
    sender: randomAccountA,
    assetId: 123n,
    manager: randomAccountA,
    reserve: randomAccountA,
    freeze: randomAccountA,
    clawback: randomAccountA,
  })
  // example: ASSET_CONFIG_TRANSACTION

  // example: ASSET_TRANSFER_TRANSACTION
  await algorand.createTransaction.assetTransfer({
    sender: randomAccountA, // Account sending the asset
    receiver: randomAccountB, // Account receiving the asset
    assetId: 123n, // ID of the asset to transfer
    amount: 1n, // Amount in smallest divisible units
  })
  // example: ASSET_TRANSFER_TRANSACTION

  // example: ASSET_CLAWBACK_TRANSACTION
  /**
   * Create an unsigned asset clawback transaction. This allows an authorized clawback address
   * to revoke assets from an account and send them to another.
   *
   * Parameters for asset clawback:
   * - sender: The address of the clawback authority (must be the configured clawback address for the asset)
   * - clawbackTarget: The address to clawback assets from
   * - receiver: The address to send the clawed back assets to
   * - assetId: ID of the asset
   * - amount: The number of asset units to transfer
   */
  await algorand.createTransaction.assetTransfer({
    sender: randomAccountA,
    clawbackTarget: randomAccountB,
    receiver: randomAccountA,
    assetId: 123n,
    amount: 500000n,
  })
  // example: ASSET_CLAWBACK_TRANSACTION

  // example: ASSET_FREEZE_TRANSACTION
  /**
   * Create a unsigned asset freeze transaction freezing an asset with asset id 1234
   *
   * Parameters for freezing an asset:
   * - sender: The address of the account that will send the transaction
   * - assetId: The ID of the asset
   * - account: The account to freeze or unfreeze
   * - frozen: Whether the assets in the account should be frozen
   */
  await algorand.createTransaction.assetFreeze({
    sender: randomAccountA,
    assetId: 1234n,
    account: randomAccountB,
    frozen: true,
  })
  // example: ASSET_FREEZE_TRANSACTION

  // example: ASSET_DESTROY_TRANSACTION
  /**
   * Create an unsigned asset destroy transaction destroying an asset with asset id 1234
   * All of the assets must be owned by the creator of the asset before the asset can be deleted.
   *
   * Parameters for destroying an asset:
   * - sender: The address of the account that will send the transaction
   * - assetId: ID of the asset
   */
  await algorand.createTransaction.assetDestroy({
    sender: randomAccountA,
    assetId: 1234n,
  })
  // example: ASSET_DESTROY_TRANSACTION

  // example: ASSET_OPT_IN_TRANSACTION
  /**
   * Create an unsigned asset opt in transaction for accountA opting in to asset with asset id 1234
   *
   * Parameters for an asset opt in transaction:
   * - sender: The address of the account that will opt in to the asset
   * - assetId: ID of the asset
   */
  await algorand.createTransaction.assetOptIn({
    sender: randomAccountA, // The address of the account that will opt in to the asset
    assetId: 1234n, // ID of the asset
  })
  // example: ASSET_OPT_IN_TRANSACTION

  // example: ASSET_OPT_OUT_TRANSACTION
  /**
   * Create an unsigned asset opt out transaction for accountA opting out of asset with asset id 1234
   *
   * Parameters for an asset opt out transaction:
   * - sender: The address of the account that will opt out of the asset
   * - assetId: ID of the asset
   * - creator: The creator address of the asset
   */
  await algorand.createTransaction.assetOptOut({
    sender: randomAccountA,
    assetId: 1234n,
    creator: randomAccountB,
  })
  // example: ASSET_OPT_OUT_TRANSACTION
}

assetTransactionTypes()

async function applicationTransactionTypes() {
  const { algorand, randomAccountA } = await setupLocalnetEnvironment()

  // example: APPLICATION_CREATE_TRANSACTION
  // Minimal TEAL program that just returns 1 (success)
  const minimalTEAL = `
    #pragma version 10
    int 1
    return
  `

  /**
   * Create a unsigned application call transaction calling the hello method on the hello world contract
   *
   * Parameters for creating an application:
   * - sender: The address of the account that will send the transaction
   * - approvalProgram: The program to execute for all OnCompletes other than ClearState as raw TEAL (string)
   *     or compiled TEAL (bytes)
   * - clearStateProgram: The program to execute for ClearState OnComplete as raw TEAL (string)
   *     or compiled TEAL (bytes)
   */
  await algorand.send.appCreate({
    sender: randomAccountA,
    approvalProgram: minimalTEAL,
    clearStateProgram: minimalTEAL,
  })
  // example: APPLICATION_CREATE_TRANSACTION

  // Create app using compiled bytes
  const algodClient = algorand.client.algod
  const compiledApproval = await algodClient.compile(minimalTEAL).do()
  const compiledClear = await algodClient.compile(minimalTEAL).do()

  await algorand.send.appCreate({
    sender: randomAccountA,
    approvalProgram: new Uint8Array(Buffer.from(compiledApproval.result, 'base64')),
    clearStateProgram: new Uint8Array(Buffer.from(compiledClear.result, 'base64')),
  })

  // example: APPLICATION_UPDATE_TRANSACTION
  /**
   * Create a unsigned application update transaction updating the approval program and clear state program of an application
   *
   * Parameters for updating an application:
   * - sender: The address of the account that will send the transaction
   * - appId: ID of the application
   * - approvalProgram: The program to execute for all OnCompletes other than ClearState as raw TEAL (string)
   *     or compiled TEAL (bytes)
   * - clearStateProgram: The program to execute for ClearState OnComplete as raw TEAL (string)
   *     or compiled TEAL (bytes)
   */
  await algorand.createTransaction.appUpdate({
    sender: randomAccountA,
    appId: 1234n,
    approvalProgram: new Uint8Array(),
    clearStateProgram: new Uint8Array(),
  })
  // example: APPLICATION_UPDATE_TRANSACTION

  // example: APPLICATION_NO_OP_TRANSACTION
  /**
   * Create a unsigned application call transaction with the NoOp OnComplete actions
   *
   * Parameters for calling an application:
   * - sender: The address of the account that will send the transaction
   * - onComplete: The OnComplete action
   * - appId: ID of the application, defaults to undefined
   */
  await algorand.createTransaction.appCall({
    sender: randomAccountA,
    appId: 1234n,
    onComplete: OnApplicationComplete.NoOpOC,
  })
  // example: APPLICATION_NO_OP_TRANSACTION

  // example: APPLICATION_DELETE_TRANSACTION
  /**
   * Create an unsigned application delete transaction deleting an application with app id 1234
   *
   * Parameters for deleting an application:
   * - sender: The address of the account that will send the transaction
   * - appId: ID of the application
   */
  await algorand.createTransaction.appDelete({
    sender: randomAccountA,
    appId: 1234n,
  })
  // example: APPLICATION_DELETE_TRANSACTION
}

applicationTransactionTypes()

async function keyRegistrationTransactionTypes() {
  const { algorand, randomAccountA } = await setupLocalnetEnvironment()

  // example: KEY_REGISTRATION_ONLINE_TRANSACTION
  /**
   * Create an unsigned online key registration transaction
   *
   * Parameters for online key registration.
   * - sender: The address of the account that will send the transaction
   * - voteKey: The root participation public key
   * - selectionKey: The VRF public key
   * - voteFirst: The first round that the participation key is valid. Not to be confused with the firstValid round of the keyreg transaction
   * - voteLast: The last round that the participation key is valid. Not to be confused with the lastValid round of the keyreg transaction
   * - voteKeyDilution: This is the dilution for the 2-level participation key. It determines the interval (number of rounds) for generating new ephemeral keys
   */
  await algorand.createTransaction.onlineKeyRegistration({
    sender: randomAccountA,
    voteKey: new Uint8Array(),
    selectionKey: new Uint8Array(),
    voteFirst: 1000n,
    voteLast: 2000n,
    voteKeyDilution: 10n,
  })
  // example: KEY_REGISTRATION_ONLINE_TRANSACTION

  // example: KEY_REGISTRATION_OFFLINE_TRANSACTION
  /**
   * Create an unsigned offline key registration transaction
   *
   * Parameters for offline key registration.
   * - sender: The address of the account that will send the transaction
   * - preventAccountFromEverParticipatingAgain: Whether to prevent the account from ever participating again
   */
  await algorand.createTransaction.offlineKeyRegistration({
    sender: randomAccountA,
    preventAccountFromEverParticipatingAgain: false,
  })
  // example: KEY_REGISTRATION_OFFLINE_TRANSACTION
}

keyRegistrationTransactionTypes()
