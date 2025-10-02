// example: REFERENCE_APP_BOX_EXAMPLE
import {
  Contract,
  readonly,
  Account,
  BoxMap,
  Txn,
  Global,
  gtxn,
  assert,
  Uint64,
  GlobalState,
  contract,
} from '@algorandfoundation/algorand-typescript'
import type { uint64 } from '@algorandfoundation/algorand-typescript'

/**
 * A contract that uses box storage to maintain a counter for each account
 * Each account needs to pay for the Minimum Balance Requirement (MBR) for their box
 * Constants for box storage are stored in global state
 */
@contract({ stateTotals: { globalUints: 4 } })
export default class ReferenceAppBox extends Contract {
  // Define constants for box storage in global state
  public keyLength = GlobalState<uint64>({ initialValue: Uint64(32 + 19) }) // Account address (32 bytes) + key prefix overhead (19 bytes)
  public valueLength = GlobalState<uint64>({ initialValue: Uint64(8) }) // uint64 (8 bytes)
  public boxSize = GlobalState<uint64>() // Calculated in constructor
  public boxMbr = GlobalState<uint64>() // Calculated in constructor

  // Create a box map to store counter values per account
  public accountBoxCounter = BoxMap<Account, uint64>({ keyPrefix: 'counter' })

  /**
   * Initialize calculated values in constructor
   */
  public constructor() {
    super()
    // Calculate the total box size and MBR in constructor
    this.boxSize.value = this.keyLength.value + this.valueLength.value
    this.boxMbr.value = Uint64(2500) + this.boxSize.value * Uint64(400) // Base MBR + (size * per-byte cost)
  }

  /**
   * Increments the counter for the transaction sender
   * Requires a payment transaction to cover the MBR for the box
   * @param payMbr Payment transaction covering the box MBR
   * @returns The new counter value
   */
  @readonly
  public incrementBoxCounter(payMbr: gtxn.PaymentTxn): uint64 {
    // Verify the payment covers the MBR cost and is sent to the contract
    assert(payMbr.amount === this.boxMbr.value, 'Payment must cover the box MBR')
    assert(payMbr.receiver === Global.currentApplicationAddress, 'Payment must be to the contract')

    const [counter, hasCounter] = this.accountBoxCounter(Txn.sender).maybe()

    if (hasCounter) {
      // Increment existing counter
      this.accountBoxCounter(Txn.sender).value = counter + 1
      return counter + 1
    } else {
      // Initialize new counter to 1
      this.accountBoxCounter(Txn.sender).value = Uint64(1)
      return Uint64(1)
    }
  }

  /**
   * Gets the current counter value for the transaction sender
   * @returns The current counter value or 0 if not set
   */
  @readonly
  public getBoxCounter(): uint64 {
    const [counter, hasCounter] = this.accountBoxCounter(Txn.sender).maybe()

    if (hasCounter) {
      return counter
    }

    return 0
  }

  /**
   * Gets the current counter value for any account
   * @param account The account to check
   * @returns The current counter value or 0 if not set
   */
  @readonly
  public getBoxCounterForAccount(account: Account): uint64 {
    const [counter, hasCounter] = this.accountBoxCounter(account).maybe()

    if (hasCounter) {
      return counter
    }

    return 0
  }

  /**
   * Returns the MBR cost for creating a box
   * @returns The MBR cost in microAlgos
   */
  @readonly
  public getBoxMbr(): uint64 {
    return this.boxMbr.value
  }

  /**
   * Returns all the box size configuration values
   * @returns A tuple containing [keyLength, valueLength, boxSize, boxMbr]
   */
  @readonly
  public getBoxConfiguration(): [uint64, uint64, uint64, uint64] {
    return [this.keyLength.value, this.valueLength.value, this.boxSize.value, this.boxMbr.value]
  }

  /**
   * Updates the box size configuration values
   * @param newKeyLength The new key length
   * @param newValueLength The new value length
   */
  @readonly
  public updateBoxConfiguration(newKeyLength: uint64, newValueLength: uint64): void {
    this.keyLength.value = newKeyLength
    this.valueLength.value = newValueLength

    // Recalculate derived values
    this.boxSize.value = this.keyLength.value + this.valueLength.value
    this.boxMbr.value = Uint64(2500) + this.boxSize.value * Uint64(400)
  }
}
// example: REFERENCE_APP_BOX_EXAMPLE
