import { Config } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '../setup-localnet-environment'

async function AccountAppReferenceExampleMethod1() {
  const { referenceAccountAppAppClient } = await setupLocalnetEnvironment()

  // example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_1
  // Configure automatic resource population per app call
  const result1 = await referenceAccountAppAppClient.send.getMyCounter({
    args: {},
    populateAppCallResources: true,
  })

  console.log('Method #1 My Counter', result1.return)

  // Or set the default value for populateAppCallResources to true globally and apply to all app calls
  Config.configure({
    populateAppCallResources: true,
  })

  const result2 = await referenceAccountAppAppClient.send.getMyCounter({
    args: {},
  })

  console.log('Method #1 My Counter', result2.return)
  // example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_1
}

AccountAppReferenceExampleMethod1().catch(console.error)

async function AccountAppReferenceExampleMethod2() {
  const { referenceAccountAppAppClient, randomAccountA } = await setupLocalnetEnvironment()

  // example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_2
  // Include the account and app references in the app call arguments to be populated automatically
  const result = await referenceAccountAppAppClient.send.getMyCounterWithArg({
    args: {
      account: randomAccountA.addr.toString(),
      app: 1717n, // Using the default app ID from the contract
    },
  })

  console.log('Method #2 My Counter', result.return)
  // example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_2
}

AccountAppReferenceExampleMethod2().catch(console.error)

async function AccountAppReferenceExampleMethod3() {
  const { referenceAccountAppAppClient, randomAccountA } = await setupLocalnetEnvironment()

  // example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_3
  // Manually provide both account and app references in the respective arrays
  const result = await referenceAccountAppAppClient.send.getMyCounter({
    args: {},
    accountReferences: [randomAccountA.addr],
    appReferences: [1717n], // Using the default app ID from the contract
  })

  console.log('Method #3 My Counter', result.return)
  // example: ACCOUNT_APP_REFERENCE_EXAMPLE_METHOD_3
}

AccountAppReferenceExampleMethod3().catch(console.error)
