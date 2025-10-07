import { Uint64 } from '@algorandfoundation/algorand-typescript'
import { TestExecutionContext } from '@algorandfoundation/algorand-typescript-testing'
import { describe, expect, it } from 'vitest'
import StructInBoxMap from './contract.algo'

describe('StructInBoxMap contract', () => {
  const ctx = new TestExecutionContext()

  describe('User Management Operations', () => {
    it('should create a new user successfully', () => {
      const contract = ctx.contract.create(StructInBoxMap)
      const testUser = {
        id: Uint64(1),
        name: 'TestUser',
        age: Uint64(25),
      }

      const result = contract.createNewUser(testUser.id, testUser)
      expect(result).toBe(true)
    })

    it('should get user details correctly', () => {
      const contract = ctx.contract.create(StructInBoxMap)
      const testUser = {
        id: Uint64(1),
        name: 'TestUser',
        age: Uint64(25),
      }

      contract.createNewUser(testUser.id, testUser)
      const retrievedUser = contract.getUser(testUser.id)

      expect(retrievedUser.id.valueOf()).toBe(testUser.id.valueOf())
      expect(retrievedUser.name).toBe(testUser.name)
      expect(retrievedUser.age.valueOf()).toBe(testUser.age.valueOf())
    })

    it('should check user existence correctly', () => {
      const contract = ctx.contract.create(StructInBoxMap)
      const testUser = {
        id: Uint64(1),
        name: 'TestUser',
        age: Uint64(25),
      }

      expect(contract.checkUserExists(testUser.id)).toBe(false)

      contract.createNewUser(testUser.id, testUser)
      expect(contract.checkUserExists(testUser.id)).toBe(true)
    })

    it('should update user name and age successfully', () => {
      const contract = ctx.contract.create(StructInBoxMap)
      const testUser = {
        id: Uint64(1),
        name: 'TestUser',
        age: Uint64(25),
      }

      // Create user first
      contract.createNewUser(testUser.id, testUser)

      // Update user details
      const newName = 'UpdatedUser'
      const newAge = Uint64(30)
      const updateResult = contract.updateUserNameAndAge(testUser.id, newName, newAge)

      expect(updateResult).toBe(true)

      // Verify the update
      const updatedUser = contract.getUser(testUser.id)
      expect(updatedUser.name).toBe(newName)
      expect(updatedUser.age.valueOf()).toBe(newAge.valueOf())
      expect(updatedUser.id.valueOf()).toBe(testUser.id.valueOf()) // ID should remain unchanged
    })

    it('should handle multiple users independently', () => {
      const contract = ctx.contract.create(StructInBoxMap)

      const user1 = {
        id: Uint64(1),
        name: 'UserOne',
        age: Uint64(25),
      }

      const user2 = {
        id: Uint64(2),
        name: 'UserTwo',
        age: Uint64(30),
      }

      // Create both users
      contract.createNewUser(user1.id, user1)
      contract.createNewUser(user2.id, user2)

      // Verify both users exist
      expect(contract.checkUserExists(user1.id)).toBe(true)
      expect(contract.checkUserExists(user2.id)).toBe(true)

      // Retrieve and verify both users
      const retrievedUser1 = contract.getUser(user1.id)
      const retrievedUser2 = contract.getUser(user2.id)

      expect(retrievedUser1.name).toBe('UserOne')
      expect(retrievedUser1.age.valueOf()).toBe(25n)
      expect(retrievedUser2.name).toBe('UserTwo')
      expect(retrievedUser2.age.valueOf()).toBe(30n)

      // Update one user and verify the other remains unchanged
      contract.updateUserNameAndAge(user1.id, 'UpdatedUserOne', Uint64(26))

      const updatedUser1 = contract.getUser(user1.id)
      const unchangedUser2 = contract.getUser(user2.id)

      expect(updatedUser1.name).toBe('UpdatedUserOne')
      expect(updatedUser1.age.valueOf()).toBe(26n)
      expect(unchangedUser2.name).toBe('UserTwo')
      expect(unchangedUser2.age.valueOf()).toBe(30n)
    })

    it('should handle edge cases with zero and maximum values', () => {
      const contract = ctx.contract.create(StructInBoxMap)

      const userWithZeroAge = {
        id: Uint64(0),
        name: 'ZeroAgeUser',
        age: Uint64(0),
      }

      const userWithMaxValues = {
        id: Uint64(18446744073709551615n), // Max uint64
        name: 'MaxValueUser',
        age: Uint64(18446744073709551615n),
      }

      // Create users with edge case values
      expect(contract.createNewUser(userWithZeroAge.id, userWithZeroAge)).toBe(true)
      expect(contract.createNewUser(userWithMaxValues.id, userWithMaxValues)).toBe(true)

      // Verify both users exist and have correct values
      expect(contract.checkUserExists(userWithZeroAge.id)).toBe(true)
      expect(contract.checkUserExists(userWithMaxValues.id)).toBe(true)

      const retrievedZeroAge = contract.getUser(userWithZeroAge.id)
      const retrievedMaxValues = contract.getUser(userWithMaxValues.id)

      expect(retrievedZeroAge.age.valueOf()).toBe(0n)
      expect(retrievedMaxValues.age.valueOf()).toBe(18446744073709551615n)
    })
  })
})
