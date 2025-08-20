import {
  abimethod,
  Contract,
  uint64,
  Uint64,
  BoxMap,
  clone,
  assertMatch,
} from '@algorandfoundation/algorand-typescript'

// example: EXAMPLE_STRUCT_IN_BOX
type User = {
  name: string
  id: uint64
  asset: uint64
}

export default class StructInBoxMap extends Contract {
  public userMap = BoxMap<uint64, User>({ keyPrefix: 'users' })

  @abimethod()
  public boxMapTest(): boolean {
    const key0 = Uint64(0)
    const value = {
      name: 'testName',
      id: Uint64(70),
      asset: Uint64(2),
    } satisfies User

    this.userMap(key0).value = clone(value)

    return true
  }

  @abimethod()
  public boxMapSet(key: uint64, value: User): boolean {
    this.userMap(key).value = clone(value)

    assertMatch(this.userMap(key).value, {
      id: value.id,
      asset: value.asset,
      name: value.name,
    })

    return true
  }

  @abimethod()
  public boxMapGet(key: uint64): User {
    return this.userMap(key).value
  }

  @abimethod()
  public boxMapExists(key: uint64): boolean {
    return this.userMap(key).exists
  }
}
// example: EXAMPLE_STRUCT_IN_BOX
