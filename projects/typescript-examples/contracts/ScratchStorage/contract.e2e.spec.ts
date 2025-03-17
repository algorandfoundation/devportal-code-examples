import { Config } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address } from 'algosdk'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { ScratchStorageFactory } from '../artifacts/clients/ScratchStorage/ScratchStorageClient'

describe('ScratchStorage contract', () => {
  const localnet = algorandFixture()
  beforeAll(() => {
    Config.configure({
      debug: true,
    })
    registerDebugEventHandlers()
  })
  beforeEach(localnet.newScope)

  const deploy = async (account: Address) => {
    const factory = localnet.algorand.client.getTypedAppFactory(ScratchStorageFactory, {
      defaultSender: account,
    })

    const { appClient } = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append', suppressLog: true })
    return { client: appClient }
  }

  test('demonstrateScratchStorage executes successfully', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const result = await client.newGroup().demonstrateScratchStorage().simulate()

    expect(result.returns).toBeDefined()
    expect(result.returns![0]).toBe(true)
  })

  test('read uint64 from group transaction', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const result = await client
      .newGroup()
      .demonstrateScratchStorage() // First transaction sets values in scratch slots
      .readFromGroupTransaction({ args: { groupIndex: 0n, scratchSlot: 0n } }) // Read uint64 value from first transaction
      .simulate()

    expect(result.returns).toBeDefined()
    expect(result.returns![1]).toBe(42n)
  })

  test('read bytes from group transaction', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const result = await client
      .newGroup()
      .demonstrateScratchStorage() // First transaction sets values in scratch slots
      .readBytesFromGroupTransaction({ args: { groupIndex: 0n, scratchSlot: 1n } }) // Read bytes from first transaction
      .simulate()

    expect(result.returns).toBeDefined()
    expect(result.returns![1]).toBeDefined()

    const bytesArray = result.returns![1]
    expect(bytesArray).toBeDefined()
    // Convert the returned bytes to a string for comparison
    expect(String.fromCharCode(...bytesArray!)).toBe('Hello, Algorand!')
  })

  test('verify app budget consumption is reasonable', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const result = await client
      .newGroup()
      .demonstrateScratchStorage()
      .readFromGroupTransaction({ args: { groupIndex: 0n, scratchSlot: 0n } })
      .readBytesFromGroupTransaction({ args: { groupIndex: 0n, scratchSlot: 1n } })
      .simulate()

    expect(result.simulateResponse.txnGroups[0].appBudgetConsumed).toBeLessThan(120)
  })
})
