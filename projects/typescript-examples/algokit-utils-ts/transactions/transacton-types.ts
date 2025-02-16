import { algo } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function paymentTransactionTypes() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment()

  // example: PAYMENT_TRANSACTION
  await algorand.createTransaction.payment({
    sender: randomAccountA, // The address of the account sending the transaction
    receiver: randomAccountB, // The address of the account that will receive the Algo
    amount: algo(1), // Amount to send
  })
  // example: PAYMENT_TRANSACTION
}

paymentTransactionTypes()

async function assetTransactionTypes() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment()

  // example: ASSET_CREATE_TRANSACTION
  await algorand.createTransaction.assetCreate({
    sender: randomAccountA, // Creator and manager of the asset
    total: 1000n, // Total amount of the smallest divisible unit to create
    decimals: 0, // Number of decimals for display (0 = not divisible)
    defaultFrozen: false, // Whether accounts must be unfrozen before receiving the asset
  })
  // example: ASSET_CREATE_TRANSACTION

  // example: ASSET_CONFIG_TRANSACTION
  await algorand.createTransaction.assetConfig({
    sender: randomAccountA, // Account sending the transaction
    assetId: 123n, // ID of the asset to reconfigure
    manager: randomAccountA, // Account that can manage the configuration
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

  // example: ASSET_FREEZE_TRANSACTION
  await algorand.createTransaction.assetFreeze({
    sender: randomAccountA, // Must be the freeze address
    assetId: 123n, // ID of the asset to freeze/unfreeze
    account: randomAccountB, // Account to freeze/unfreeze
    frozen: true, // Whether the assets should be frozen
  })
  // example: ASSET_FREEZE_TRANSACTION

  // example: ASSET_DELETE_TRANSACTION
  await algorand.createTransaction.assetDestroy({
    sender: randomAccountA, // Must be the asset manager
    assetId: 123n, // ID of the asset to destroy
  })
  // example: ASSET_DELETE_TRANSACTION

  // example: ASSET_OPTIN_TRANSACTION
  await algorand.createTransaction.assetOptIn({
    sender: randomAccountA, // Account that wants to receive the asset
    assetId: 123n, // ID of the asset to opt into
  })
  // example: ASSET_OPTIN_TRANSACTION

  // example: ASSET_OPTOUT_TRANSACTION
  await algorand.createTransaction.assetOptOut({
    creator: randomAccountA, // The address of the asset creator account to close the asset position to (any remaining asset units will be sent to this account).
    sender: randomAccountA, // The address of the account sending the transaction.
    assetId: 123n, // ID of the asset that will be opted-out of.
  })
  // example: ASSET_OPTOUT_TRANSACTION
}

assetTransactionTypes()

async function applicationTransactionTypes() {
  const { algorand, randomAccountA } = await setupLocalnetEnvironment()

  // Minimal TEAL program that just returns 1 (success)
  const minimalTEAL = `
    #pragma version 10
    int 1
    return
  `

  // example: APP_CREATE_TRANSACTION
  const result = await algorand.send.appCreate({
    sender: randomAccountA, // Creator of the application
    approvalProgram: minimalTEAL, // Logic that processes all application calls
    clearStateProgram: minimalTEAL, // Logic that processes clear state calls
  })

  console.log('App created with TEAL source:', result.appId)
  // example: APP_CREATE_TRANSACTION

  // Create app using compiled bytes
  const algodClient = algorand.client.algod
  const compiledApproval = await algodClient.compile(minimalTEAL).do()
  const compiledClear = await algodClient.compile(minimalTEAL).do()

  await algorand.send.appCreate({
    sender: randomAccountA,
    approvalProgram: new Uint8Array(Buffer.from(compiledApproval.result, 'base64')),
    clearStateProgram: new Uint8Array(Buffer.from(compiledClear.result, 'base64')),
  })

  // example: APP_UPDATE_TRANSACTION
  await algorand.createTransaction.appUpdate({
    sender: randomAccountA, // Must be the application creator
    appId: 123n, // ID of the app to update
    approvalProgram: new Uint8Array(), // New approval program logic
    clearStateProgram: new Uint8Array(), // New clear state program logic
  })
  // example: APP_UPDATE_TRANSACTION

  // example: APP_CALL_TRANSACTION
  await algorand.createTransaction.appCall({
    sender: randomAccountA, // The address of the account sending the transaction.
    appId: 123n, // ID of the application; 0 if the application is being created.
  })
  // example: APP_CALL_TRANSACTION

  // example: APP_DELETE_TRANSACTION
  await algorand.createTransaction.appDelete({
    sender: randomAccountA, // The address of the account sending the transaction.
    appId: 123n, // ID of the application; 0 if the application is being created.
  })
  // example: APP_DELETE_TRANSACTION
}

applicationTransactionTypes()

async function keyRegistrationTransactionTypes() {
  const { algorand, randomAccountA } = await setupLocalnetEnvironment()

  // example: KEY_REG_ONLINE_TRANSACTION
  await algorand.createTransaction.onlineKeyRegistration({
    sender: randomAccountA, // The address of the account sending the transaction
    voteKey: new Uint8Array(), // The root participation public key
    selectionKey: new Uint8Array(), // The VRF public key
    voteFirst: 1000n, // The first round that the participation key is valid. Not to be confused with the firstValid round of the keyreg transaction
    voteLast: 2000n, // The last round that the participation key is valid. Not to be confused with the lastValid round of the keyreg transaction
    voteKeyDilution: 10n, // This is the dilution for the 2-level participation key. It determines the interval (number of rounds) for generating new ephemeral keys
  })
  // example: KEY_REG_ONLINE_TRANSACTION

  // example: KEY_REG_OFFLINE_TRANSACTION
  await algorand.createTransaction.offlineKeyRegistration({
    sender: randomAccountA, // The address of the account sending the transaction
  })
  // example: KEY_REG_OFFLINE_TRANSACTION
}

keyRegistrationTransactionTypes()
