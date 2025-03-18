import { AlgorandClient, algo } from '@algorandfoundation/algokit-utils'
import type {
  TransactionSignerAccount,
  SigningAccount as SigningAccountType,
} from '@algorandfoundation/algokit-utils/types/account'
import type { Account as AccountType, Address } from 'algosdk'
import { ReferenceFactory, ReferenceClient } from '../contracts/artifacts/clients/Reference/ReferenceClient'

export type Account = Address &
  TransactionSignerAccount & {
    account: AccountType
  }

export type SigningAccount = Address &
  TransactionSignerAccount & {
    account: SigningAccountType
  }

async function deployReferenceApp(algorand: AlgorandClient, account: Account) {
  const factory = algorand.client.getTypedAppFactory(ReferenceFactory, {
    defaultSender: account,
  })

  const client = await factory.deploy()

  return client.appClient
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
  referenceAppClient: ReferenceClient
}> {
  // Initialize the Algorand client
  const algorand = AlgorandClient.defaultLocalNet()
  // Get the dispenser account
  const dispenser = await algorand.account.localNetDispenser()

  // Create an account from mnemonic for reference examples
  const referenceAccount = algorand.account.fromMnemonic(
    'rice broken rail solve mobile pill glue maximum speak mean stumble orbit mixed empower rent congress nest input peanut crush comfort spell swear abandon actual',
  )

  // Create random accounts
  const randomAccounts = Array.from({ length: 4 }, () => algorand.account.random())

  // Include referenceAccount in the accounts to be funded
  const allAccounts = [...randomAccounts, referenceAccount]

  // Fund all test accounts with 10 Algos each
  await Promise.all(allAccounts.map((account) => algorand.account.ensureFunded(account, dispenser, algo(10))))

  const [randomAccountA, randomAccountB, randomAccountC, randomAccountD] = randomAccounts

  // Deploy the reference app
  const referenceAppClient = await deployReferenceApp(algorand, randomAccountA)

  return {
    algorand,
    dispenser,
    randomAccountA,
    randomAccountB,
    randomAccountC,
    randomAccountD,
    referenceAccount,
    referenceAppClient,
  }
}
