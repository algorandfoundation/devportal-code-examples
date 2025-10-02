// example: REFERENCE_ACCOUNT_APP_EXAMPLE
import {
  Contract,
  op,
  abimethod,
  Account,
  Application,
  LocalState,
  Txn,
  Global,
  assert,
  Bytes,
} from '@algorandfoundation/algorand-typescript'
import type { uint64 } from '@algorandfoundation/algorand-typescript'
import { Address, readonly } from '@algorandfoundation/algorand-typescript/arc4'

/**
 * A contract that maintains a per-account counter in local state
 * Accounts must opt in to use the counter
 */
export class MyCounter extends Contract {
  // Define a local state variable for the counter
  public myCounter = LocalState<uint64>({ key: 'my_counter' })

  /**
   * Initialize the counter when an account opts in
   */
  @abimethod({ allowActions: 'OptIn' })
  public optIn(): void {
    this.myCounter(Txn.sender).value = 0
  }

  /**
   * Increment the counter for the sender and return its new value
   * @returns The new counter value
   */
  public incrementMyCounter(): uint64 {
    assert(Txn.sender.isOptedIn(Global.currentApplicationId), 'Account must opt in to contract first')

    this.myCounter(Txn.sender).value = this.myCounter(Txn.sender).value + 1

    return this.myCounter(Txn.sender).value
  }
}

/**
 * A contract that demonstrates how to reference accounts and applications
 * to access local state from external contracts
 */
export default class ReferenceAccountApp extends Contract {
  /**
   * Get the counter value from another account's local state with hardcoded values
   * @returns The counter value or 0 if it doesn't exist
   */
  @readonly
  public getMyCounter(): uint64 {
    const address = new Address('WMHF4FLJNKY2BPFK7YPV5ID6OZ7LVDB2B66ZTXEAMLL2NX4WJZRJFVX66M')
    const addressBytes = address.bytes
    const account = Account(addressBytes)
    const app = Application(1717) // Replace with your application id

    // Check if the counter value exists in the account's local state for the specified app
    const [value, hasValue] = op.AppLocal.getExUint64(account, app, Bytes('my_counter'))

    if (!hasValue) {
      return 0
    }

    return value
  }

  /**
   * Get the counter value from another account's local state with provided parameters
   * @param account The account to check
   * @param app The application to query
   * @returns The counter value or 0 if it doesn't exist
   */
  @readonly
  public getMyCounterWithArg(account: Account, app: Application): uint64 {
    // Check if the counter value exists in the account's local state for the specified app
    const [value, hasValue] = op.AppLocal.getExUint64(account, app, Bytes('my_counter'))

    if (!hasValue) {
      return 0
    }

    return value
  }
}
// example: REFERENCE_ACCOUNT_APP_EXAMPLE
