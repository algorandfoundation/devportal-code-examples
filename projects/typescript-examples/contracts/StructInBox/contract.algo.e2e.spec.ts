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
    const encodedPrefix = new TextEncoder().encode(prefix)
    const boxName = new Uint8Array([...encodedPrefix, ...encodedKey])

    return {
      appId,
      name: boxName,
    }
  }

  test('create and get user struct', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testUser = {
      id: 1n,
      name: 'TestUser',
      age: 25n,
    }

    await client.send.createNewUser({
      args: {
        id: 1n,
        user: testUser,
      },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    const { returns } = await client.send.getUser({
      args: { id: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    const [id, name, age] = returns?.[0]?.returnValue as [bigint, string, bigint]
    expect(id).toBe(testUser.id)
    expect(name).toBe(testUser.name)
    expect(age).toBe(testUser.age)
  })

  test('check user exists returns correct value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const { returns: initialReturns } = await client.send.checkUserExists({
      args: { id: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    expect(initialReturns?.[0]?.returnValue).toBe(false)

    const testUser = {
      id: 1n,
      name: 'TestUser',
      age: 25n,
    }

    await client.send.createNewUser({
      args: {
        id: 1n,
        user: testUser,
      },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    const { returns: existsReturns } = await client.send.checkUserExists({
      args: { id: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    expect(existsReturns?.[0]?.returnValue).toBe(true)
  })

  test('update user name and age', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testUser = {
      id: 1n,
      name: 'TestUser',
      age: 25n,
    }

    // Create user first
    await client.send.createNewUser({
      args: {
        id: 1n,
        user: testUser,
      },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    // Update user
    await client.send.updateUserNameAndAge({
      args: {
        id: 1n,
        name: 'UpdatedUser',
        age: 30n,
      },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    // Verify the update
    const { returns } = await client.send.getUser({
      args: { id: 1n },
      boxReferences: [createBoxReference(client.appId, 'users', 1n)],
    })

    const [id, name, age] = returns?.[0]?.returnValue as [bigint, string, bigint]
    expect(id).toBe(testUser.id)
    expect(name).toBe('UpdatedUser')
    expect(age).toBe(30n)
  })
})
