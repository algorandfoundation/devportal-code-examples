import { TestExecutionContext } from '@algorandfoundation/algorand-typescript-testing'
import { describe, expect, it } from 'vitest'
import HelloWorld from './contract.algo'

describe('HelloWrodl contract', () => {
  const ctx = new TestExecutionContext()
  it('Logs the returned value when sayHello is called', () => {
    const contract = ctx.contract.create(HelloWorld)

    const result = contract.sayHello('Sally', 'Jones')

    expect(result).toBe('Hello Sally Jones')
  })

  it('Logs the returned value when sayBananas is called', () => {
    const contract = ctx.contract.create(HelloWorld)

    const result = contract.sayBananas()

    expect(result).toBe('Bananas')
  })
})
