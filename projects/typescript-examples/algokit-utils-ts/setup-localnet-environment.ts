import { AlgorandClient, algo } from '@algorandfoundation/algokit-utils'
import type { TransactionSignerAccount, SigningAccount } from '@algorandfoundation/algokit-utils/types/account'
import type { Account, Address } from 'algosdk'

export type RandomAccount = Address &
  TransactionSignerAccount & {
    account: Account
  }

export type DispenserAccount = Address &
  TransactionSignerAccount & {
    account: SigningAccount
  }

/**
 * Sets up funded accounts for demonstration purposes.
 * This function creates a local Algorand client and multiple random accounts,
 * each funded with 10 Algos from the localnet dispenser.
 */
export async function setupLocalnetEnvironment(): Promise<{
  algorand: AlgorandClient
  dispenser: DispenserAccount
  randomAccountA: RandomAccount
  randomAccountB: RandomAccount
  randomAccountC: RandomAccount
  randomAccountD: RandomAccount
}> {
  // Initialize the Algorand client
  const algorand = AlgorandClient.defaultLocalNet()
  // Get the dispenser account
  const dispenser = await algorand.account.localNetDispenser()

  // Create random accounts
  const randomAccounts = Array.from({ length: 4 }, () => algorand.account.random())

  // Fund all test accounts with 10 Algos each
  await Promise.all(randomAccounts.map((account) => algorand.account.ensureFunded(account, dispenser, algo(10))))

  const [randomAccountA, randomAccountB, randomAccountC, randomAccountD] = randomAccounts

  return {
    algorand,
    dispenser,
    randomAccountA,
    randomAccountB,
    randomAccountC,
    randomAccountD,
  }
}
