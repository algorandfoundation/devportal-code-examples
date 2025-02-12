import { algo } from "@algorandfoundation/algokit-utils";
import { setupLocalnetEnvironment } from "@/setup-localnet-environment";

async function transactionTypes() {
  const { algorand, randomAccountA, randomAccountB } = await setupLocalnetEnvironment();

  // example: PAYMENT_TRANSACTION
  // Transfer Algos between accounts
  await algorand.send.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algo(1), // Amount in Algos (will be converted to microAlgos)
  });
  // example: PAYMENT_TRANSACTION

  // example: ASSET_CREATE_TRANSACTION
  // Create a new Algorand Standard Asset (ASA)
  await algorand.send.assetCreate({
    sender: randomAccountA, // Creator and manager of the asset
    total: 1000n, // Total units of the asset
    decimals: 0, // Number of decimals for display purposes (0 = no decimals)
    defaultFrozen: false, // Whether accounts must be unfrozen before receiving the asset
  });
  // example: ASSET_CREATE_TRANSACTION

  // example: ASSET_CONFIG_TRANSACTION
  // Configure an existing Algorand Standard Asset
  await algorand.send.assetConfig({
    sender: randomAccountA,
    assetId: 123n, // The unique ID of the asset to configure
    manager: randomAccountA, // Account authorized to change asset configuration
  });
  // example: ASSET_CONFIG_TRANSACTION

  // example: ASSET_TRANSFER_TRANSACTION
  // Transfer ASAs between accounts
  await algorand.send.assetTransfer({
    sender: randomAccountA,
    receiver: randomAccountB,
    assetId: 123n, // The ID of the asset to transfer
    amount: 1n, // Amount in base units (considering decimals)
  });
  // example: ASSET_TRANSFER_TRANSACTION

  // example: ASSET_FREEZE_TRANSACTION
  // Freeze or unfreeze an ASA for an account
  await algorand.send.assetFreeze({
    sender: randomAccountA, // Must be the freeze address
    assetId: 123n,
    account: randomAccountB, // Account to freeze/unfreeze
    frozen: true, // true = freeze, false = unfreeze
  });
  // example: ASSET_FREEZE_TRANSACTION

  // example: ASSET_DELETE_TRANSACTION
  // Delete/destroy an Algorand Standard Asset
  await algorand.send.assetDestroy({
    sender: randomAccountA, // Must be the asset manager
    assetId: 123n, // Asset will be permanently destroyed
  });
  // example: ASSET_DELETE_TRANSACTION

  // example: ASSET_OPTIN_TRANSACTION
  // Opt an account into an ASA
  await algorand.send.assetOptIn({
    sender: randomAccountA, // Account that wants to receive the asset
    assetId: 123n, // Asset to opt into
  });
  // example: ASSET_OPTIN_TRANSACTION

  // example: ASSET_OPTOUT_TRANSACTION
  // Opt an account out of an ASA
  await algorand.send.assetOptOut({
    sender: randomAccountA,
    assetId: 123n,
    ensureZeroBalance: true, // Prevents opt-out if account still holds units
  });
  // example: ASSET_OPTOUT_TRANSACTION

  // example: APP_CREATE_TRANSACTION
  // Create a new smart contract application
  await algorand.send.appCreate({
    sender: randomAccountA, // Creator of the application
    approvalProgram: new Uint8Array(), // Logic that processes all application calls
    clearStateProgram: new Uint8Array(), // Logic that processes clear state calls
  });
  // example: APP_CREATE_TRANSACTION

  // example: APP_UPDATE_TRANSACTION
  // Update an existing smart contract application
  await algorand.send.appUpdate({
    sender: randomAccountA, // Must be the application creator
    appId: 123n,
    approvalProgram: new Uint8Array(), // New program logic
    clearStateProgram: new Uint8Array(), // New clear state logic
  });
  // example: APP_UPDATE_TRANSACTION

  // example: APP_CALL_TRANSACTION
  // Call a smart contract application
  await algorand.send.appCall({
    sender: randomAccountA, // Account making the call
    appId: 123n, // Application being called
  });
  // example: APP_CALL_TRANSACTION

  // example: APP_DELETE_TRANSACTION
  // Delete a smart contract application
  await algorand.send.appDelete({
    sender: randomAccountA, // Must be the creator
    appId: 123n, // Application will be permanently deleted
  });
  // example: APP_DELETE_TRANSACTION

  // example: KEY_REG_ONLINE_TRANSACTION
  // Register online participation keys
  await algorand.send.onlineKeyRegistration({
    sender: randomAccountA,
    voteKey: new Uint8Array(), // Key used for voting
    selectionKey: new Uint8Array(), // Key used for committee selection
    voteFirst: 1000n, // First round to participate
    voteLast: 2000n, // Last round to participate
    voteKeyDilution: 10n, // Security parameter controlling key reuse
  });
  // example: KEY_REG_ONLINE_TRANSACTION

  // example: KEY_REG_OFFLINE_TRANSACTION
  // Register offline participation keys
  await algorand.send.offlineKeyRegistration({
    sender: randomAccountA, // Account will go offline
  });
  // example: KEY_REG_OFFLINE_TRANSACTION
}

transactionTypes();
