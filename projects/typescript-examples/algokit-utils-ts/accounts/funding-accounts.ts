/* eslint-disable @typescript-eslint/no-unused-vars */
import { AlgorandClient, algo } from '@algorandfoundation/algokit-utils'

async function fundingAccounts() {
  /** Initialize an Algorand client instance configured for LocalNet */
  const algorand = AlgorandClient.defaultLocalNet()

  // example: LOCALNET_DISPENSER
  /**
   * Get the default LocalNet dispenser account that can be used to fund other accounts
   */
  const localNetDispenser = await algorand.account.localNetDispenser()
  // example: LOCALNET_DISPENSER

  // example: DISPENSER_ACCOUNT
  /**
   * Returns an account (with private key loaded) that can act as a dispenser from environment variables.
   * If environment variables are not present, returns the default LocalNet dispenser account.
   */
  const environmentDispenser = await algorand.account.dispenserFromEnvironment()
  // example: DISPENSER_ACCOUNT

  // example: ENSURE_FUNDED
  /**
   * Funds a given account using a dispenser account as a funding source.
   * Ensures the given account has a certain amount of Algo free to spend (accounting for Algo locked in
   * minimum balance requirement).
   */
  await algorand.account.ensureFunded('ACCOUNTADDRESS', localNetDispenser, algo(1))
  // example: ENSURE_FUNDED

  // example: ENSURE_FUNDED_FROM_ENV
  /**
   * Ensure an account is funded from a dispenser account configured in environment.
   * Uses a dispenser account retrieved from the environment, per the dispenser_from_environment method,
   * as a funding source such that the given account has a certain amount of Algo free to spend
   * (accounting for Algo locked in minimum balance requirement).
   */
  await algorand.account.ensureFundedFromEnvironment('ACCOUNTADDRESS', algo(1))
  // example: ENSURE_FUNDED_FROM_ENV

  // example: ENSURE_FUNDED_TESTNET
  /**
   * Ensure an account has sufficient funds using the TestNet Dispenser API
   * The dispenser client uses the `ALGOKIT_DISPENSER_ACCESS_TOKEN` environment variable
   * to authenticate with the dispenser API.
   */
  const dispenserClient = algorand.client.getTestNetDispenserFromEnvironment()
  await algorand.account.ensureFundedFromTestNetDispenserApi('ACCOUNTADDRESS', dispenserClient, algo(1))
  // example: ENSURE_FUNDED_TESTNET

  // example: TESTNET_DISPENSER_FUND
  /**
   * Directly fund an account using the TestNet Dispenser API
   */
  const testnetDispenser = algorand.client.getTestNetDispenserFromEnvironment()
  await testnetDispenser.fund('ACCOUNTADDRESS', 1_000_000)
  // example: TESTNET_DISPENSER_FUND
}

fundingAccounts()
