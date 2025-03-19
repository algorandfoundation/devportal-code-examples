/* eslint-disable @typescript-eslint/no-unused-vars */
import { AlgorandClient } from '@algorandfoundation/algokit-utils'

import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'
import { AlgoAmount } from '@algorandfoundation/algokit-utils/types/amount'

import { HelloWorldFactory, HelloWorldClient } from '@/contracts/artifacts/clients/HelloWorld/HelloWorldClient'
import { CustomCreateFactory, CustomCreateClient } from '@/contracts/artifacts/clients/CustomCreate/CustomCreateClient'

export async function algorandBootstrap() {
  const { algorand, randomAccountA, randomAccountB, randomAccountC } = await setupLocalnetEnvironment()

  const algod = algorand.client.algod
  const indexer = algorand.client.indexer
  const kmd = algorand.client.kmd

  const algodConfig = {
    server: 'http://localhost',
    port: '4001',
    token: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
  }
  const indexerConfig = {
    server: 'http://localhost',
    port: '8980',
    token: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
  }
  const kmdConfig = {
    server: 'http://localhost',
    port: '4002',
    token: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
  }

  // example: INSTANTIATE_ALGORAND_CLIENT
  // Point to the network configured through environment variables or
  //  if no environment variables it will point to the default LocalNet
  //  configuration
  const client1 = AlgorandClient.fromEnvironment()
  // Point to default LocalNet configuration
  const client2 = AlgorandClient.defaultLocalNet()
  // Point to TestNet using AlgoNode free tier
  const client3 = AlgorandClient.testNet()
  // Point to MainNet using AlgoNode free tier
  const client4 = AlgorandClient.mainNet()
  // Point to a pre-created algod client
  const client5 = AlgorandClient.fromClients({ algod })
  // Point to pre-created algod, indexer and kmd clients
  const client6 = AlgorandClient.fromClients({ algod, indexer, kmd })
  // Point to custom configuration for algod
  const client7 = AlgorandClient.fromConfig({
    algodConfig: {
      server: 'http://localhost',
      port: '4001',
      token: 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    },
  })
  // Point to custom configuration for algod, indexer and kmd
  const client8 = AlgorandClient.fromConfig({
    algodConfig: algodConfig,
    indexerConfig: indexerConfig,
    kmdConfig: kmdConfig,
  })
  // example: INSTANTIATE_ALGORAND_CLIENT

  // example: SDK_CLIENTS
  const algodClient = algorand.client.algod
  const indexerClient = algorand.client.indexer
  const kmdClient = algorand.client.kmd
  // example: SDK_CLIENTS

  // example: TXN_WITHOUT_SIGNER_CACHE
  /*
   * If you don't want the Algorand client to cache the signer,
   * you can manually provide the signer.
   */
  await algorand.send.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: AlgoAmount.Algo(1),
    signer: randomAccountA.signer, // The signer must be manually provided
  })
  // example: TXN_WITHOUT_SIGNER_CACHE

  // example: SIGNER_CONFIG
  /*
   * By setting signers of accounts to the algorand client, the client will cache the signers
   * and use them to sign transactions when the sender is one of the accounts.
   */

  // If no signer is provided, the client will use the default signer
  algorand.setDefaultSigner(randomAccountA.signer)

  // If you have an address and a signer, use this method to set the signer
  algorand.setSigner(randomAccountA.addr, randomAccountA.signer)

  // If you have a `SigningAccount` object, use this method to set the signer
  algorand.setSignerFromAccount(randomAccountA)

  /*
   * The Algorand client can directly send this payment transaction without
   * needing a signer because it is tracking the signer for account_a.
   */
  await algorand.send.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: AlgoAmount.Algo(1),
  })
  // example: SIGNER_CONFIG

  // example: SUGGESTED_PARAMS_CONFIG
  /*
   * Sets the default validity window for transactions.
   * @param validityWindow The number of rounds between the first and last valid rounds
   * @returns The `algorand` so method calls can be chained
   */
  algorand.setDefaultValidityWindow(1000)

  /*
   * Get suggested params for a transaction (either cached or from algod if the cache is stale or empty)
   */
  const sp = await algorand.getSuggestedParams()

  // The suggested params can be modified like below
  sp.flatFee = true
  sp.fee = 2000

  /*
   * Sets a cache value to use for suggested params. Use this method to use modified suggested params for
   * the next transaction.
   * @param suggestedParams The suggested params to use
   * @param until A timestamp until which to cache, or if not specified then the timeout is used
   * @returns The `algorand` so method calls can be chained
   */
  algorand.setSuggestedParamsCache(sp)

  /*
   * Sets the timeout for caching suggested params. If set to 0, the Algorand client
   * will request suggested params from the algod client every time.
   * @param timeout The timeout in milliseconds
   * @returns The `algorand` so method calls can be chained
   */
  algorand.setSuggestedParamsCacheTimeout(0)
  // example: SUGGESTED_PARAMS_CONFIG
}

