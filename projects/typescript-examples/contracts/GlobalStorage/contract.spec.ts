import { Bytes } from '@algorandfoundation/algorand-typescript'
import { TestExecutionContext } from '@algorandfoundation/algorand-typescript-testing'
import { describe, expect, it } from 'vitest'
import GlobalStorage from './contract.algo'

describe('GlobalStorage contract', () => {
  const ctx = new TestExecutionContext()

  it('should initialize global state variables with correct values when accessed via properties', () => {
    const contract = ctx.contract.create(GlobalStorage)

    expect(contract.globalInt.value.valueOf()).toBe(50n)
    expect(contract.globalIntNoDefault.value.valueOf()).toBe(0n)
    expect(contract.globalBytes.value.toString()).toBe(Bytes('Silvio').toString())
    expect(contract.globalString.value).toBe('Micali')
    expect(contract.globalBool.value).toBe(true)
    expect(contract.globalAccount.value).toBe(ctx.defaultSender)
  })

  it('should show global state variables with correct values when read via readGlobalState', () => {
    const contract = ctx.contract.create(GlobalStorage)
    const [globalInt, globalIntNoDefault, globalBytes, globalString, globalBool, globalAddress] =
      contract.readGlobalState()

    expect(globalInt.valueOf()).toBe(50n)
    expect(globalIntNoDefault.valueOf()).toBe(0n)
    expect(globalBytes.toString()).toBe(Bytes('Silvio').toString())
    expect(globalString).toBe('Micali')
    expect(globalBool).toBe(true)
    expect(globalAddress.bytes.toString()).toBe(ctx.defaultSender.bytes.toString())
  })

  it('should check if global state exists and return correct values', () => {
    const contract = ctx.contract.create(GlobalStorage)
    const [value, hasValue] = contract.hasGlobalState()

    expect(value.valueOf()).toBe(0n)
    expect(hasValue).toBe(true)
  })

  it('should write and verify multiple global state values', () => {
    const contract = ctx.contract.create(GlobalStorage)
    const newAccount = ctx.defaultSender

    contract.writeGlobalState('New String', false, newAccount)

    expect(contract.globalString.value).toBe('New String')
    expect(contract.globalBool.value).toBe(false)
    expect(contract.globalAccount.value).toBe(newAccount)
  })

  it('should write and read dynamic global state values', () => {
    const contract = ctx.contract.create(GlobalStorage)
    const testKey = 'testKey'
    const testValue = 'testValue'

    const returnedValue = contract.writeDynamicGlobalState(testKey, testValue)

    expect(returnedValue).toBe(testValue)
  })
})
