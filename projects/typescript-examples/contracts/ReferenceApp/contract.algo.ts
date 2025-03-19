import {
  Contract,
  abimethod,
  Application,
  GlobalState,
  Uint64,
  itxn,
  arc4,
} from '@algorandfoundation/algorand-typescript'
import type { uint64 } from '@algorandfoundation/algorand-typescript'

/**
 * A contract that increments a counter
 */
export class Counter extends Contract {
  public counter = GlobalState<uint64>({ initialValue: Uint64(0) })

  /**
   * Increments the counter and returns the new value
   * @returns The new counter value
   */
  @abimethod()
  public increment(): uint64 {
    this.counter.value = this.counter.value + 1
    return this.counter.value
  }
}

/**
 * A contract that demonstrates how to use resource usage in a contract using an asset reference
 */
export default class ReferenceApp extends Contract {
  /**
   * Calls the increment method on another Counter app with a hardcoded app ID
   * @returns The incremented counter value from the inner call
   */
  @abimethod()
  public incrementViaInner(): uint64 {
    const app = Application(1717) // Replace with your application id

    // Call the increment method on the Counter application
    const appCallTxn = itxn
      .applicationCall({
        appId: app.id,
        // Use methodSelector to get the ABI selector for the increment method
        appArgs: [arc4.methodSelector('increment()uint64')],
        fee: 0,
      })
      .submit()

    // Decode the ABI return value from the transaction logs
    // The ABI return value is in the last log with a prefix for the ABI return format
    return arc4.decodeArc4<uint64>(appCallTxn.lastLog, 'log')
  }

  /**
   * Calls the increment method on another Counter app passed as an argument
   * @param app The application to call
   * @returns The incremented counter value from the inner call
   */
  @abimethod()
  public incrementViaInnerWithArg(app: Application): uint64 {
    // Call the increment method on the provided Counter application
    const appCallTxn = itxn
      .applicationCall({
        appId: app.id,
        // Use methodSelector to get the ABI selector for the increment method
        appArgs: [arc4.methodSelector('increment()uint64')],
        fee: 0,
      })
      .submit()

    // Decode the ABI return value from the transaction logs
    // The ABI return value is in the last log with a prefix for the ABI return format
    return arc4.decodeArc4<uint64>(appCallTxn.lastLog, 'log')
  }
}
