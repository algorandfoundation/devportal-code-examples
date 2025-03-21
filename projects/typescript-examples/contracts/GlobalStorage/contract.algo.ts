import {
  arc4,
  Uint64,
  GlobalState,
  assert,
  Account,
  Txn,
  Bytes,
  Contract,
  contract,
} from '@algorandfoundation/algorand-typescript'
import type { uint64, bytes } from '@algorandfoundation/algorand-typescript'

/**
 * A contract demonstrating global storage functionality
 */
@contract({ stateTotals: { globalBytes: 4, globalUints: 3 } })
export default class GlobalStorage extends Contract {
  // example: INIT_GLOBAL_STORAGE
  public globalInt = GlobalState<uint64>({ initialValue: Uint64(50) }) // UInt64 with default value
  public globalIntNoDefault = GlobalState<uint64>() // UInt64 with no default value
  public globalBytes = GlobalState<bytes>({ initialValue: Bytes('Silvio') }) // Bytes with default value
  public globalString = GlobalState<string>({ initialValue: 'Micali' }) // Bytes with default value
  public globalBool = GlobalState({ initialValue: true }) // Bool with default value
  public globalAccount = GlobalState<Account>() // Address with no default value
  // example: INIT_GLOBAL_STORAGE

  // example: INIT_GLOBAL_STORAGE_IN_CONSTRUCTOR
  public constructor() {
    // Global state without default values can have values set in the constructor
    // Otherwise, the values will not be initialized until the first write
    super()
    this.globalIntNoDefault.value = Uint64(0)
    this.globalAccount.value = Txn.sender
  }
  // example: INIT_GLOBAL_IN_CONSTRUCTOR

  // example: READ_GLOBAL_STATE
  /**
   * Reads and returns all global state values from the contract
   * @returns A tuple containing [globalInt, globalIntNoDefault, globalBytes, globalString, globalBool, globalAccount]
   * where each value corresponds to the current state of the respective global variable
   */
  public readGlobalState(): [uint64, uint64, bytes, string, boolean, arc4.Address] {
    // Convert Account reference type to native Address type for return value
    const accountAddress = new arc4.Address(this.globalAccount.value)

    return [
      this.globalInt.value,
      this.globalIntNoDefault.value,
      this.globalBytes.value,
      this.globalString.value,
      this.globalBool.value,
      accountAddress,
    ]
  }
  // example: READ_GLOBAL_STATE

  // example: HAS_GLOBAL_STATE
  /**
   * Checks if a global state value exists and returns it
   * @returns A tuple containing [value, hasValue] where value is the current globalIntNoDefault value
   * and hasValue indicates if the value has been initialized
   */
  public hasGlobalState(): [uint64, boolean] {
    const hasValue = this.globalIntNoDefault.hasValue
    const value = this.globalIntNoDefault.value

    assert(hasValue, 'Global state not set.')

    return [value, hasValue]
  }
  // example: HAS_GLOBAL_STATE

  // example: WRITE_GLOBAL_STATE
  /**
   * Updates multiple global state values
   * @param valueBytes New value for globalBytes
   * @param valueBool New value for globalBool
   * @param valueAccount New value for globalAccount
   */
  public writeGlobalState(valueString: string, valueBool: boolean, valueAccount: Account): void {
    this.globalString.value = valueString
    this.globalBool.value = valueBool
    this.globalAccount.value = valueAccount

    assert(this.globalString.value === valueString)
    assert(this.globalBool.value === valueBool)
    assert(this.globalAccount.value === valueAccount)
  }
  // example: WRITE_GLOBAL_STATE

  /**
   * Writes a value to global state using a dynamic key and returns the stored value
   * @param key The key to store the value under in global state
   * @param value The string value to store in global state
   * @returns The stored string value, confirming successful storage
   */
  public writeDynamicGlobalState(key: string, value: string): string {
    // Dynamic keys must be explicitly reserved in the contract's stateTotals configuration
    const globalDynamicAccess = GlobalState<string>({ key })
    globalDynamicAccess.value = value

    assert(globalDynamicAccess.value === value)

    return globalDynamicAccess.value
  }

  // example: DELETE_GLOBAL_STATE
  @arc4.abimethod()
  public deleteGlobalState(): boolean {
    this.globalInt.delete()
    return true
  }
  // example: DELETE_GLOBAL_STATE
}
