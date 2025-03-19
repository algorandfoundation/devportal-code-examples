import { Config, algo } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address } from 'algosdk'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { ReferenceAccountFactory } from '../artifacts/clients/ReferenceAccount/ReferenceAccountClient'

describe('ResourceUsage contract', () => {
  const localnet = algorandFixture()

  beforeAll(() => {
    Config.configure({
      debug: true,
    })
    registerDebugEventHandlers()
  })

  beforeEach(localnet.newScope)

  const deploy = async (account: Address) => {
    const factory = localnet.algorand.client.getTypedAppFactory(ReferenceAccountFactory, {
      defaultSender: account,
    })

    await localnet.algorand.account.ensureFundedFromEnvironment(account, algo(200))

    const { appClient } = await factory.deploy({
      onUpdate: 'append',
      onSchemaBreak: 'append',
    })

    return { client: appClient }
  }

  const createReferenceAccount = async () => {
    const referenceAccount = localnet.algorand.account.fromMnemonic(
      'rice broken rail solve mobile pill glue maximum speak mean stumble orbit mixed empower rent congress nest input peanut crush comfort spell swear abandon actual',
    )

    await localnet.algorand.account.ensureFundedFromEnvironment(referenceAccount, algo(1))

    return referenceAccount
  }

  test('get account balance with reference account', async () => {
    const { testAccount } = localnet.context
    const referenceAccount = await createReferenceAccount()
    await localnet.algorand.account.ensureFundedFromEnvironment(testAccount, algo(1))
    const { client } = await deploy(testAccount)

    const { return: result } = await client.send.getAccountBalance({
      args: {},
      sender: testAccount,
      accountReferences: [referenceAccount],
      populateAppCallResources: false,
    })

    expect(typeof result).toBe('bigint')
    expect(result).toBeGreaterThan(0n)
  })

  test('fail to get account balance without reference account', async () => {
    const { testAccount } = localnet.context

    await localnet.algorand.account.ensureFundedFromEnvironment(testAccount, algo(1))

    const { client } = await deploy(testAccount)

    await expect(async () => {
      await client.send.getAccountBalance({
        args: {},
        sender: testAccount,
        accountReferences: [],
        populateAppCallResources: false,
      })
    }).rejects.toThrow('invalid Account reference')
  })

  test('get account balance with argument by passing account reference as argument', async () => {
    const { testAccount } = localnet.context
    await localnet.algorand.account.ensureFundedFromEnvironment(testAccount, algo(100))

    const { client } = await deploy(testAccount)

    const { return: result } = await client.send.getAccountBalanceWithArgument({
      args: {
        account: testAccount.addr.publicKey,
      },
      sender: testAccount,
      populateAppCallResources: false,
    })

    expect(typeof result).toBe('bigint')
    expect(result).toBeGreaterThan(0n)
  })
})
