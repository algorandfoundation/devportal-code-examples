import { Uint64 } from '@algorandfoundation/algorand-typescript'
import { TestExecutionContext } from '@algorandfoundation/algorand-typescript-testing'
import { describe, expect, it } from 'vitest'
import BoxStorage from './contract.algo'

describe('BoxStorage contract', () => {
  const ctx = new TestExecutionContext()

  describe('Basic Box Operations', () => {
    it('should set and get box integer value', () => {
      const contract = ctx.contract.create(BoxStorage)
      const testValue = Uint64(42)

      contract.setBox(testValue)
      expect(contract.getBox()).toStrictEqual(testValue)
      expect(contract.valueBox()).toStrictEqual(testValue)
    })

    it('should set and get box string value', () => {
      const contract = ctx.contract.create(BoxStorage)
      const testString = 'test string'

      contract.setBoxString(testString)
      const [value, exists] = contract.boxString.maybe()
      expect(exists).toBe(true)
      expect(value).toBe(testString)
    })

    /** @TODO figure out how to test this */
    // it('should set and get dynamic bytes value', () => {
    //   const contract = ctx.contract.create(BoxStorage)
    //   const testBytes = new arc4.DynamicBytes('test bytes')

    //   contract.setBoxDynamicBytes(testBytes)
    //   const [, exists] = contract.maybeBox()
    //   expect(exists).toBe(true)
    // })

    it('should delete box values and return default values when using get', () => {
      const contract = ctx.contract.create(BoxStorage)
      const testValue = Uint64(42)

      contract.setBox(testValue)
      contract.deleteBox()

      // Check that the box doesn't exist using maybe
      const [value, exists] = contract.maybeBox()
      expect(exists).toBe(false)
      expect(value.valueOf()).toBe(0n) // When using maybe(), deleted boxes return 0

      // Verify that get() with default value works as expected
      expect(contract.boxInt.get({ default: Uint64(42) }).valueOf()).toBe(42n)
    })
  })

  describe('BoxMap Operations', () => {
    it('should set and get boxMap values', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = Uint64(1)
      const value = 'test value'

      contract.setBoxMap(key, value)
      expect(contract.getBoxMap(key)).toBe(value)
    })

    it('should return default value for non-existent boxMap key', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = Uint64(999)

      expect(contract.getBoxMapWithDefault(key)).toBe('default')
    })

    it('should delete boxMap value', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = Uint64(1)
      const value = 'test value'

      contract.setBoxMap(key, value)
      contract.deleteBoxMap(key)
      const [, exists] = contract.maybeBoxMap(key)
      expect(exists).toBe(false)
    })

    it('should check boxMap existence and length', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = Uint64(1)
      const value = 'test value'

      contract.setBoxMap(key, value)
      expect(contract.boxMapExists(key)).toBe(true)
      expect(contract.boxMapLength(key).valueOf()).toBeGreaterThan(0)
    })
  })

  describe('BoxMapStruct Operations', () => {
    it('should set and get boxMapStruct values', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = Uint64(1)
      const value = {
        name: 'testName',
        id: Uint64(70),
        asset: Uint64(1234),
      }

      expect(contract.setBoxMapObject(key, value)).toBe(true)
      const result = contract.getBoxMapObject(key)
      expect(result.name).toBe('testName')
      expect(result.id.valueOf()).toBe(70n)
      expect(result.asset.valueOf()).toBe(1234n)
    })

    it('should check boxMapObject length', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = Uint64(1)

      expect(contract.boxMapObjectLength(key)).toBe(28)
    })

    it('should check boxMapStruct existence', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = Uint64(1)
      const value = {
        name: 'testName',
        id: Uint64(70),
        asset: Uint64(1234),
      }

      contract.setBoxMapObject(key, value)
      expect(contract.boxMapObjectExists(key)).toBe(true)
    })
  })

  describe('BoxRef Operations', () => {
    it('should get and set boxRef values', () => {
      const contract = ctx.contract.create(BoxStorage)
      const result = contract.getBoxRef()
      expect(result.bytes).toEqual(ctx.defaultSender.bytes)
    })

    it('should set boxRef with custom key', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = 'customKey'

      contract.setBoxRef(key)
      const [, exists] = contract.maybeBoxRef(key)
      expect(exists).toBe(true)
    })

    it('should delete boxRef', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = 'customKey'

      contract.setBoxRef(key)
      contract.deleteBoxRef(key)
      const [, exists] = contract.maybeBoxRef(key)
      expect(exists).toBe(false)
    })

    it('should get boxRef length', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = 'customKey'

      expect(contract.lengthBoxRef(key).valueOf()).toBe(32)
    })

    it('should extract boxRef values', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = 'customKey'

      expect(() => contract.extractBoxRef(key)).not.toThrow()
    })
  })

  describe('Special Operations', () => {
    it('should create and manipulate arc4 static array box', () => {
      const contract = ctx.contract.create(BoxStorage)
      const key = 'staticArrayBox'

      const result = contract.arc4Box(key)
      expect(result[0].native.valueOf()).toBe(0n)
      expect(result[1].native.valueOf()).toBe(1n)
      expect(result[2].native.valueOf()).toBe(2n)
      expect(result[3].native.valueOf()).toBe(3n)
    })
  })
})
