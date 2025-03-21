import {
  Box,
  arc4,
  abimethod,
  Contract,
  bytes,
  Bytes,
  uint64,
  Uint64,
  BoxMap,
  BoxRef,
  Global,
  Txn,
} from '@algorandfoundation/algorand-typescript'
import { assert, assertMatch } from '@algorandfoundation/algorand-typescript'

type StaticInts = arc4.StaticArray<arc4.UintN8, 4>

class UserStruct extends arc4.Struct<{
  name: arc4.Str
  id: arc4.UintN64
  asset: arc4.UintN64
}> {}

/**
 * BoxStorage Contract
 *
 * This contract demonstrates various box storage operations in Algorand smart contracts.
 * It shows how to:
 * - Create and manage different types of boxes (int, bytes, dynamic bytes, string)
 * - Use BoxMap for key-value storage
 * - Work with BoxRef for direct box manipulation
 * - Perform operations like get, set, delete, and length calculations
 * - Handle complex data structures in boxes
 *
 * The contract implements the same functionality as its Python counterpart
 * in python-examples/smart_contracts/box_storage/contract.py
 */
export default class BoxStorage extends Contract {
  // example: INIT_BOX_STORAGE
  public boxString = Box<string>({ key: 'boxString' })
  public boxInt = Box<uint64>({ key: 'boxInt' })
  public boxBytes = Box<bytes>({ key: 'boxBytes' })
  public boxDynamicBytes = Box<arc4.DynamicBytes>({ key: 'boxDynamicBytes' })
  public boxRef = BoxRef({ key: 'boxRef' })
  public boxMap = BoxMap<uint64, string>({ keyPrefix: 'boxMap' })
  public boxMapStruct = BoxMap<uint64, UserStruct>({ keyPrefix: 'users' })
  // example: INIT_BOX_STORAGE

  // example: GET_BOX_STORAGE
  /**
   * Retrieves the value stored in the boxInt box
   * @returns The uint64 value stored in boxInt
   */
  @abimethod({ readonly: true })
  public getBox(): uint64 {
    return this.boxInt.value
  }

  /**
   * Retrieves the value of the boxInt box
   */
  @abimethod({ readonly: true })
  public valueBox(): uint64 {
    return this.boxInt.value
  }

  /**
   * Retrieves the value stored in the boxInt box and checks if it exists
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @abimethod({ readonly: true })
  public maybeBox(): [uint64, boolean] {
    const [boxIntValue, boxIntExists] = this.boxInt.maybe()
    return [boxIntValue, boxIntExists]
  }

  /**
   * Retrieves the value stored in the boxMap box
   * @param key The key of the boxMap to retrieve the value from
   * @returns The value stored in the boxMap box
   */
  @abimethod({ readonly: true })
  public getBoxMap(key: uint64): string {
    return this.boxMap(key).value
  }

  /**
   * Retrieves the value stored in the boxMap box with a default value if the key does not exist
   * @param key The key of the boxMap to retrieve the value from
   * @returns The value stored in the boxMap box
   */
  @abimethod({ readonly: true })
  public getBoxMapWithDefault(key: uint64): string {
    return this.boxMap(key).get({ default: 'default' })
  }

  /**
   * Retrieves the value stored in the boxMap box and checks if it exists
   * @param key The key to check in the boxMap
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @abimethod({ readonly: true })
  public maybeBoxMap(key: uint64): [string, boolean] {
    const [value, exists] = this.boxMap(key).maybe()
    return [exists ? value : '', exists]
  }

  /**
   * Retrieves the key prefix of the boxMap box
   * @returns The key prefix of the boxMap box
   */
  @abimethod({ readonly: true })
  public keyPrefixBoxMap(): bytes {
    return this.boxMap.keyPrefix
  }

  /**
   * Retrieves the value stored in the boxRef box
   * @returns The value stored in the boxRef box
   */
  public getBoxRef(): arc4.Address {
    this.boxRef.create({ size: 32 })
    const senderBytes = Txn.sender.bytes
    this.boxRef.put(senderBytes)
    const value = this.boxRef.get({ default: senderBytes })
    assert(value === senderBytes, 'boxRef value mismatch')
    return new arc4.Address(value)
  }

  /**
   * Checks if the boxMap box exists
   * @param key The key to check for
   * @returns true if the box exists, false otherwise
   */
  @abimethod({ readonly: true })
  public boxMapExists(key: uint64): boolean {
    return this.boxMap(key).exists
  }

  /**
   * Retrieves the value stored in the boxRef box and checks if it exists
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @abimethod({ readonly: true })
  public maybeBoxRef(key: string): [bytes, boolean] {
    const boxRef = BoxRef({ key })
    const [value, exists] = boxRef.maybe()
    return [value, exists]
  }
  // example: GET_BOX_STORAGE

  // example: SET_BOX_STORAGE
  /**
   * Sets the value of the boxInt box
   * @param valueInt The uint64 value to set in the boxInt box
   */
  public setBox(valueInt: uint64): void {
    this.boxInt.value = valueInt
  }

  /**
   * Sets the value of the boxString box
   * @param value The string value to set in the boxString box
   */
  public setBoxString(value: string): void {
    this.boxString.value = value
  }

  /**
   * Sets the value of the boxDynamicBytes box
   * @param value The dynamic bytes value to set in the boxDynamicBytes box
   */
  public setBoxDynamicBytes(value: arc4.DynamicBytes): void {
    this.boxDynamicBytes.value = value
  }

  /**
   * Sets the value of the boxMap box
   * @param key The key to set the value for
   * @param value The value to set in the boxMap box
   */
  public setBoxMap(key: uint64, value: string): void {
    this.boxMap(key).value = value
  }

