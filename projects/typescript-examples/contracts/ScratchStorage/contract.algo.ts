// example: SCRATCH_STORAGE
import {
  abimethod,
  uint64,
  Uint64,
  bytes,
  Bytes,
  assert,
  Contract,
  contract,
} from '@algorandfoundation/algorand-typescript'
import { Scratch, gloadBytes, gloadUint64 } from '@algorandfoundation/algorand-typescript/op'

/**
 * ScratchStorage Contract
 *
 * This contract demonstrates how to use scratch storage in Algorand smart contracts.
 * Scratch storage persists for the lifetime of a group transaction and can be used to pass
 * values between multiple calls and/or applications in the same group.
 *
 * Key features demonstrated:
 * - Reserving scratch slots using the contract decorator
 * - Storing and loading values from scratch space
 * - Using scratch space to pass values between transactions in a group
 * - Different data types in scratch space (uint64 and bytes)
 */
@contract({ scratchSlots: [0, 1, 2, { from: 10, to: 20 }] }) // This reserves slots 0, 1, 2 and slots 10-20
export default class ScratchStorage extends Contract {
  /**
   * Stores values in scratch space
   * This method demonstrates how to store different types of values in scratch slots
   */
  private setScratchValues(): void {
    Scratch.store(0, Uint64(42))
    Scratch.store(1, Bytes('Hello, Algorand!'))
    Scratch.store(2, Uint64(100))
    Scratch.store(15, Uint64(999))
  }

  /**
   * Reads values from scratch space
   * This method demonstrates how to read different types of values from scratch slots
   */
  private readScratchValues(): void {
    // Read uint64 values from scratch slots
    const value1 = Scratch.loadUint64(0)
    const value2 = Scratch.loadUint64(2)
    const value3 = Scratch.loadUint64(15)
    const bytesValue = Scratch.loadBytes(1)

    assert(value1 === 42, 'Value in slot 0 should be 42')
    assert(bytesValue === Bytes('Hello, Algorand!'), 'Value in slot 1 should be "Hello, Algorand!"')
    assert(value2 === 100, 'Value in slot 2 should be 100')
    assert(value3 === 999, 'Value in slot 15 should be 999')
  }

  /**
   * Demonstrates basic scratch storage operations
   * @returns true if all operations succeed
   */
  public demonstrateScratchStorage(): boolean {
    this.setScratchValues()
    this.readScratchValues()

    return true
  }

  /**
   * Demonstrates reading values from another transaction in the same group
   * @param groupIndex The index of the transaction in the group to read from
   * @param scratchSlot The scratch slot to read from
   * @returns The uint64 value read from the specified transaction's scratch slot
   */
  @abimethod({ readonly: true })
  public readFromGroupTransaction(groupIndex: uint64, scratchSlot: uint64): uint64 {
    return gloadUint64(groupIndex, scratchSlot)
  }

  /**
   * Demonstrates reading bytes values from another transaction in the same group
   * @param groupIndex The index of the transaction in the group to read from
   * @param scratchSlot The scratch slot to read from
   * @returns The bytes value read from the specified transaction's scratch slot
   */
  @abimethod({ readonly: true })
  public readBytesFromGroupTransaction(groupIndex: uint64, scratchSlot: uint64): bytes {
    return gloadBytes(groupIndex, scratchSlot)
  }
}
// example: SCRATCH_STORAGE
