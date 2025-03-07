import { TestExecutionContext } from '@algorandfoundation/algorand-typescript-testing'
import { describe, expect, it } from 'vitest'
import ScratchStorage from './contract.algo'

describe('ScratchStorage contract', () => {
  const ctx = new TestExecutionContext()

  it('Successfully demonstrates basic scratch storage operations', () => {
    const contract = ctx.contract.create(ScratchStorage)
    const result = contract.demonstrateScratchStorage()

    expect(result).toBe(true)
  })
})
