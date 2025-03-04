import { Config } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address, ABIUintType } from 'algosdk'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { BoxStorageFactory } from '../artifacts/clients/BoxStorage/BoxStorageClient'

describe('BoxStorage contract', () => {
  const localnet = algorandFixture()
  beforeAll(() => {
    Config.configure({
      debug: true,
    })
    registerDebugEventHandlers()
  })
  beforeEach(localnet.newScope)

  const deploy = async (account: Address) => {
    const factory = localnet.algorand.client.getTypedAppFactory(BoxStorageFactory, {
      defaultSender: account,
    })

    const { appClient } = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append', suppressLog: true })
    return { client: appClient }
  }

  const fundContract = async (sender: Address, receiver: Address) => {
    await localnet.algorand.send.payment({
      amount: (1).algo(),
      sender,
      receiver,
    })
  }

  function createBoxReference(appId: bigint, prefix: string, key: bigint) {
    const uint64Type = new ABIUintType(64)
    const encodedKey = uint64Type.encode(key)
    const boxName = new Uint8Array([...new TextEncoder().encode(prefix), ...encodedKey])

    return {
      appId,
      name: boxName,
    }
  }

  test('set and read box int value', async () => {
    const { testAccount } = localnet.context

    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testValue = 42n

    await client
      .newGroup()
      .setBox({ args: { valueInt: testValue }, boxReferences: ['boxInt'] })
      .send()

    const boxValue = await client.state.box.boxInt()
    expect(boxValue).toBe(testValue)
  })

  test('set and read box map value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testString = 'Hello Box Storage'

    await client
      .newGroup()
      .setBoxMap({
        args: { key: 1n, value: testString },
        boxReferences: [createBoxReference(client.appId, 'boxMap', 1n)],
      })
      .send()

    const boxValue = await client.getBoxMap({ args: { key: 1n } })
    expect(boxValue).toBe(testString)
  })

  test('set and read box map with default value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const boxValue = await client.getBoxMapWithDefault({ args: { key: 1n } })
    expect(boxValue).toBe('default')
  })

  test('set and read box ref value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const { returns } = await client.send.getBoxRef({
      args: {},
      boxReferences: [(client.appId, 'boxRef')],
    })

    expect(returns?.[0]?.returnValue).toBe(testAccount.addr.toString())
  })

  test('maybe box returns correct value and existence', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    // First check when box doesn't exist
    const [emptyValue, exists] = await client.maybeBox()
    expect(exists).toBe(false)
    expect(emptyValue).toBe(0n) // Default value for uint64

    // Set a value and check again
    const testValue = 42n
    await client
      .newGroup()
      .setBox({ args: { valueInt: testValue }, boxReferences: ['boxInt'] })
      .send()

    const [value, existsAfterSet] = await client.maybeBox()

    expect(existsAfterSet).toBe(true)
    expect(value).toBe(testValue)
  })

  test('verify app budget consumption is reasonable', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const result = await client
      .newGroup()
      .setBoxMap({
        args: { key: 1n, value: 'Test String' },
        boxReferences: [createBoxReference(client.appId, 'boxMap', 1n)],
      })
      .setBox({ args: { valueInt: 123n }, boxReferences: ['boxInt'] })
      .simulate()

    expect(result.simulateResponse.txnGroups[0].appBudgetConsumed).toBeLessThan(700)
  })
})