  /**
   * Creates a box ref with the given key and sets its value to the sender's address
   * @param key The key to use for the box ref
   */
  public setBoxRef(key: string): void {
    const boxRef = BoxRef({ key })
    boxRef.create({ size: 32 })
    const senderBytes = Txn.sender.bytes
    boxRef.put(senderBytes)
  }
  // example: SET_BOX_STORAGE

  // example: LENGTH_BOX_STORAGE
  /**
   * Retrieves the length of the boxMap box
   * @param key The key to get the length for
   * @returns The length of the boxMap box
   */
  @abimethod({ readonly: true })
  public boxMapLength(key: uint64): uint64 {
    if (!this.boxMap(key).exists) {
      return Uint64(0)
    }

    return this.boxMap(key).length
  }

  /**
   * Retrieves the length of the boxRef box
   * @param key The key to get the length for
   * @returns The length of the boxRef box
   */
  public lengthBoxRef(key: string): uint64 {
    const boxRef = BoxRef({ key })
    assert(boxRef.create({ size: 32 }), 'boxRef creation failed')
    return boxRef.length
  }
  // example: LENGTH_BOX_STORAGE

  // example: DELETE_BOX_STORAGE
  /**
   * Deletes the value of the boxInt box
   */
  public deleteBox(): void {
    this.boxInt.delete()
    this.boxDynamicBytes.delete()
    this.boxString.delete()

    assert(this.boxInt.get({ default: Uint64(42) }) === 42)
    assert(this.boxDynamicBytes.get({ default: new arc4.DynamicBytes('42') }).native === Bytes('42'))
    assert(this.boxString.get({ default: '42' }) === '42')
  }

  /**
   * Deletes the value of the boxMap box
   * @param key The key to delete the value from
   */
  public deleteBoxMap(key: uint64): void {
    this.boxMap(key).delete()
  }

  /**
   * Deletes the value of the boxRef box
   * @param key The key to delete the value from
   */
  public deleteBoxRef(key: string): void {
    const boxRef = BoxRef({ key })
    boxRef.delete()
    assertMatch(boxRef.maybe(), [Bytes(''), false])
  }
  // example: DELETE_BOX_STORAGE

  // example: EXTRACT_BOX_STORAGE
  /**
   * Extracts a value from the boxRef box
   * @param key The key to extract from
   */
  public extractBoxRef(key: string): void {
    const senderBytes = Txn.sender.bytes
    const appAddress = Global.currentApplicationAddress.bytes

    const totalSize = Uint64(appAddress.length + senderBytes.length)

    const boxRef = BoxRef({ key })
    assert(boxRef.create({ size: totalSize }), 'boxRef creation failed')

    boxRef.replace(0, senderBytes)
    boxRef.splice(0, 0, appAddress)

    const part1 = boxRef.extract(0, 32)
    const part2 = boxRef.extract(32, 32)

    assert(part1.equals(appAddress), 'First part should match app address')
    assert(part2.equals(senderBytes), 'Second part should match sender bytes')
  }
  // example: EXTRACT_BOX_STORAGE

  // example: STRUCT_BOX_STORAGE
  /**
   * Retrieves the value stored in the boxMapStruct box
   * @param key The key to retrieve the value from
   * @returns The value stored in the boxMapStruct box
   */
  @abimethod({ readonly: true })
  public getBoxMapStruct(key: uint64): UserStruct {
    return this.boxMapStruct(key).value
  }

  /**
   * Checks if the boxMapStruct box exists
   * @param key The key to check for
   * @returns true if the box exists, false otherwise
   */
  @abimethod({ readonly: true })
  public boxMapStructExists(key: uint64): boolean {
    return this.boxMapStruct(key).exists
  }

  /**
   * Sets the value of the boxMapStruct box
   * @param key The key to set the value for
   * @param value The value to set in the boxMapStruct box
   */
  public setBoxMapStruct(key: uint64, value: UserStruct): boolean {
    // Mutable references to ARC4-encoded values must be copied using .copy() when being assigned to another variable
    this.boxMapStruct(key).value = value.copy()
    assertMatch(
      this.boxMapStruct(key).value,
      {
        name: value.name,
        id: value.id,
        asset: value.asset,
      },
      'boxMapStruct value mismatch',
    )
    return true
  }

  /**
   * Retrieves the length of the boxMapStruct box
   * @param key The key to get the length for
   * @returns The length of the boxMapStruct box
   */
  public boxMapStructLength(key: uint64): boolean {
    const value = new UserStruct({
      name: new arc4.Str('testName'),
      id: new arc4.UintN64(70),
      asset: new arc4.UintN64(1234),
    })

    this.boxMapStruct(key).value = value.copy()

    assert(this.boxMapStruct(key).value.bytes.length === value.bytes.length, 'boxMapStruct bytes length mismatch')
    assert(this.boxMapStruct(key).length === value.bytes.length, 'boxMapStruct length mismatch')

    return true
  }
  // example: STRUCT_BOX_STORAGE

  /**
   * Creates and manipulates a box containing a static array of 8-bit unsigned integers
   * @param key The key for the static array box
   * @returns The static array stored in the box
   */
  public arc4Box(key: string): StaticInts {
    const staticIntBox = Box<StaticInts>({ key: Bytes(key) })

    staticIntBox.value = new arc4.StaticArray<arc4.UintN8, 4>(
      new arc4.UintN8(0),
      new arc4.UintN8(1),
      new arc4.UintN8(2),
      new arc4.UintN8(3),
    )

    assert(staticIntBox.value[0].native === 0)
    assert(staticIntBox.value[1].native === 1)
    assert(staticIntBox.value[2].native === 2)
    assert(staticIntBox.value[3].native === 3)

    return staticIntBox.value
  }
}
