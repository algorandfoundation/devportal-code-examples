import { AlgorandClient, algo } from '@algorandfoundation/algokit-utils'
import type {
  TransactionSignerAccount,
  SigningAccount as SigningAccountType,
} from '@algorandfoundation/algokit-utils/types/account'
import type { Account as AccountType, Address } from 'algosdk'
import {
  ReferenceAccountFactory,
  ReferenceAccountClient,
} from '../contracts/artifacts/clients/ReferenceAccount/ReferenceAccountClient'
import {
  ReferenceAssetFactory,
  ReferenceAssetClient,
} from '../contracts/artifacts/clients/ReferenceAsset/ReferenceAssetClient'
import { ReferenceAppFactory, ReferenceAppClient } from '@/contracts/artifacts/clients/ReferenceApp/ReferenceAppClient'
import {
  ReferenceAccountAssetFactory,
  ReferenceAccountAssetClient,
} from '@/contracts/artifacts/clients/ReferenceAccountAsset/ReferenceAccountAssetClient'
import {
  ReferenceAccountAppFactory,
  ReferenceAccountAppClient,
} from '@/contracts/artifacts/clients/ReferenceAccountApp/ReferenceAccountAppClient'
import {
  ReferenceAppBoxFactory,
  ReferenceAppBoxClient,
} from '@/contracts/artifacts/clients/ReferenceAppBox/ReferenceAppBoxClient'

export type Account = Address &
  TransactionSignerAccount & {
    account: AccountType
  }

export type SigningAccount = Address &
  TransactionSignerAccount & {
    account: SigningAccountType
  }

async function bootstrapReferenceAccountExample(algorand: AlgorandClient, account: Account) {
  // Create an account from mnemonic for reference examples
  const referenceAccount = algorand.account.fromMnemonic(
    'rice broken rail solve mobile pill glue maximum speak mean stumble orbit mixed empower rent congress nest input peanut crush comfort spell swear abandon actual',
  )

  const factory = algorand.client.getTypedAppFactory(ReferenceAccountFactory, {
    defaultSender: account,
  })
  const client = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append' })

  return {
    referenceAccount,
    referenceAccountAppClient: client.appClient,
  }
}

async function bootstrapReferenceAssetExample(algorand: AlgorandClient, account: Account) {
  const { assetId } = await algorand.send.assetCreate({
    sender: account,
    total: 1_000_000n,
    decimals: 6,
    assetName: 'Reference Asset',
    unitName: 'REF',
  })

  const factory = algorand.client.getTypedAppFactory(ReferenceAssetFactory, {
    defaultSender: account,
  })
  const client = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append' })

  return {
    referenceAssetAppClient: client.appClient,
    referenceAssetId: assetId,
  }
}

async function bootstrapReferenceAppExample(algorand: AlgorandClient, account: Account) {
  const factory = algorand.client.getTypedAppFactory(ReferenceAppFactory, {
    defaultSender: account,
  })

  const client = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append' })

  return {
    referenceAppAppClient: client.appClient,
  }
}

async function bootstrapAccountAssetReferenceExample(algorand: AlgorandClient, account: Account) {
  const factory = algorand.client.getTypedAppFactory(ReferenceAccountAssetFactory, {
    defaultSender: account,
  })

  const client = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append' })

  return {
    accountAssetReferenceAppClient: client.appClient,
  }
}

async function bootstrapReferenceAccountAppExample(algorand: AlgorandClient, account: Account) {
  const factory = algorand.client.getTypedAppFactory(ReferenceAccountAppFactory, {
    defaultSender: account,
  })

  const client = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append' })

  return {
    referenceAccountAppAppClient: client.appClient,
  }
}

async function bootstrapAppBoxExample(algorand: AlgorandClient, account: Account) {
  const factory = algorand.client.getTypedAppFactory(ReferenceAppBoxFactory, {
    defaultSender: account,
  })

  const client = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append' })

  return {
    referenceAppBoxAppClient: client.appClient,
  }
}

/**
 * Sets up funded accounts for demonstration purposes.
 * This function creates a local Algorand client and multiple random accounts,
 * each funded with 10 Algos from the localnet dispenser.
 */
export async function setupLocalnetEnvironment(): Promise<{
  algorand: AlgorandClient
  dispenser: SigningAccount
  randomAccountA: Account
  randomAccountB: Account
  randomAccountC: Account
  randomAccountD: Account
  referenceAccount: SigningAccount
  referenceAccountAppClient: ReferenceAccountClient
  referenceAssetAppClient: ReferenceAssetClient
  referenceAssetId: bigint
  referenceAppAppClient: ReferenceAppClient
  accountAssetReferenceAppClient: ReferenceAccountAssetClient
  referenceAccountAppAppClient: ReferenceAccountAppClient
  referenceAppBoxAppClient: ReferenceAppBoxClient
}> {
  // Initialize the Algorand client
  const algorand = AlgorandClient.defaultLocalNet()

  // Set the suggested params cache timeout to 0 to avoid 'transaction already in ledger' errors
  algorand.setSuggestedParamsCacheTimeout(0)

  // Get the dispenser account
  const dispenser = await algorand.account.localNetDispenser()

  // Create random accounts
  const randomAccounts = Array.from({ length: 4 }, () => algorand.account.random())
  const [randomAccountA, randomAccountB, randomAccountC, randomAccountD] = randomAccounts

  // Create other apps, accounts and assets related to examples
  const { referenceAccount, referenceAccountAppClient } = await bootstrapReferenceAccountExample(algorand, dispenser)
  const { referenceAssetAppClient, referenceAssetId } = await bootstrapReferenceAssetExample(algorand, dispenser)
  const { referenceAppAppClient } = await bootstrapReferenceAppExample(algorand, dispenser)
  const { accountAssetReferenceAppClient } = await bootstrapAccountAssetReferenceExample(algorand, dispenser)
  const { referenceAccountAppAppClient } = await bootstrapReferenceAccountAppExample(algorand, dispenser)
  const { referenceAppBoxAppClient } = await bootstrapAppBoxExample(algorand, dispenser)

  // Fund all test accounts with 10 Algos each
  await Promise.all(
    [...randomAccounts, referenceAccount].map((account) => algorand.account.ensureFunded(account, dispenser, algo(10))),
  )

  return {
    algorand,
    dispenser,
    randomAccountA,
    randomAccountB,
    randomAccountC,
    randomAccountD,
    referenceAccount,
    referenceAccountAppClient,
    referenceAssetAppClient,
    referenceAssetId,
    referenceAppAppClient,
    accountAssetReferenceAppClient,
    referenceAccountAppAppClient,
    referenceAppBoxAppClient,
  }
}
