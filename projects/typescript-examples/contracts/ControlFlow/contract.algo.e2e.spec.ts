import { Config } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address } from 'algosdk'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { ControlFlowFactory } from '../artifacts/clients/ControlFlow/ControlFlowClient'

describe('ControlFlow contract', () => {
  const localnet = algorandFixture()
  beforeAll(() => {
    Config.configure({
      debug: true,
    })
    registerDebugEventHandlers()
  })
  beforeEach(localnet.newScope)

  const deploy = async (account: Address) => {
    const factory = localnet.algorand.client.getTypedAppFactory(ControlFlowFactory, {
      defaultSender: account,
    })

    const { appClient } = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append', suppressLog: true })
    return { client: appClient }
  }

  test('isRich method returns correct values', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const richResult = await client.isRich({ args: { accountBalance: 2000 } })
    expect(richResult).toBe('This account is rich!')

    const okResult = await client.isRich({ args: { accountBalance: 500 } })
    expect(okResult).toBe('This account is doing well.')

    const poorResult = await client.isRich({ args: { accountBalance: 50 } })
    expect(poorResult).toBe('This account is poor :(')
  })

  test('isEven method returns correct values', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const evenResult = await client.isEven({ args: { number: 2 } })
    expect(evenResult).toBe('Even')

    const oddResult = await client.isEven({ args: { number: 3 } })
    expect(oddResult).toBe('Odd')

    const zeroResult = await client.isEven({ args: { number: 0 } })
    expect(zeroResult).toBe('Even')
  })

  test('forLoop method returns correct array', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const result = await client.forLoop()

    expect(result).toBeDefined()
    const array = result

    // Check that the array contains [3, 2, 1, 0]
    expect(array[0]).toBe(3n)
    expect(array[1]).toBe(2n)
    expect(array[2]).toBe(1n)
    expect(array[3]).toBe(0n)
  })

  test('getDay method returns correct day names', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const days = ['Invalid day', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    for (let i = 0; i < 7; i++) {
      const result = await client.getDay({ args: { date: i } })
      expect(result).toBe(days[i])
    }

    const invalidResult = await client.getDay({ args: { date: 10 } })
    expect(invalidResult).toBe('Invalid day')
  })

  test('loop method returns correct loop count', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const result = await client.loop()
    expect(result).toBe(7n)
  })

  test('calculateBoxStorageCost returns correct MBR values', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    // Test with different box size labels
    const tinyBoxCost = await client.calculateBoxStorageCost({
      args: { boxSizeLabel: 'xs', boxName: 'counter' },
    })
    expect(tinyBoxCost).toBe(8500n) // 2500 + 400 * (7 + 8) = 8500

    const smallBoxCost = await client.calculateBoxStorageCost({
      args: { boxSizeLabel: 'sm', boxName: 'user' },
    })
    expect(smallBoxCost).toBe(29700n) // 2500 + 400 * (4 + 64) = 29700

    const mediumBoxCost = await client.calculateBoxStorageCost({
      args: { boxSizeLabel: 'md', boxName: 'settings' },
    })
    expect(mediumBoxCost).toBe(108100n) // 2500 + 400 * (8 + 256) = 108100

    const largeBoxCost = await client.calculateBoxStorageCost({
      args: { boxSizeLabel: 'lg', boxName: 'data' },
    })
    expect(largeBoxCost).toBe(413700n) // 2500 + 400 * (4 + 1024) = 413700

    const maxBoxCost = await client.calculateBoxStorageCost({
      args: { boxSizeLabel: 'max', boxName: 'bigdata' },
    })
    expect(maxBoxCost).toBe(12805300n) // 2500 + 400 * (7 + 32000) = 12805300

    // Test with invalid box size label
    const invalidBoxCost = await client.calculateBoxStorageCost({
      args: { boxSizeLabel: 'invalid', boxName: 'test' },
    })
    expect(invalidBoxCost).toBe(0n)
  })
})
