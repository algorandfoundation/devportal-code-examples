import { Config, algo } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address } from 'algosdk'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { ReferenceAssetFactory } from '../artifacts/clients/ReferenceAsset/ReferenceAssetClient'

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
    const factory = localnet.algorand.client.getTypedAppFactory(ReferenceAssetFactory, {
      defaultSender: account,
    })

    await localnet.algorand.account.ensureFundedFromEnvironment(account, algo(200))

    const { appClient } = await factory.deploy({
      onUpdate: 'append',
      onSchemaBreak: 'append',
    })

    return { client: appClient }
  }

  const createReferenceAsset = async () => {
    const { assetId } = await localnet.algorand.send.assetCreate({
      sender: localnet.context.testAccount,
      total: 1_000_000_000n,
      decimals: 6,
      assetName: 'Reference Asset',
      unitName: 'REF',
    })

    return assetId
  }

  // test('get asset total supply with reference asset', async () => {
  //   const { testAccount } = localnet.context
  //   const referenceAssetId = await createReferenceAsset()

  //   const { client } = await deploy(testAccount)

  //   const { return: result } = await client.send.getAssetTotalSupply({
  //     args: {},
  //     sender: testAccount,
  //     assetReferences: [referenceAssetId],
  //     populateAppCallResources: false,
  //   })

  //   console.log('result', result)

  //   expect(typeof result).toBe('bigint')
  //   expect(result).toBeGreaterThan(0n)
  // })

  test('fail to get asset total supply without reference asset', async () => {
    const { testAccount } = localnet.context

    const { client } = await deploy(testAccount)

    await expect(async () => {
      await client.send.getAssetTotalSupply({
        args: {},
        sender: testAccount,
        populateAppCallResources: false,
      })
    }).rejects.toThrow('unavailable Asset')
  })

  test('get asset total supply with reference asset as argument', async () => {
    const { testAccount } = localnet.context
    const referenceAssetId = await createReferenceAsset()

    const { client } = await deploy(testAccount)

    const { return: result } = await client.send.getAssetTotalSupplyWithArgument({
      args: { asset: referenceAssetId },
      sender: testAccount,
      populateAppCallResources: false,
    })

    expect(typeof result).toBe('bigint')
    expect(result).toBeGreaterThan(0n)
  })
})
