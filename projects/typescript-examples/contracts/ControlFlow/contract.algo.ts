import { arc4, Contract, assert, urange, Bytes, Uint64 } from '@algorandfoundation/algorand-typescript'
import type { uint64 } from '@algorandfoundation/algorand-typescript'

/**
 * ControlFlow Contract
 *
 * This contract demonstrates various control flow operations in Algorand smart contracts.
 * It shows how to use:
 * - If/else statements
 * - For loops
 * - Switch statements (equivalent to Python's match)
 * - While loops
 *
 * The contract implements the same functionality as its Python counterpart
 * in python-examples/smart_contracts/control_flow/contract.py
 */
export default class ControlFlow extends Contract {
  // example: IF_ELSE
  /**
   * Determines if an account is rich based on its balance
   * @param accountBalance The account balance to check
   * @returns A string describing the account's wealth status
   */
  @arc4.abimethod({ readonly: true })
  public isRich(accountBalance: uint64): string {
    if (accountBalance > 1000) {
      return 'This account is rich!'
    } else if (accountBalance > 100) {
      return 'This account is doing well.'
    } else {
      return 'This account is poor :('
    }
  }

  /**
   * Determines if a number is even or odd
   * @param number The number to check
   * @returns "Even" if the number is even, "Odd" otherwise
   */
  @arc4.abimethod({ readonly: true })
  public isEven(number: uint64): string {
    return number % 2 === 0 ? 'Even' : 'Odd'
  }
  // example: IF_ELSE

  // example: FOR_LOOP
  /**
   * Demonstrates different types of for loops
   * @returns An array of uint64 values in reversed order
   */
  @arc4.abimethod({ readonly: true })
  public forLoop(): uint64[] {
    // Create an array with values [0, 1, 2, 3]
    let numbers: uint64[] = []

    // Use for-of loop with urange to fill the array
    for (const item of urange(4)) {
      numbers = [...numbers, item]
    }

    // Create a reversed array [3, 2, 1, 0]
    let reversed: uint64[] = []

    // Reverse the array by prepending each element
    // This demonstrates another way to use for-of loops
    for (const num of numbers) {
      // Add each new element to the beginning of the array
      reversed = [num, ...reversed]
    }

    // Sum all values in the reversed array
    let sum: uint64 = 0
    for (const num of reversed) {
      sum += num
    }

    // The sum should be 0 + 1 + 2 + 3 = 6
    assert(sum === 6, 'Sum of reversed array should be 6')

    return reversed
  }

  // example: SWITCH_CASE
  /**
   * Returns the day of the week based on a numeric input
   * @param date A number from 0-6 representing a day of the week
   * @returns The name of the day, or "Invalid day" if out of range
   */
  @arc4.abimethod({ readonly: true })
  public getDay(date: uint64): string {
    switch (Uint64(date)) {
      case Uint64(1):
        return 'Monday'
      case Uint64(2):
        return 'Tuesday'
      case Uint64(3):
        return 'Wednesday'
      case Uint64(4):
        return 'Thursday'
      case Uint64(5):
        return 'Friday'
      case Uint64(6):
        return 'Saturday'
      case Uint64(7):
        return 'Sunday'
      default:
        return 'Invalid day'
    }
  }
  // example: SWITCH_CASE

  // example: SWITCH_BOX_STORAGE_COST
  /**
   * Calculates the minimum balance requirement (MBR) increase for box storage
   * based on different box size categories.
   *
   * @param boxSizeLabel The category of box size as a string label. Valid values:
   *                     'xs' (8B), 'sm' (64B), 'md' (256B), 'lg' (1KB), 'max' (32KB)
   * @param boxName The name of the box (used to calculate name length)
   * @returns The MBR increase in microAlgos, or 0 if invalid size label
   */
  @arc4.abimethod({ readonly: true })
  public calculateBoxStorageCost(boxSizeLabel: string, boxName: string): uint64 {
    // Base cost for any box
    const baseCost: uint64 = 2500 // microAlgos
    const byteUnitCost: uint64 = 400 // microAlgos per byte

    // Get the box name length in bytes
    const boxNameLength: uint64 = Bytes(boxName).length

    // Determine box size based on category label
    let boxSize: uint64

    switch (boxSizeLabel) {
      case 'xs':
        boxSize = 8 // 8 bytes (enough for a uint64)
        break

      case 'sm':
        boxSize = 64 // 64 bytes
        break

      case 'md':
        boxSize = 256 // 256 bytes
        break

      case 'lg':
        boxSize = 1024 // 1KB
        break

      case 'max':
        boxSize = 32000 // 32KB (close to max allowed)
        break

      default:
        // Invalid value
        return 0
    }

    // Calculate MBR increase using the formula:
    // MBR Increase = 2500 + 400 × (box name length + box size)
    const mbrIncrease: uint64 = baseCost + byteUnitCost * (boxNameLength + boxSize)

    return mbrIncrease
  }
  // example: SWITCH_BOX_STORAGE_COST

  // example: WHILE_LOOP
  /**
   * Demonstrates while loop with continue and break statements
   * @returns The number of iterations performed
   */
  @arc4.abimethod({ readonly: true })
  public loop(): uint64 {
    let num: uint64 = 10
    let loopCount: uint64 = 0

    while (num > 0) {
      if (num > 5) {
        num -= 1
        loopCount += 1
        continue
      }

      num -= 2
      loopCount += 1

      if (num === 1) {
        break
      }
    }

    return loopCount
  }
  // example: WHILE_LOOP
}
