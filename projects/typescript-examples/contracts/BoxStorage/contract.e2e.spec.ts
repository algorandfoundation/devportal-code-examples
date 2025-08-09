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

    const [emptyValue, exists] = await client.maybeBox()
    expect(exists).toBe(false)
    expect(emptyValue).toBe(0n)

    const testValue = 42n
    await client
      .newGroup()
      .setBox({ args: { valueInt: testValue }, boxReferences: ['boxInt'] })
      .send()

    const [value, existsAfterSet] = await client.maybeBox()

    expect(existsAfterSet).toBe(true)
    expect(value).toBe(testValue)
  })

  test('maybe box map returns correct value and existence', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testKey = 1n

    const [emptyValue, exists] = await client.maybeBoxMap({ args: { key: testKey } })
    expect(exists).toBe(false)
    expect(emptyValue).toBe('')

    const testString = 'Hello Box Map'
    await client
      .newGroup()
      .setBoxMap({
        args: { key: testKey, value: testString },
        boxReferences: [createBoxReference(client.appId, 'boxMap', testKey)],
      })
      .send()

    const [value, existsAfterSet] = await client.maybeBoxMap({ args: { key: testKey } })

    expect(existsAfterSet).toBe(true)
    expect(value).toBe(testString)
  })

  test('maybe box ref returns correct value and existence', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const { returns: beforeCreateReturns } = await client.send.maybeBoxRef({
      args: {
        key: 'maybeBoxRef',
      },
      boxReferences: [(client.appId, 'maybeBoxRef')],
    })

    const [valueBeforeCreate, existsBeforeCreate] = beforeCreateReturns?.[0]?.returnValue as [Uint8Array, boolean]

    expect(existsBeforeCreate).toBe(false)
    expect(valueBeforeCreate).toStrictEqual(new Uint8Array())
    expect(valueBeforeCreate.length).toBe(0)

    const { returns: afterCreateReturns } = await client
      .newGroup()
      .setBoxRef({
        args: { key: 'maybeBoxRef' },
        boxReferences: [(client.appId, 'maybeBoxRef')],
      })
      .maybeBoxRef({
        args: { key: 'maybeBoxRef' },
        boxReferences: [(client.appId, 'maybeBoxRef')],
      })
      .send()

    const [valueAfterCreate, existsAfterCreate] = afterCreateReturns?.[1] as [Uint8Array, boolean]

    expect(existsAfterCreate).toBe(true)
    expect(valueAfterCreate).toBeDefined()
    expect(valueAfterCreate.length).toBe(32)
  })

  test('set and read box map struct value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testStruct = {
      name: 'TestUser',
      id: 123n,
      asset: 456n,
    }

    await client
      .newGroup()
      .setBoxMapStruct({
        args: {
          key: 1n,
          value: testStruct,
        },
        boxReferences: [createBoxReference(client.appId, 'users', 1n)],
      })
      .send()

    const storedStruct = await client.getBoxMapStruct({
      args: { key: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    expect(storedStruct.name).toBe(testStruct.name)
    expect(storedStruct.id).toBe(testStruct.id)
    expect(storedStruct.asset).toBe(testStruct.asset)
  })

  test('delete boxes and verify deletion', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    await client
      .newGroup()
      .setBox({
        args: { valueInt: 123n },
        boxReferences: ['boxInt'],
      })
      .setBoxDynamicBytes({
        args: { value: new TextEncoder().encode('test bytes') },
        boxReferences: ['boxDynamicBytes'],
      })
      .setBoxString({
        args: { value: 'test string' },
        boxReferences: ['boxString'],
      })
      .send()

    await client
      .newGroup()
      .deleteBox({
        args: {},
        boxReferences: ['boxInt', 'boxDynamicBytes', 'boxString'],
      })
      .send()

    await Promise.all([
      expect(async () => {
        await client.state.box.boxInt()
      }).rejects.toThrow('box not found'),
      expect(async () => {
        await client.state.box.boxDynamicBytes()
      }).rejects.toThrow('box not found'),
      expect(async () => {
        await client.state.box.boxString()
      }).rejects.toThrow('box not found'),
    ])
  })

  test('delete box ref and verify deletion', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    await client.send.setBoxRef({
      args: {
        key: 'boxTobeDeleted',
      },
      boxReferences: [(client.appId, 'boxTobeDeleted')],
    })

    await client
      .newGroup()
      .deleteBoxRef({
        args: {
          key: 'boxTobeDeleted',
        },
        boxReferences: [(client.appId, 'boxTobeDeleted')],
      })
      .send()

    const { returns } = await client.send.maybeBoxRef({
      args: {
        key: 'boxTobeDeleted',
      },
      boxReferences: [(client.appId, 'boxTobeDeleted')],
    })

    const [value, exists] = returns?.[0]?.returnValue as [Uint8Array, boolean]
    expect(exists).toBe(false)
    expect(value).toBeDefined()
    expect(value.length).toBe(0)
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

  test('delete box map and verify deletion', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testString = 'Test String'
    await client
      .newGroup()
      .setBoxMap({
        args: { key: 1n, value: testString },
        boxReferences: [createBoxReference(client.appId, 'boxMap', 1n)],
      })
      .send()

    const boxValue = await client.getBoxMap({ args: { key: 1n } })
    expect(boxValue).toBe(testString)

    await client
      .newGroup()
      .deleteBoxMap({
        args: { key: 1n },
        boxReferences: [createBoxReference(client.appId, 'boxMap', 1n)],
      })
      .send()

    const defaultValue = await client.getBoxMapWithDefault({ args: { key: 1n } })
    expect(defaultValue).toBe('default')
  })

  test('box map length returns correct value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const initialLength = await client.boxMapLength({ args: { key: 0n } })
    expect(initialLength).toBe(0n)

    await client
      .newGroup()
      .setBoxMap({
        args: { key: 0n, value: 'Test String' },
        boxReferences: [createBoxReference(client.appId, 'boxMap', 0n)],
      })
      .send()

    const lengthAfterSet = await client.boxMapLength({ args: { key: 0n } })
    expect(lengthAfterSet).toBe(BigInt('Test String'.length))
  })

  test('length box ref returns correct value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const { returns } = await client.send.lengthBoxRef({
      args: { key: 'blob' },
      boxReferences: [(client.appId, 'blob')],
    })

    const length = returns?.[0]?.returnValue as bigint
    expect(length).toBe(32n)
  })

  test('box map exists returns correct value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const { returns: initialExists } = await client.send.boxMapExists({
      args: { key: 1n },
      boxReferences: [createBoxReference(client.appId, 'boxMap', 1n)],
    })

    expect(initialExists?.[0]?.returnValue).toBe(false)

    await client
      .newGroup()
      .setBoxMap({
        args: { key: 1n, value: 'Test String' },
        boxReferences: [createBoxReference(client.appId, 'boxMap', 1n)],
      })
      .send()

    const { returns: existsAfterSet } = await client.send.boxMapExists({
      args: { key: 1n },
      boxReferences: [createBoxReference(client.appId, 'boxMap', 1n)],
    })

    expect(existsAfterSet?.[0]?.returnValue).toBe(true)
  })

  test('box map struct exists returns correct value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const { returns: initialExists } = await client.send.boxMapStructExists({
      args: { key: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    expect(initialExists?.[0]?.returnValue).toBe(false)

    const testStruct = {
      name: 'TestUser',
      id: 123n,
      asset: 456n,
    }

    await client
      .newGroup()
      .setBoxMapStruct({
        args: {
          key: 1n,
          value: testStruct,
        },
        boxReferences: [createBoxReference(client.appId, 'users', 1n)],
      })
      .send()

    const { returns: existsAfterSet } = await client.send.boxMapStructExists({
      args: { key: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    expect(existsAfterSet?.[0]?.returnValue).toBe(true)
  })

  test('key prefix box map returns correct value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const keyPrefix = await client.keyPrefixBoxMap()
    expect(keyPrefix).toStrictEqual(new TextEncoder().encode('boxMap'))
  })

  test('box map struct length returns correct value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const { returns: result } = await client.send.boxMapStructLength({
      args: { key: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    expect(result?.[0]?.returnValue).toBe(true)

    const storedStruct = await client.getBoxMapStruct({
      args: { key: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    expect(storedStruct).toBeDefined()
    expect(storedStruct.name).toBe('testName')
    expect(storedStruct.id).toBe(70n)
    expect(storedStruct.asset).toBe(1234n)
  })

  test('arc4 box handles static array correctly', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const { returns } = await client.send.arc4Box({
      args: { key: 'staticArray' },
      boxReferences: [(client.appId, 'staticArray')],
    })

    const result = returns?.[0]?.returnValue as number[]

    expect(result[0]).toBe(0)
    expect(result[1]).toBe(1)
    expect(result[2]).toBe(2)
    expect(result[3]).toBe(3)
  })

  test('extract box ref handles data correctly', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    await client.send.extractBoxRef({
      args: { key: 'extractTest' },
      boxReferences: [(client.appId, 'extractTest')],
    })

    // The verification is done inside the contract itself
    // If the assertions fail, the transaction will fail
    // So if we get here, the test passed
    expect(true).toBe(true)
  })

  test('value box returns correct value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testValue = 42n
    await client
      .newGroup()
      .setBox({ args: { valueInt: testValue }, boxReferences: ['boxInt'] })
      .send()

    const value = await client.valueBox()
    expect(value).toBe(testValue)
  })
})
