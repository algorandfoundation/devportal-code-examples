import { Config } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address, ABIUintType } from 'algosdk'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { StructInBoxMapFactory } from '../artifacts/clients/StructInBoxMap/StructInBoxMapClient'

describe('StructInBox contract', () => {
  const localnet = algorandFixture()
  beforeAll(() => {
    Config.configure({
      debug: true,
    })
    registerDebugEventHandlers()
  })
  beforeEach(localnet.newScope)

  const deploy = async (account: Address) => {
    const factory = localnet.algorand.client.getTypedAppFactory(StructInBoxMapFactory, {
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

  test('box map test creates and verifies struct', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const { returns } = await client.send.boxMapTest({
      args: {},
      boxReferences: [createBoxReference(client.appId, 'users', 0n)],
    })

    expect(returns?.[0]?.returnValue).toBe(true)
  })

  test('set and get box map struct', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testStruct = {
      name: 'TestUser',
      id: 123n,
      asset: 456n,
    }

    await client.send.boxMapSet({
      args: {
        key: 1n,
        value: testStruct,
      },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    const { returns } = await client.send.boxMapGet({
      args: { key: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    const [name, id, asset] = returns?.[0]?.returnValue as [string, bigint, bigint]
    expect(name).toBe(testStruct.name)
    expect(id).toBe(testStruct.id)
    expect(asset).toBe(testStruct.asset)
  })

  test('box map exists returns correct value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const { returns: initialReturns } = await client.send.boxMapExists({
      args: { key: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    expect(initialReturns?.[0]?.returnValue).toBe(false)

    const testStruct = {
      name: 'TestUser',
      id: 123n,
      asset: 456n,
    }

    await client.send.boxMapSet({
      args: {
        key: 1n,
        value: testStruct,
      },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    const { returns: existsReturns } = await client.send.boxMapExists({
      args: { key: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    expect(existsReturns?.[0]?.returnValue).toBe(true)
  })
})
