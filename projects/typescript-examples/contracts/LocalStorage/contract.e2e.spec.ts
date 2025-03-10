import { Config } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { LocalStorageFactory } from '../artifacts/clients/LocalStorage/LocalStorageClient'

describe('LocalStorage contract', () => {
  const localnet = algorandFixture()
  beforeAll(() => {
    Config.configure({
      debug: true,
    })
    registerDebugEventHandlers()
  })
  beforeEach(localnet.newScope)

  const deploy = async (address: string) => {
    const factory = localnet.algorand.client.getTypedAppFactory(LocalStorageFactory, {
      defaultSender: address,
    })

    const { appClient } = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append', suppressLog: true })
    return { client: appClient }
  }

  test('opt in and read local state values', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    await client.newGroup().optIn.optInToApplication().send()

    const result = await client.newGroup().readLocalState().simulate()

    expect(result.returns).toBeDefined()
    expect(result.returns![0]).toBeDefined()

    const returns = result.returns![0]

    expect(returns![0]).toBe(100n)
    expect(returns![1]).toBe(200n)
    expect(String.fromCharCode(...returns![2])).toBe('Silvio')
    expect(returns![3]).toBe('Micali')
    expect(returns![4]).toBe(true)
    expect(returns![5]).toBe(testAccount.addr.toString())
  })

  test('write and verify local state values', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    await client.newGroup().optIn.optInToApplication().send()
    await client
      .newGroup()
      .writeLocalState({
        args: {
          valueString: 'New String',
          valueBool: false,
          valueAccount: testAccount.publicKey,
        },
      })
      .send()

    const result = await client.newGroup().readLocalState().simulate()
    const returns = result.returns![0]

    expect(returns![3]).toBe('New String')
    expect(returns![4]).toBe(false)
    expect(returns![5]).toBe(testAccount.addr.toString())
  })

  test('write and read dynamic local state', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    await client.newGroup().optIn.optInToApplication().send()

    const writeResult = await client
      .newGroup()
      .writeDynamicLocalState({
        args: {
          key: 'testKey',
          value: 'testValue',
        },
      })
      .send()

    expect(writeResult.returns[0]).toBe('testValue')

    const readResult = await client
      .newGroup()
      .readDynamicLocalState({ args: { key: 'testKey' } })
      .simulate()

    expect(readResult.returns[0]).toBe('testValue')
  })

  test('clear local state', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    await client.newGroup().optIn.optInToApplication().send()
    await client.newGroup().clearLocalState().send()

    await expect(client.newGroup().readLocalState().simulate()).rejects.toThrow('assert failed')
  })

  test('verify app budget consumption is reasonable', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    const result = await client
      .newGroup()
      .optIn.optInToApplication()
      .readLocalState()
      .writeLocalState({
        args: {
          valueString: 'Test',
          valueBool: true,
          valueAccount: testAccount.publicKey,
        },
      })
      .simulate()

    expect(result.simulateResponse.txnGroups[0].appBudgetConsumed).toBeLessThan(700)
  })
})
