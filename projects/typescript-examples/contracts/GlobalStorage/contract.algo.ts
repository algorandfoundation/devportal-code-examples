import { arc4, Uint64, Bytes, GlobalState, assert, contract } from '@algorandfoundation/algorand-typescript'
import type { uint64, bytes, Asset, Application, Account } from '@algorandfoundation/algorand-typescript'

/**
 * A contract demonstrating global storage functionality
 */
@contract({ scratchSlots: [50] })
export default class GlobalStorage extends arc4.Contract {
  // example: INIT_GLOBAL_STORAGE
  public globalInt = GlobalState<uint64>({ initialValue: Uint64(50) }) // UInt64 with default value
  public globalIntNoDefault = GlobalState<uint64>() // UInt64 with no default value
  // example: INIT_GLOBAL_STORAGE

  // example: INIT_BYTES
  public globalBytes = GlobalState({ initialValue: Bytes('Hello') }) // Bytes with default value
  public globalBytesNoDefault = GlobalState<bytes>() // Bytes with no default value
  // example: INIT_BYTES

  // example: INIT_BOOL
  public globalBool = GlobalState({ initialValue: true }) // Bool with default value
  public globalBoolNoDefault = GlobalState<boolean>() // Bool with no default value
  // example: INIT_BOOL

  // example: INIT_ASSET
  public globalAsset = GlobalState<Asset>() // Asset
  // example: INIT_ASSET

  // example: INIT_APPLICATION
  public globalApplication = GlobalState<Application>() // Application
  // example: INIT_APPLICATION

  // example: INIT_ACCOUNT
  public globalAccount = GlobalState<Account>() // Account
  // example: INIT_ACCOUNT

  // example: READ_GLOBAL_STATE
  @arc4.abimethod({ readonly: true })
  public getGlobalState(): [uint64, bytes] {
    return [this.globalInt.value, this.globalBytes.value]
  }
  // example: READ_GLOBAL_STATE

  @arc4.abimethod({ readonly: true })
  public hasGlobalState(): [uint64, boolean] {
    const hasValue = this.globalInt.hasValue
    const value = this.globalInt.value

    return [value, hasValue]
  }

  // example: WRITE_GLOBAL_STATE
  @arc4.abimethod()
  public setGlobalState(value: bytes): void {
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
  // @arc4.abimethod()
  // public deleteGlobalState(): boolean {
  //   this.globalInt.delete() // @TODO: Not implemented
  //   return true
  // }
  // example: DELETE_GLOBAL_STATE
}
