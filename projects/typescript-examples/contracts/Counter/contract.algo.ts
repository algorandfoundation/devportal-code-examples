import { Contract, GlobalState, Uint64 } from '@algorandfoundation/algorand-typescript'
import type { uint64 } from '@algorandfoundation/algorand-typescript'

/**
 * A contract that increments a counter
 */
export default class Counter extends Contract {
  public counter = GlobalState<uint64>({ initialValue: Uint64(0) })

  /**
   * Increments the counter and returns the new value
   * @returns The new counter value
   */
  public increment(): uint64 {
    this.counter.value = this.counter.value + 1
    return this.counter.value
  }
}
