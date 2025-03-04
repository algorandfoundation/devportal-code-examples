import {
  arc4,
  LocalState,
  assert,
  Account,
  Txn,
  contract,
  Bytes,
  Global,
} from '@algorandfoundation/algorand-typescript'
import type { uint64, bytes } from '@algorandfoundation/algorand-typescript'

/**
 * A contract demonstrating local storage functionality.
 * This contract shows how to use local state storage in an Algorand smart contract,
 * including initialization, reading, writing, and clearing of local state values.
 * Local state is per-account storage that requires accounts to opt-in before use.
 *
 * @stateTotals.localBytes - 4 bytes allocated for local byte storage
 * @stateTotals.localUints - 3 uints allocated for local integer storage
 */
@contract({ stateTotals: { localBytes: 4, localUints: 3 } })
export default class LocalStorage extends arc4.Contract {
  // example: INIT_LOCAL_STATE
  public localInt = LocalState<uint64>({ key: 'int' })
  public localIntNoDefault = LocalState<uint64>()
  public localBytes = LocalState<bytes>()
  public localString = LocalState<string>()
  public localBool = LocalState<boolean>()
  public localAccount = LocalState<Account>()
  // example: INIT_LOCAL_STATE

  // example: OPT_IN_TO_APPLICATION
  /**
   * Initializes local state values when an account opts into the application.
   * This method can only be called during an OptIn transaction.
   * Sets initial values for all local state variables:
   * - localInt: 100
   * - localIntNoDefault: 200
   * - localBytes: 'Silvio'
   * - localString: 'Micali'
   * - localBool: true
   * - localAccount: sender's address
   */
  @arc4.abimethod({ allowActions: 'OptIn' })
  public optInToApplication(): void {
    this.localInt(Txn.sender).value = 100
    this.localIntNoDefault(Txn.sender).value = 200
    this.localBytes(Txn.sender).value = Bytes('Silvio')
    this.localString(Txn.sender).value = 'Micali'
    this.localBool(Txn.sender).value = true
    this.localAccount(Txn.sender).value = Txn.sender
  }
  // example: OPT_IN_TO_APPLICATION

  // example: READ_LOCAL_STATE
  /**
   * Reads and returns all local state values for the transaction sender.
   * @returns A tuple containing:
   * - [0] uint64: The value of localInt
   * - [1] uint64: The value of localIntNoDefault
   * - [2] bytes: The value of localBytes
   * - [3] string: The value of localString
   * - [4] boolean: The value of localBool
   * - [5] Address: The value of localAccount converted to Address type
   */
  @arc4.abimethod()
  public readLocalState(): [uint64, uint64, bytes, string, boolean, arc4.Address] {
    const sender = Txn.sender
    // Convert Account reference type to native Address type for return value
    const accountAddress = new arc4.Address(this.localAccount(sender).value)

    return [
      this.localInt(sender).value,
      this.localIntNoDefault(sender).value,
      this.localBytes(sender).value,
      this.localString(sender).value,
      this.localBool(sender).value,
      accountAddress,
    ]
  }
  // example: READ_LOCAL_STATE

  // example: WRITE_LOCAL_STATE
  /**
   * Updates multiple local state values for the transaction sender.
   * Requires the account to be opted into the application.
   * @param valueString - New string value to store
   * @param valueBool - New boolean value to store
   * @param valueAccount - New account address to store
   */
  @arc4.abimethod()
  public writeLocalState(valueString: string, valueBool: boolean, valueAccount: Account): void {
    // Dynamic keys must be explicitly reserved in the contract's stateTotals configuration
    const sender = Txn.sender

    assert(sender.isOptedIn(Global.currentApplicationId), 'Account must opt in to contract first')

    this.localString(sender).value = valueString
    this.localBool(sender).value = valueBool
    this.localAccount(sender).value = valueAccount

    assert(this.localString(sender).value === valueString)
    assert(this.localBool(sender).value === valueBool)
    assert(this.localAccount(sender).value === valueAccount)
  }
  // example: WRITE_LOCAL_STATE

  // example: WRITE_DYNAMIC_LOCAL_STATE
  /**
   * Writes a value to local state using a dynamic key.
   * Demonstrates dynamic key-value storage in local state.
   * @param key - The dynamic key to store the value under
   * @param value - The string value to store
   * @returns The stored string value
   */
  @arc4.abimethod()
  public writeDynamicLocalState(key: string, value: string): string {
    const sender = Txn.sender

    assert(sender.isOptedIn(Global.currentApplicationId), 'Account must opt in to contract first')

    const localDynamicAccess = LocalState<string>({ key })

    localDynamicAccess(sender).value = value

    assert(localDynamicAccess(sender).value === value)

    return localDynamicAccess(sender).value
  }
  // example: WRITE_DYNAMIC_LOCAL_STATE

  // example: READ_DYNAMIC_LOCAL_STATE
  /**
   * Reads a value from local state using a dynamic key.
   * @param key - The dynamic key to read the value from
   * @returns The stored string value for the given key
   */
  @arc4.abimethod()
  public readDynamicLocalState(key: string): string {
    const sender = Txn.sender

    assert(sender.isOptedIn(Global.currentApplicationId), 'Account must opt in to contract first')

    const localDynamicAccess = LocalState<string>({ key })

    assert(localDynamicAccess(sender).hasValue, 'Key not found')

    return localDynamicAccess(sender).value
  }
  // example: READ_DYNAMIC_LOCAL_STATE

  // example: CLEAR_LOCAL_STATE
  /**
   * Clears all local state values for the transaction sender.
   * After calling this method, all local state values will be deleted.
   */
  @arc4.abimethod()
  public clearLocalState(): void {
    const sender = Txn.sender

    assert(sender.isOptedIn(Global.currentApplicationId), 'Account must opt in to contract first')

    this.localInt(sender).delete()
    this.localIntNoDefault(sender).delete()
    this.localBytes(sender).delete()
    this.localString(sender).delete()
    this.localBool(sender).delete()
    this.localAccount(sender).delete()
  }
  // example: CLEAR_LOCAL_STATE
}
