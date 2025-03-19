import { Config, algo, microAlgo } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address } from 'algosdk'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { InnerTransactionsFactory } from '../artifacts/clients/InnerTransactions/InnerTransactionsClient'
import { HelloWorldFactory } from '../artifacts/clients/HelloWorld/HelloWorldClient'

describe('InnerTransactions contract', () => {
  const localnet = algorandFixture()

  beforeAll(() => {
    Config.configure({
      debug: true,
    })
    registerDebugEventHandlers()
  })

  beforeEach(localnet.newScope)

  const deploy = async (account: Address) => {
    const factory = localnet.algorand.client.getTypedAppFactory(InnerTransactionsFactory, {
      defaultSender: account,
    })

    const { appClient } = await factory.deploy({
      onUpdate: 'append',
      onSchemaBreak: 'append',
      suppressLog: true,
    })

    return { client: appClient }
  }

  const fundContract = async (sender: Address, receiver: Address, amount: number = 1) => {
    await localnet.algorand.send.payment({
      amount: algo(amount),
      sender,
      receiver,
    })
  }

  const deployHelloWorld = async (account: Address) => {
    const factory = localnet.algorand.client.getTypedAppFactory(HelloWorldFactory, {
      defaultSender: account,
    })

    const { appClient } = await factory.deploy({
      onUpdate: 'append',
      onSchemaBreak: 'append',
      suppressLog: true,
    })

    return { client: appClient }
  }

  test('payment inner transaction works correctly', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress, 1)

    const { return: result } = await client.send.payment({ args: {}, extraFee: microAlgo(1000) })
    expect(result).toBe(5000n)
  })

  test('fungible asset create works correctly', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress, 2)

    const { return: assetId } = await client.send.fungibleAssetCreate({ args: {}, extraFee: microAlgo(1000) })
    expect(assetId).toBeGreaterThan(0n)
  })

  test('non-fungible asset create works correctly', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress, 2)

    const { return: assetId } = await client.send.nonFungibleAssetCreate({ args: {}, extraFee: microAlgo(1000) })
    expect(assetId).toBeGreaterThan(0n)
  })

  test('asset opt-in and send interactions', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress, 2)

    // Test asset creation and opt-in
    const { return: assetId } = await client.send.fungibleAssetCreate({ args: {}, extraFee: microAlgo(1000) })
    expect(assetId).toBeGreaterThan(0n)

    // Test opt-in
    await client.send.assetOptIn({ args: { asset: assetId! }, extraFee: microAlgo(1000) })
  })

  test('asset freeze functionality', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress, 5)

    // Create an asset with freeze capability
    const { return: assetId } = await client.send.nonFungibleAssetCreate({ args: {}, extraFee: microAlgo(1000) })
    expect(assetId).toBeGreaterThan(0n)

    // The test account needs to opt into the asset
    await localnet.algorand.send.assetOptIn({
      assetId: BigInt(Number(assetId)),
      sender: testAccount,
    })

    // Verify the asset is not frozen initially
    const accountInfoBefore = await localnet.algorand.account.getInformation(testAccount.addr)
    // Check if assets property exists before trying to access it
    expect(accountInfoBefore.assets).toBeDefined()

    // Use proper property names based on the assetHolding structure
    if (accountInfoBefore.assets) {
      const assetHoldingBefore = accountInfoBefore.assets.find((asset) => asset.assetId === BigInt(Number(assetId)))
      expect(assetHoldingBefore).toBeDefined()
      expect(assetHoldingBefore?.isFrozen).toBe(false)
    }

    // Now freeze the asset for the test account
    await client.send.assetFreeze({
      args: {
        acctToBeFrozen: testAccount.addr.publicKey,
        asset: assetId!,
      },
      extraFee: microAlgo(1000),
    })

    // Verify the asset is now frozen
    const accountInfoAfter = await localnet.algorand.account.getInformation(testAccount.addr)
    // Check if assets property exists before trying to access it
    expect(accountInfoAfter.assets).toBeDefined()

    if (accountInfoAfter.assets) {
      const assetHoldingAfter = accountInfoAfter.assets.find((asset) => asset.assetId === BigInt(Number(assetId)))
      expect(assetHoldingAfter).toBeDefined()
      expect(assetHoldingAfter?.isFrozen).toBe(true)
    }
  })

  test('asset configuration', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress, 5)

    // Create an asset to configure
    const { return: assetId } = await client.send.nonFungibleAssetCreate({ args: {}, extraFee: microAlgo(1000) })
    expect(assetId).toBeGreaterThan(0n)

    // Test changing the asset configuration
    await client.send.assetConfig({ args: { asset: assetId! }, extraFee: microAlgo(1000) })

    // Verify configuration was updated - need to use algod or a different approach
    // to check the asset parameters
    const assetInfo = await localnet.algorand.client.algod.getAssetByID(Number(assetId)).do()
    expect(assetInfo).toBeDefined()
    expect(assetInfo.params).toBeDefined()
    expect(assetInfo.params.manager).toBe(client.appAddress.toString())
    expect(assetInfo.params.reserve).toBe(client.appAddress.toString())
    expect(assetInfo.params.freeze).toBe(testAccount.addr.toString())
    expect(assetInfo.params.clawback).toBe(testAccount.addr.toString())
  })

  test('asset deletion', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress, 5)

    // Test asset creation and delete
    const { return: assetId } = await client.send.nonFungibleAssetCreate({ args: {}, extraFee: microAlgo(1000) })
    expect(assetId).toBeGreaterThan(0n)

    // Delete the asset
    await client.send.assetDelete({ args: { asset: assetId! }, extraFee: microAlgo(1000) })
  })

  test('multi inner transactions works correctly', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    // Deploy a HelloWorld app to call
    const { client: helloWorldClient } = await deployHelloWorld(testAccount)

    await fundContract(testAccount, client.appAddress, 5)

    // Call multiInnerTxns with app reference
    const { return: result } = await client.send.multiInnerTxns({
      args: { appId: helloWorldClient.appId },
      appReferences: [helloWorldClient.appId],
      extraFee: microAlgo(2000),
    })

    if (result) {
      const [paymentAmount, helloResult] = result
      expect(paymentAmount).toBe(5000n)
      expect(helloResult).toBe('Hello Jane Doe')
    }
  })

  /** @TODO not implemented in the contract */
  // test('deploy app works correctly', async () => {
  //   const { testAccount } = localnet.context
  //   const { client } = await deploy(testAccount)

  //   await fundContract(testAccount, client.appAddress, 5)

  //   // Deploy an app via inner transaction
  //   const { return: deployedAppId } = await client.send.deployApp({ args: {}, extraFee: microAlgo(1000) })
  //   expect(deployedAppId).toBeGreaterThan(0n)
  // })

  /** @TODO not implemented in the contract */
  // test('arc4 deploy app works correctly', async () => {
  //   const { testAccount } = localnet.context
  //   const { client } = await deploy(testAccount)

  //   await fundContract(testAccount, client.appAddress, 5)

  //   // Deploy an arc4 app via inner transaction
  //   const { return: deployedAppId } = await client.send.arc4DeployApp({ args: {} })
  //   expect(deployedAppId).toBeGreaterThan(0n)
  // })

  test('noop app call works correctly', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    // Deploy a HelloWorld app to call
    const { client: helloWorldClient } = await deployHelloWorld(testAccount)

    await fundContract(testAccount, client.appAddress, 5)

    // Call the Hello app via inner transactio
    const { return: result } = await client.send.noopAppCall({
      args: { appId: helloWorldClient.appId },
      appReferences: [helloWorldClient.appId],
      extraFee: microAlgo(2000),
    })

    expect(result).toBe('Hello John Doe')
  })
})
