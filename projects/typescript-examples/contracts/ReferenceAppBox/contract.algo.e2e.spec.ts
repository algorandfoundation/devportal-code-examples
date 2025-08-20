import { Config, microAlgo } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { algorandFixture } from '@algorandfoundation/algokit-utils/testing'
import { Address } from 'algosdk'
import { beforeAll, beforeEach, describe, expect, test } from 'vitest'
import { ReferenceAppBoxFactory } from '../artifacts/clients/ReferenceAppBox/ReferenceAppBoxClient'

describe('BoxCounter contract', () => {
  const localnet = algorandFixture()
  beforeAll(() => {
    Config.configure({
      debug: true,
    })
    registerDebugEventHandlers()
  })
  beforeEach(localnet.newScope)

  const deploy = async (account: Address) => {
    const factory = localnet.algorand.client.getTypedAppFactory(ReferenceAppBoxFactory, {
      defaultSender: account,
    })

    const { appClient } = await factory.deploy({ onUpdate: 'append', onSchemaBreak: 'append', suppressLog: true })
    return { client: appClient }
  }

  const fundContract = async (sender: Address, receiver: Address, amount: number) => {
    await localnet.algorand.send.payment({
      sender,
      receiver,
      amount: microAlgo(amount),
    })
  }

  const createBoxReference = (address: Address, boxPrefix: string) => {
    const encoder = new TextEncoder()
    const boxPrefixBytes = encoder.encode(boxPrefix) //UInt8Array of boxPrefix
    const publicKey = address.publicKey

    return new Uint8Array([...boxPrefixBytes, ...publicKey])
  }

  test('get box configuration values from global state', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    // Get the box configuration values
    const result = await client.getBoxConfiguration({
      args: {},
      boxReferences: [createBoxReference(testAccount.addr, 'counter')],
    })

    expect(result).toBeDefined()
    const [keyLength, valueLength, boxSize, boxMbr] = result

    // Verify expected initial values
    expect(keyLength).toBe(51n) // 32 + 19
    expect(valueLength).toBe(8n) // size of uint64
    expect(boxSize).toBe(59n) // keyLength + valueLength
    expect(boxMbr).toBe(26100n) // 2500 + 59 * 400
  })

  test('get box MBR cost', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    const result = await client.getBoxMbr()
    expect(result).toBe(26100n) // Initial MBR: 2500 + 59 * 400
  })

  test('increment box counter with payment', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    // Get the MBR cost
    const mbrResult = await client.getBoxMbr()
    const mbr = mbrResult

    // Ensure the app account has enough balance
    await fundContract(testAccount, client.appAddress, 1_000_000)

    // Create a payment for the MBR
    const mbrPayment = await localnet.algorand.createTransaction.payment({
      sender: testAccount,
      receiver: client.appAddress,
      amount: microAlgo(mbr),
      signer: testAccount,
    })

    // Create a payment for the MBR
    const result = await client
      .newGroup()
      .incrementBoxCounter({
        args: {
          payMbr: mbrPayment, // Reference to the payment transaction
        },
        sender: testAccount,
        boxReferences: [createBoxReference(testAccount.addr, 'counter')],
      })
      .send()

    // Check the counter result
    expect(result.returns[0]).toBe(1n) // First increment should return 1

    // Get the counter value for the sender
    const counterResult = await client.getBoxCounter()
    expect(counterResult).toBe(1n)

    // Get the counter for a specific account
    const accountCounterResult = await client.getBoxCounterForAccount({
      args: {
        account: testAccount.addr.toString(),
      },
    })

    expect(accountCounterResult).toBe(1n)
  })

  test('increment box counter multiple times', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    // Get the MBR cost
    const mbr = await client.getBoxMbr()

    // Ensure the app account has enough balance
    await fundContract(testAccount, client.appAddress, 100_000)

    // Create a payment for the first MBR
    const mbrPayment1 = await localnet.algorand.createTransaction.payment({
      sender: testAccount,
      receiver: client.appAddress,
      amount: microAlgo(mbr),
      signer: testAccount,
    })

    // First increment (need to pay MBR)
    await client
      .newGroup()
      .incrementBoxCounter({
        args: {
          payMbr: mbrPayment1,
        },
        sender: testAccount,
        boxReferences: [createBoxReference(testAccount.addr, 'counter')],
      })
      .send()

    // Create a payment for the second MBR
    const mbrPayment2 = await localnet.algorand.createTransaction.payment({
      sender: testAccount,
      receiver: client.appAddress,
      amount: microAlgo(mbr),
      signer: testAccount,
    })

    // Second increment
    const secondIncrementResult = await client
      .newGroup()
      .incrementBoxCounter({
        args: {
          payMbr: mbrPayment2,
        },
        sender: testAccount,
        boxReferences: [createBoxReference(testAccount.addr, 'counter')],
      })
      .send()

    expect(secondIncrementResult.returns[0]).toBe(2n) // Should be 2 after second increment

    // Check final counter value
    const counterResult = await client.getBoxCounter()
    expect(counterResult).toBe(2n)
  })

  test('get counter for non-existent account returns zero', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    // Generate a random account that hasn't interacted with the contract
    const randomAccount = localnet.algorand.account.random()

    // Try to get counter for that account
    const result = await client.getBoxCounterForAccount({
      args: {
        account: randomAccount.addr.toString(),
      },
    })

    // Should return 0 for non-existent counter
    expect(result).toBe(0n)
  })

  test('fails when payment amount is incorrect', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    // Get the MBR cost
    const mbr = await client.getBoxMbr()

    // Ensure the app account has enough balance
    await fundContract(testAccount, client.appAddress, 100_000)

    // Create an incorrect payment (1 microAlgo less than required)
    const incorrectPayment = await localnet.algorand.createTransaction.payment({
      sender: testAccount,
      receiver: client.appAddress,
      amount: microAlgo(Number(mbr) - 1), // Pay 1 less than required
      signer: testAccount,
    })

    // Try to increment with incorrect payment amount
    await expect(
      client
        .newGroup()
        .incrementBoxCounter({
          args: {
            payMbr: incorrectPayment,
          },
          sender: testAccount,
          boxReferences: [createBoxReference(testAccount.addr, 'counter')],
        })
        .simulate(),
    ).rejects.toThrow('Payment must cover the box MBR')
  })

  test('fails when payment receiver is incorrect', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    // Ensure the app account has enough balance
    await fundContract(testAccount, client.appAddress, 100_000)

    // Get the MBR cost
    const mbr = await client.getBoxMbr()

    // Generate a different account
    const otherAccount = localnet.algorand.account.random()
    const localnetDispenser = await localnet.algorand.account.localNetDispenser()

    await localnet.algorand.send.payment({
      sender: localnetDispenser,
      receiver: testAccount,
      amount: microAlgo(100_000),
      signer: localnetDispenser,
    })

    // Fund the other account so it can complete payment
    await localnet.algorand.send.payment({
      sender: localnetDispenser,
      receiver: otherAccount,
      amount: microAlgo(100_000),
      signer: localnetDispenser,
    })

    // Create a payment to the wrong address
    const incorrectReceiverPayment = await localnet.algorand.createTransaction.payment({
      sender: testAccount,
      receiver: otherAccount, // Send to wrong address
      amount: microAlgo(mbr),
      signer: testAccount,
    })

    // Try to increment with incorrect payment receiver
    await expect(
      client
        .newGroup()
        .incrementBoxCounter({
          args: {
            payMbr: incorrectReceiverPayment,
          },
          sender: testAccount,
          boxReferences: [createBoxReference(testAccount.addr, 'counter')],
        })
        .simulate(),
    ).rejects.toThrow('Payment must be to the contract')
  })

  test('verify app budget consumption is reasonable', async () => {
    const { testAccount } = localnet.context
    const { client } = await deploy(testAccount)

    // This test needs to use simulation to check budget consumption
    const result = await client
      .newGroup()
      .getBoxMbr()
      .getBoxConfiguration({
        args: {},
        boxReferences: [createBoxReference(testAccount.addr, 'counter')],
        sender: testAccount,
      })
      .updateBoxConfiguration({
        args: {
          newKeyLength: 60,
          newValueLength: 10,
        },
        sender: testAccount,
      })
      .simulate()

    // Check budget consumption is reasonable
    expect(result.simulateResponse.txnGroups[0].appBudgetConsumed).toBeLessThan(700)
  })
})
