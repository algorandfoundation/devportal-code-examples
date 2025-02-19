import { Config } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address } from 'algosdk'
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

  test('set and read box bytes value', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testString = 'Hello Box Storage'

    await client
      .newGroup()
      .setBoxBytes({ args: { value: testString }, boxReferences: ['boxBytes'] })
      .send()

    const boxValue = await client.state.box.boxBytes()
    expect(boxValue?.asString()).toBe(testString)
  })

  test('set and read box int value', async () => {
    const { testAccount } = localnet.context

    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const testValue = 42n

    await client
      .newGroup()
      .setBoxInt({ args: { value: testValue }, boxReferences: ['boxInt'] })
      .send()

    const boxValue = await client.state.box.boxInt()
    expect(boxValue).toBe(testValue)
  })

  test('verify app budget consumption is reasonable', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    await fundContract(testAccount, client.appAddress)

    const result = await client
      .newGroup()
      .setBoxBytes({ args: { value: 'Test String' }, boxReferences: ['boxBytes'] })
      .setBoxInt({ args: { value: 123n }, boxReferences: ['boxInt'] })
      .simulate()

    expect(result.simulateResponse.txnGroups[0].appBudgetConsumed).toBeLessThan(700)
  })
})