export async function appClient() {
  const { algorand, randomAccountA, randomAccountB, randomAccountC } = await setupLocalnetEnvironment()

  // example: GET_APP_CLIENT_WHEN_DEPLOYED

  /*
  Get typed app client by id
  */

  //For single app client instance
  let appClient = await algorand.client.getTypedAppClientById(HelloWorldClient, {
    appId: 1234n,
  })
  // or
  appClient = new HelloWorldClient({
    algorand,
    appId: 1234n,
  })

  // For multiple app client instances use the factory
  const factory = algorand.client.getTypedAppFactory(HelloWorldFactory)
  // or
  const factory2 = new HelloWorldFactory({ algorand })

  const appClient1 = await factory.getAppClientById({ appId: 1234n })
  const appClient2 = await factory.getAppClientById({ appId: 4321n })

  /*
  Get typed app client by creator and name
  */

  // For single app client instance
  let appClientByCreator = await algorand.client.getTypedAppClientByCreatorAndName(HelloWorldClient, {
    creatorAddress: randomAccountA.addr,
    appName: 'contract-name',
    // ...
  })
  // or
  appClientByCreator = await HelloWorldClient.fromCreatorAndName({
    algorand,
    creatorAddress: randomAccountA.addr,
    appName: 'contract-name',
    // ...
  })

  // For multiple app client instances use the factory
  let appClientFactory = algorand.client.getTypedAppFactory(HelloWorldFactory)
  // or
  appClientFactory = new HelloWorldFactory({ algorand })

  const appClientByCreator1 = await appClientFactory.getAppClientByCreatorAndName({
    creatorAddress: randomAccountA.addr,
    appName: 'contract-name',
    // ...
  })
  const appClientByCreator2 = await appClientFactory.getAppClientByCreatorAndName({
    creatorAddress: randomAccountA.addr,
    appName: 'contract-name-2',
    // ...
  })
  // example: GET_APP_CLIENT_WHEN_DEPLOYED

  // example: APP_NOT_DEPLOYED_APP_CREATE
  /*
   * Deploy a New App
   */
  let createFactory = algorand.client.getTypedAppFactory(HelloWorldFactory)
  // or
  createFactory = new HelloWorldFactory({ algorand })

  const { result, appClient: newAppClient } = await createFactory.send.create.bare()

  // or if the contract has a custom create method:
  const customFactory = algorand.client.getTypedAppFactory(CustomCreateFactory)

  const { result: customCreateResult, appClient: customCreateAppClient } = await customFactory.send.create.customCreate(
    { args: { age: 28 } },
  )

  // Deploy or Resolve App Idempotently by Creator and Name
  const { result: deployResult, appClient: deployedClient } = await createFactory.deploy({
    appName: 'contract-name',
  })
  // example: APP_NOT_DEPLOYED_APP_CREATE

  // example: APP_CLIENT_CALL_METHOD
  const methodResponse = await appClient.send.sayHello({ args: { firstName: 'there', lastName: 'world' } })
  console.log(methodResponse.return)
  // example: APP_CLIENT_CALL_METHOD
}

export async function fullAppClientExample() {
  // example: FULL_APP_CLIENT_EXAMPLE
  // A similar working example can be seen in the AlgoKit init production smart contract templates
  // In this case the generated factory is called `HelloWorldAppFactory` and is accessible via AppClients

  // These require environment variables to be present, or it will retrieve from default LocalNet
  const algorand = AlgorandClient.fromEnvironment()
  const deployer = await algorand.account.fromEnvironment('DEPLOYER', (1).algo())

  // Create the typed app factory
  const factory = algorand.client.getTypedAppFactory(HelloWorldFactory, {
    defaultSender: deployer.addr,
  })

  // Create the app and get a typed app client for the created app (note: this creates a new instance of the app every time,
  //  you can use .deploy() to deploy idempotently if the app wasn't previously
  //  deployed or needs to be updated if that's allowed)
  const { appClient } = await factory.send.create.bare()

  // Make a call to an ABI method and print the result
  const response = await appClient.send.sayHello({ args: { firstName: 'there', lastName: 'world' } })
  console.log(response.return)
  // example: FULL_APP_CLIENT_EXAMPLE
}
