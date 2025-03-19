import { Config } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '../setup-localnet-environment'

async function AccountReferenceExampleMethod1() {
  const { referenceAccountAppClient } = await setupLocalnetEnvironment()

  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_1
  // Configure automatic resource population per app call
  const result1 = await referenceAccountAppClient.send.getAccountBalance({
    args: {},
  })

  console.log('Method #1 Account Balance', result1.return)

  // Or set the default value for populateAppCallResources to true globally and apply to all app calls
  Config.configure({
    populateAppCallResources: true,
  })

  const result2 = await referenceAccountAppClient.send.getAccountBalance({
    args: {},
  })

  console.log('Method #1 Account Balance', result2.return)
  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_1
}

AccountReferenceExampleMethod1().catch(console.error)

async function AccountReferenceExampleMethod2() {
  const { referenceAccountAppClient, referenceAccount } = await setupLocalnetEnvironment()

  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_2
  // Include the account reference in the app call argument to be populated automatically
  const result = await referenceAccountAppClient.send.getAccountBalanceWithArgument({
    args: {
      account: referenceAccount.addr.toString(),
    },
  })

  console.log('Method #2 Account Balance', result.return)
  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_2
}

AccountReferenceExampleMethod2().catch(console.error)

async function AccountReferenceExampleMethod3() {
  const { referenceAccountAppClient, referenceAccount } = await setupLocalnetEnvironment()

  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_3
  // Include the account reference in the accountReferences array to be populated
  const result = await referenceAccountAppClient.send.getAccountBalance({
    args: {},
    accountReferences: [referenceAccount],
  })

  console.log('Method #3 Account Balance', result.return)
  // example: ACCOUNT_REFERENCE_EXAMPLE_METHOD_3
}

AccountReferenceExampleMethod3().catch(console.error)
