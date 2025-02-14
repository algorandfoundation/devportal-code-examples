import { arc4, Uint64, Bytes, GlobalState, assert } from '@algorandfoundation/algorand-typescript'
import type { uint64, bytes, Asset, Application, Account } from '@algorandfoundation/algorand-typescript'

/**
 * A contract demonstrating global storage functionality
 */
export default class GlobalStorage extends arc4.Contract {
  // example: INIT_GLOBAL_STORAGE
  globalInt = GlobalState({ initialValue: Uint64(50) }) // UInt64 with default value
  globalIntNoDefault = GlobalState<uint64>() // UInt64 with no default value
  // example: INIT_GLOBAL_STORAGE

  // example: INIT_BYTES
  globalBytes = GlobalState({ initialValue: Bytes('Hello') }) // Bytes with default value
  globalBytesNoDefault = GlobalState<bytes>() // Bytes with no default value
  // example: INIT_BYTES

  // example: INIT_BOOL
  globalBool = GlobalState({ initialValue: true }) // Bool with default value
  globalBoolNoDefault = GlobalState<boolean>() // Bool with no default value
  // example: INIT_BOOL

  // example: INIT_ASSET
  globalAsset = GlobalState<Asset>() // Asset
  // example: INIT_ASSET

  // example: INIT_APPLICATION
  globalApplication = GlobalState<Application>() // Application
  // example: INIT_APPLICATION

  // example: INIT_ACCOUNT
  globalAccount = GlobalState<Account>() // Account
  // example: INIT_ACCOUNT

  // example: READ_GLOBAL_STATE
  @arc4.abimethod({ readonly: true })
  public getGlobalState(): uint64 {
    return this.globalInt.value
  }
  // example: READ_GLOBAL_STATE

  @arc4.abimethod({ readonly: true })
  public hasGlobalState(): [uint64, boolean] {
    const value = this.globalInt.value
    const hasValue = this.globalInt.hasValue

    if (!hasValue) {
      return [value, hasValue]
    }

    return [value, hasValue]
  }

  @arc4.abimethod({ readonly: true })
  public getGlobalStateExample(): {
    globalInt: uint64
    globalIntNoDefault: uint64
    globalBytes: bytes
  } {
    assert(this.globalInt.value === Uint64(50))
    assert(this.globalIntNoDefault.value === Uint64(0))
    assert(this.globalBytes.value === Bytes('Hello'))

    const globalInt = this.globalInt.value
    const globalIntNoDefault = this.globalIntNoDefault.value
    const globalBytes = this.globalBytes.value

    return { globalInt, globalIntNoDefault, globalBytes }
  }

  // example: WRITE_GLOBAL_STATE
  @arc4.abimethod()
  setGlobalState(value: bytes): void {
    this.globalBytes.value = value
  }
  // example: WRITE_GLOBAL_STATE

  // example: WRITE_GLOBAL_STATE_EXAMPLES
  @arc4.abimethod()
  public setGlobalStateExample(valueBytes: bytes, valueAsset: Asset, valueBool: boolean): void {
    this.globalBytesNoDefault.value = valueBytes
    assert(this.globalBytesNoDefault.value === valueBytes)

    this.globalBoolNoDefault.value = valueBool
    assert(this.globalBoolNoDefault.value)

    this.globalAsset.value = valueAsset
    assert(this.globalAsset.value === valueAsset)
  }
  // example: WRITE_GLOBAL_STATE_EXAMPLES

  // example: DELETE_GLOBAL_STATE
  @arc4.abimethod()
  delGlobalState(): boolean {
    // delete this.globalIntNoDefault.value
    return true
  }
  // example: DELETE_GLOBAL_STATE
}
