import { Bytes, OnCompleteAction } from '@algorandfoundation/algorand-typescript'
import { TestExecutionContext } from '@algorandfoundation/algorand-typescript-testing'
import { describe, expect, it } from 'vitest'
import LocalStorage from './contract.algo'

describe('LocalStorage contract', () => {
  const ctx = new TestExecutionContext()

  it('should initialize local state with correct values after opting in', () => {
    const contract = ctx.contract.create(LocalStorage)

    contract.optInToApplication()

    const [localInt, localIntNoDefault, localBytes, localString, localBool, localAddress] = contract.readLocalState()

    expect(localInt.valueOf()).toBe(100)
    expect(localIntNoDefault.valueOf()).toBe(200)
    expect(localBytes.toString()).toBe(Bytes('Silvio').toString())
    expect(localString).toBe('Micali')
    expect(localBool).toBe(true)
    expect(localAddress.bytes.toString()).toBe(ctx.defaultSender.bytes.toString())
  })

  it('should write and verify multiple local state values', () => {
    const contract = ctx.contract.create(LocalStorage)
    const account = ctx.any.account({ optedApplications: [ctx.ledger.getApplicationForContract(contract)] })

    ctx.txn
      .createScope([
        ctx.any.txn.applicationCall({ appId: contract, sender: account, onCompletion: OnCompleteAction.OptIn }),
      ])
      .execute(() => {
        contract.optInToApplication()
      })

    ctx.txn.createScope([ctx.any.txn.applicationCall({ appId: contract, sender: account })]).execute(() => {
      contract.writeLocalState('New String', false, account)

      const [, , , localString, localBool, localAccount] = contract.readLocalState()

      expect(localString).toBe('New String')
      expect(localBool).toBe(false)
      expect(localAccount.bytes.toString()).toEqual(account.bytes.toString())
    })
  })

  it('should write and read dynamic local state values', () => {
    const contract = ctx.contract.create(LocalStorage)
    const account = ctx.any.account({ optedApplications: [ctx.ledger.getApplicationForContract(contract)] })

    ctx.txn
      .createScope([
        ctx.any.txn.applicationCall({ appId: contract, sender: account, onCompletion: OnCompleteAction.OptIn }),
      ])
      .execute(() => {
        contract.optInToApplication()
      })

    ctx.txn.createScope([ctx.any.txn.applicationCall({ appId: contract, sender: account })]).execute(() => {
      const testKey = 'testKey'
      const testValue = 'testValue'

      const writtenValue = contract.writeDynamicLocalState(testKey, testValue)
      expect(writtenValue).toBe(testValue)

      const readValue = contract.readDynamicLocalState(testKey)
      expect(readValue).toBe(testValue)
    })
  })

  it('should clear all local state values', () => {
    const contract = ctx.contract.create(LocalStorage)
    const account = ctx.any.account({ optedApplications: [ctx.ledger.getApplicationForContract(contract)] })
    ctx.txn
      .createScope([
        ctx.any.txn.applicationCall({ appId: contract, sender: account, onCompletion: OnCompleteAction.OptIn }),
      ])
      .execute(() => {
        contract.optInToApplication()
      })

    ctx.txn.createScope([ctx.any.txn.applicationCall({ appId: contract, sender: account })]).execute(() => {
      contract.clearLocalState()

      expect(() => contract.readLocalState()).toThrow()
    })
  })

  it('should fail to write local state if not opted in', () => {
    const contract = ctx.contract.create(LocalStorage)
    const newAccount = ctx.defaultSender

    expect(() => contract.writeLocalState('New String', false, newAccount)).toThrow(
      'Account must opt in to contract first',
    )
  })

  it('should fail to read dynamic local state for non-existent key', () => {
    const contract = ctx.contract.create(LocalStorage)
    const account = ctx.any.account({ optedApplications: [ctx.ledger.getApplicationForContract(contract)] })
    ctx.txn
      .createScope([
        ctx.any.txn.applicationCall({ appId: contract, sender: account, onCompletion: OnCompleteAction.OptIn }),
      ])
      .execute(() => {
        contract.optInToApplication()
      })

    ctx.txn.createScope([ctx.any.txn.applicationCall({ appId: contract, sender: account })]).execute(() => {
      expect(() => contract.readDynamicLocalState('nonexistentKey')).toThrow('Key not found')
    })
  })
})
