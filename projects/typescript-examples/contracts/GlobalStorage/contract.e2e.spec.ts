import { Config } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { GlobalStorageFactory } from '../artifacts/clients/GlobalStorage/GlobalStorageClient'

describe('GlobalStorage contract', () => {
  const localnet = algorandFixture()
  beforeAll(() => {
    Config.configure({
      debug: true,
    })
    registerDebugEventHandlers()
  })
  beforeEach(localnet.newScope)

  const deploy = async (address: string) => {
    const factory = localnet.algorand.client.getTypedAppFactory(GlobalStorageFactory, {
      defaultSender: address,
    })

    const { appClient } = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append', suppressLog: true })
    return { client: appClient }
  }

  test('read initial global state values', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    const result = await client.newGroup().readGlobalState().simulate()

    expect(result.returns).toBeDefined()
    expect(result.returns![0]).toBeDefined()

    const returns = result.returns![0]

    expect(returns![0]).toBe(50n)
    expect(returns![1]).toBe(0n)
    expect(String.fromCharCode(...returns![2])).toBe('Silvio')
    expect(returns![3]).toBe('Micali')
    expect(returns?.[4]).toBe(true)
    expect(returns?.[5]).toBe(testAccount.addr.toString())
  })

  test('check global state existence', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    const result = await client.newGroup().hasGlobalState().simulate()

    expect(result.returns).toBeDefined()
    expect(result.returns![0]).toBeDefined()
    expect(result.returns?.[0]?.[0]).toBe(0n)
    expect(result.returns?.[0]?.[1]).toBe(true)
  })

  test('write and verify global state values', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    await client
      .newGroup()
      .writeGlobalState({
        args: {
          valueString: 'New String',
          valueBool: false,
          valueAccount: testAccount.publicKey,
        },
      })
      .send()

    const state = await client.state.global.getAll()

    expect(state.globalInt).toBe(50n)
    expect(state.globalIntNoDefault).toBe(0n)
    expect(state.globalBytes ? state.globalBytes.asString() : '').toBe('Silvio')
    expect(state.globalString).toBe('New String')
    expect(state.globalBool).toBe(0n)
    expect(state.globalAccount?.asByteArray()).toEqual(testAccount.publicKey)
  })

  test('write and read dynamic global state', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    const result = await client
      .newGroup()
      .writeDynamicGlobalState({
        args: {
          key: 'testKey',
          value: 'testValue',
        },
      })
      .simulate()

    expect(result.returns[0]).toBe('testValue')
  })

  test('verify app budget consumption is reasonable', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    const result = await client
      .newGroup()
      .readGlobalState()
      .writeGlobalState({
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
