import { Contract, Uint64, GlobalState, abimethod } from '@algorandfoundation/algorand-typescript'
import type { uint64 } from '@algorandfoundation/algorand-typescript'

export default class CustomCreate extends Contract {
  public age = GlobalState<uint64>() // UInt64 with no default value

  @abimethod({ onCreate: 'require' })
  public custom_create(age: uint64): void {
    this.age.value = Uint64(age)
  }

  public getAge(): uint64 {
    return this.age.value
  }
}
