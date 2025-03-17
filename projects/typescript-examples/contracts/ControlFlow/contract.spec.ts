import { TestExecutionContext } from '@algorandfoundation/algorand-typescript-testing'
import { describe, expect, it } from 'vitest'
import ControlFlow from './contract.algo'

describe('ControlFlow contract', () => {
  const ctx = new TestExecutionContext()

  describe('IF_ELSE tests', () => {
    it('should correctly determine if an account is rich', () => {
      const contract = ctx.contract.create(ControlFlow)

      expect(contract.isRich(2000)).toBe('This account is rich!')
      expect(contract.isRich(500)).toBe('This account is doing well.')
      expect(contract.isRich(50)).toBe('This account is poor :(')
    })

    it('should correctly determine if a number is even or odd', () => {
      const contract = ctx.contract.create(ControlFlow)

      expect(contract.isEven(2)).toBe('Even')
      expect(contract.isEven(3)).toBe('Odd')
      expect(contract.isEven(0)).toBe('Even')
      expect(contract.isEven(101)).toBe('Odd')
    })
  })

  describe('FOR_LOOP tests', () => {
    it('should correctly implement for loops', () => {
      const contract = ctx.contract.create(ControlFlow)

      const result = contract.forLoop()

      // Check that the array contains [3, 2, 1, 0]
      expect(result[0].valueOf()).toBe(3n)
      expect(result[1].valueOf()).toBe(2n)
      expect(result[2].valueOf()).toBe(1n)
      expect(result[3].valueOf()).toBe(0n)
    })
  })

  describe('MATCH tests', () => {
    it('should return the correct day name based on number', () => {
      const contract = ctx.contract.create(ControlFlow)

      expect(contract.getDay(1)).toBe('Monday')
      expect(contract.getDay(2)).toBe('Tuesday')
      expect(contract.getDay(3)).toBe('Wednesday')
      expect(contract.getDay(4)).toBe('Thursday')
      expect(contract.getDay(5)).toBe('Friday')
      expect(contract.getDay(6)).toBe('Saturday')
      expect(contract.getDay(7)).toBe('Sunday')
      expect(contract.getDay(0)).toBe('Invalid day')
    })
  })

  describe('WHILE_LOOP tests', () => {
    it('should correctly implement while loop with continue and break', () => {
      const contract = ctx.contract.create(ControlFlow)

      const loopCount = contract.loop()

      // The loop should execute 7 times based on the implementation
      expect(loopCount).toBe(7)
    })
  })

  describe('SWITCH tests', () => {
    it('should calculate correct MBR for different box sizes', () => {
      const contract = ctx.contract.create(ControlFlow)

      // Test with different box size labels
      const tinyBoxCost = contract.calculateBoxStorageCost('xs', 'counter')
      const smallBoxCost = contract.calculateBoxStorageCost('sm', 'user')
      const mediumBoxCost = contract.calculateBoxStorageCost('md', 'settings')
      const largeBoxCost = contract.calculateBoxStorageCost('lg', 'data')
      const maxBoxCost = contract.calculateBoxStorageCost('max', 'bigdata')

      // Expected values calculated using the formula: 2500 + 400 * (name.length + boxSize)
      // 'xs' box (8 bytes) with name 'counter' (7 bytes): 2500 + 400 * (7 + 8) = 2500 + 400 * 15 = 2500 + 6000 = 8500
      expect(tinyBoxCost.valueOf()).toBe(8500n)

      // 'sm' box (64 bytes) with name 'user' (4 bytes): 2500 + 400 * (4 + 64) = 2500 + 400 * 68 = 2500 + 27200 = 29700
      expect(smallBoxCost.valueOf()).toBe(29700n)

      // 'md' box (256 bytes) with name 'settings' (8 bytes): 2500 + 400 * (8 + 256) = 2500 + 400 * 264 = 2500 + 105600 = 108100
      expect(mediumBoxCost.valueOf()).toBe(108100n)

      // 'lg' box (1024 bytes) with name 'data' (4 bytes): 2500 + 400 * (4 + 1024) = 2500 + 400 * 1028 = 2500 + 411200 = 413700
      expect(largeBoxCost.valueOf()).toBe(413700n)

      // 'max' box (32000 bytes) with name 'bigdata' (7 bytes): 2500 + 400 * (7 + 32000) = 2500 + 400 * 32007 = 2500 + 12802800 = 12805300
      expect(maxBoxCost.valueOf()).toBe(12805300n)
    })

    it('should return 0 for invalid box size labels', () => {
      const contract = ctx.contract.create(ControlFlow)

      // Test with invalid box size label
      const invalidBoxCost = contract.calculateBoxStorageCost('invalid', 'test')

      // Should return 0 for invalid labels
      expect(invalidBoxCost.valueOf()).toBe(0)
    })
  })
})
