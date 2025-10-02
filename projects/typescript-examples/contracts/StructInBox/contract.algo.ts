import { Contract, uint64, BoxMap, clone, assertMatch } from '@algorandfoundation/algorand-typescript'

// example: EXAMPLE_STRUCT_IN_BOX
type User = {
  id: uint64
  name: string
  age: uint64
}

export default class StructInBoxMap extends Contract {
  public users = BoxMap<uint64, User>({ keyPrefix: 'users' })

  public createNewUser(id: uint64, user: User): boolean {
    this.users(id).value = clone(user)

    assertMatch(this.users(id).value, {
      name: user.name,
      age: user.age,
    })

    return true
  }

  public getUser(id: uint64): User {
    return this.users(id).value
  }

  public checkUserExists(id: uint64): boolean {
    return this.users(id).exists
  }

  public updateUserNameAndAge(id: uint64, name: string, age: uint64): boolean {
    this.users(id).value.name = name
    this.users(id).value.age = age

    assertMatch(this.users(id).value, {
      name,
      age,
    })

    return true
  }
}
// example: EXAMPLE_STRUCT_IN_BOX
