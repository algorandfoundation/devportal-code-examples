import { Config } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { HelloWorldFactory } from '../artifacts/clients/HelloWorld/HelloWorldClient'

describe('HelloWorld contract', () => {
  const localnet = algorandFixture()
  beforeAll(() => {
    Config.configure({
      debug: true,
      // traceAll: true,
    })
    registerDebugEventHandlers()
  })
  beforeEach(localnet.newScope)

  const deploy = async (address: string) => {
    const factory = localnet.algorand.client.getTypedAppFactory(HelloWorldFactory, {
      defaultSender: address,
    })

    const { appClient } = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append', suppressLog: true })
    return { client: appClient }
  }

  test('say hello and bananas', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())

    const result = await client
      .newGroup()
      .sayHello({ args: { firstName: 'Silvio', lastName: 'Micali' } })
      .sayBananas()
      .simulate()

    expect(result.returns[0]).toBe('Hello Silvio Micali')
    expect(result.returns[1]).toBe('Bananas')
  })

  test('simulate say hello and bananas with correct budget consumed', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount.addr.toString())
    const result = await client
      .newGroup()
      .sayHello({ args: { firstName: 'Silvio', lastName: 'Micali' } })
      .sayBananas()
      .simulate()

    expect(result.returns[0]).toBe('Hello Silvio Micali')
    expect(result.returns[1]).toBe('Bananas')
    expect(result.simulateResponse.txnGroups[0].appBudgetConsumed).toBeLessThan(100)
  })
})
