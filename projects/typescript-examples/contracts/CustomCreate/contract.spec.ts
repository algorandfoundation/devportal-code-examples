import { TestExecutionContext } from '@algorandfoundation/algorand-typescript-testing'
import { describe, expect, it } from 'vitest'
import CustomCreate from './contract.algo'

describe('CustomCreate contract', () => {
  const ctx = new TestExecutionContext()
  it('get age', () => {
    const contract = ctx.contract.create(CustomCreate, { age: 28 })

    const result = contract.getAge()

    expect(result).toBe(28)
  })
})
