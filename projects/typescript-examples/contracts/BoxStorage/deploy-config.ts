import { AlgorandClient } from '@algorandfoundation/algokit-utils'
import { BoxStorageFactory } from '@/contracts/artifacts/clients/BoxStorage/BoxStorageClient'
import { getOperationMessage } from '@/utils'

export async function deploy() {
  // Initialize Algorand client using environment variables or default LocalNet config:
  // - Uses ALGOD_SERVER with optional ALGOD_PORT and ALGOD_TOKEN if defined
  // - Falls back to localnet configuration if variables aren't defined
  const algorand = AlgorandClient.fromEnvironment()
  // Get deployer account using environment-based convention:
  // - For mainnet/testnet: Uses DEPLOYER_MNEMONIC from environment variables
  // - For localnet: Creates/uses KMD wallet named 'DEPLOYER' with auto-funded account
  const deployer = await algorand.account.fromEnvironment('DEPLOYER')

  // Create a typed factory for the contract
  // This provides type-safe interaction with the contract
  const typedFactory = algorand.client.getTypedAppFactory(BoxStorageFactory, {
    defaultSender: deployer.addr,
  })

  console.log('\n', `🚀 Deploying ${typedFactory.appName} Application...`, '\n')

  // Deploy the contract with the following settings:
  // - onUpdate: 'append' -> create new app instead of updating if code changes
  // - onSchemaBreak: 'append' -> create new app if storage schema changes
  const { appClient, result } = await typedFactory.deploy({
    appName: typedFactory.appName,
    onUpdate: 'append',
    onSchemaBreak: 'append',
    suppressLog: true,
  })

  // If this is a new deployment or replacement, fund the contract with 1 ALGO
  // This ensures the contract has minimum balance to operate
  if (['create', 'replace'].includes(result.operationPerformed)) {
    await algorand.send.payment({
      amount: (1).algo(),
      sender: deployer.addr,
      receiver: appClient.appAddress,
    })
  }

  // Get deployment details and display in a table
  const { appId, appAddress, appName } = appClient

  console.table({
    name: appName,
    id: appId.toString(),
    address: appAddress.toString(),
    deployer: deployer.addr.toString(),
    status: getOperationMessage(result.operationPerformed),
  })
}
