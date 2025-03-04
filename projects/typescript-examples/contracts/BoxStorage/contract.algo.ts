import {
  Box,
  arc4,
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
export default class BoxStorage extends arc4.Contract {
  // example: INIT_BOX_STORAGE
  public boxString = Box<string>({ key: 'boxString' })
  public boxInt = Box<uint64>({ key: 'boxInt' })
  public boxBytes = Box<bytes>({ key: 'boxBytes' })
  public boxDynamicBytes = Box<arc4.DynamicBytes>({ key: 'boxDynamicBytes' })
  public boxRef = BoxRef({ key: 'boxRef' })
  public boxMap = BoxMap<uint64, string>({ keyPrefix: 'boxMap' })
  public boxMapStruct = BoxMap<uint64, UserStruct>({ keyPrefix: 'users' })
  // example: INIT_BOX_STORAGE

  // Basic Box Operations (Int, String, DynamicBytes)
  // example: GET_BOX_STORAGE_INT
  /**
   * Retrieves the value stored in the boxInt box
   * @returns The uint64 value stored in boxInt
   */
  @arc4.abimethod()
  public getBox(): uint64 {
    return this.boxInt.value
  }
  // example: GET_BOX_STORAGE_INT

  // example: GET_BOX_STORAGE_VALUE
  /**
   * Retrieves the value of the boxInt box
   */
  @arc4.abimethod()
  public valueBox(): uint64 {
    return this.boxInt.value
  }
  // example: GET_BOX_STORAGE_VALUE

  // example: SET_BOX_STORAGE
  /**
   * Sets the value of the boxInt box
   * @param valueInt The uint64 value to set in the boxInt box
   */
  @arc4.abimethod()
  public setBox(valueInt: uint64): void {
    this.boxInt.value = valueInt
  }
  // example: SET_BOX_STORAGE

  // example: SET_BOX_STORAGE_STRING
  /**
   * Sets the value of the boxString box
   * @param value The string value to set in the boxString box
   */
  @arc4.abimethod()
  public setBoxString(value: string): void {
    this.boxString.value = value
  }
  // example: SET_BOX_STORAGE_STRING

  // example: SET_BOX_STORAGE_DYNAMIC_BYTES
  /**
   * Sets the value of the boxDynamicBytes box
   * @param value The dynamic bytes value to set in the boxDynamicBytes box
   */
  @arc4.abimethod()
  public setBoxDynamicBytes(value: arc4.DynamicBytes): void {
    this.boxDynamicBytes.value = value
  }
  // example: SET_BOX_STORAGE_DYNAMIC_BYTES

  // example: DELETE_BOX_STORAGE
  /**
   * Deletes the value of the boxInt box
   */
  @arc4.abimethod()
  public deleteBox(): void {
    this.boxInt.delete()
    this.boxDynamicBytes.delete()
    this.boxString.delete()

    assert(this.boxInt.get({ default: Uint64(42) }) === 42)
    assert(this.boxDynamicBytes.get({ default: new arc4.DynamicBytes('42') }).native === Bytes('42'))
    assert(this.boxString.get({ default: '42' }) === '42')
  }
  // example: DELETE_BOX_STORAGE

  // example: GET_BOX_STORAGE_MAYBE_BOX
  /**
   * Retrieves the value stored in the boxInt box and checks if it exists
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @arc4.abimethod()
  public maybeBox(): [uint64, boolean] {
    const [boxIntValue, boxIntExists] = this.boxInt.maybe()
    return [boxIntValue, boxIntExists]
  }
  // example: GET_BOX_STORAGE_MAYBE_BOX

  // BoxMap Operations
  // example: GET_BOX_STORAGE_MAP
  /**
   * Retrieves the value stored in the boxMap box
   * @param key The key of the boxMap to retrieve the value from
   * @returns The value stored in the boxMap box
   */
  @arc4.abimethod()
  public getBoxMap(key: uint64): string {
    return this.boxMap.get(key)
  }
  // example: GET_BOX_STORAGE_MAP

  // example: GET_BOX_STORAGE_MAP_DEFAULT
  /**
   * Retrieves the value stored in the boxMap box with a default value if the key does not exist
   * @param key The key of the boxMap to retrieve the value from
   * @returns The value stored in the boxMap box
   */
  @arc4.abimethod()
  public getBoxMapWithDefault(key: uint64): string {
    return this.boxMap.get(key, { default: 'default' })
  }
  // example: GET_BOX_STORAGE_MAP_DEFAULT

  // example: SET_BOX_STORAGE_MAP
  /**
   * Sets the value of the boxMap box
   * @param key The key to set the value for
   * @param value The value to set in the boxMap box
   */
  @arc4.abimethod()
  public setBoxMap(key: uint64, value: string): void {
    this.boxMap.set(key, value)
  }
  // example: SET_BOX_STORAGE_MAP

  // example: DELETE_BOX_STORAGE_MAP
  /**
   * Deletes the value of the boxMap box
   * @param key The key to delete the value from
   */
  @arc4.abimethod()
  public deleteBoxMap(key: uint64): void {
    this.boxMap.delete(key)
  }
  // example: DELETE_BOX_STORAGE_MAP

  // example: GET_BOX_STORAGE_MAYBE_BOX_MAP
  /**
   * Retrieves the value stored in the boxMap box and checks if it exists
   * @param key The key to check in the boxMap
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @arc4.abimethod()
  public maybeBoxMap(key: uint64): [string, boolean] {
    const [value, exists] = this.boxMap.maybe(key)
    return [exists ? value : '', exists]
  }
  // example: GET_BOX_STORAGE_MAYBE_BOX_MAP

  // example: LENGTH_BOX_STORAGE_MAP
  /**
   * Retrieves the length of the boxMap box
   * @param key The key to get the length for
   * @returns The length of the boxMap box
   */
  @arc4.abimethod()
  public boxMapLength(key: uint64): uint64 {
    if (!this.boxMap.has(key)) {
      return Uint64(0)
    }

    return this.boxMap.length(key)
  }
  // example: LENGTH_BOX_STORAGE_MAP

  // example: CHECK_BOX_STORAGE_MAP_EXISTS
  /**
   * Checks if the boxMap box exists
   * @param key The key to check for
   * @returns true if the box exists, false otherwise
   */
  @arc4.abimethod()
  public boxMapExists(key: uint64): boolean {
    return this.boxMap.has(key)
  }
  // example: CHECK_BOX_STORAGE_MAP_EXISTS

  // example: GET_BOX_STORAGE_MAP_KEY_PREFIX
  /**
   * Retrieves the key prefix of the boxMap box
   * @returns The key prefix of the boxMap box
   */
  @arc4.abimethod()
  public keyPrefixBoxMap(): bytes {
    return this.boxMap.keyPrefix
  }
  // example: GET_BOX_STORAGE_MAP_KEY_PREFIX

  // BoxMapStruct Operations
  // example: GET_BOX_STORAGE_MAP_STRUCT
  /**
   * Retrieves the value stored in the boxMapStruct box
   * @param key The key to retrieve the value from
   * @returns The value stored in the boxMapStruct box
   */
  @arc4.abimethod()
  public getBoxMapStruct(key: uint64): UserStruct {
    return this.boxMapStruct.get(key)
  }
  // example: GET_BOX_STORAGE_MAP_STRUCT

  // example: SET_BOX_STORAGE_MAP_STRUCT
  /**
   * Sets the value of the boxMapStruct box
   * @param key The key to set the value for
   * @param value The value to set in the boxMapStruct box
   */
  @arc4.abimethod()
  public setBoxMapStruct(key: uint64, value: UserStruct): boolean {
    this.boxMapStruct.set(key, value)
    assertMatch(
      this.boxMapStruct.get(key),
      {
        name: value.name,
        id: value.id,
        asset: value.asset,
      },
      'boxMapStruct value mismatch',
    )
    return true
  }
  // example: SET_BOX_STORAGE_MAP_STRUCT

  // example: LENGTH_BOX_STORAGE_MAP_STRUCT
  /**
   * Retrieves the length of the boxMapStruct box
   * @param key The key to get the length for
   * @returns The length of the boxMapStruct box
   */
  @arc4.abimethod()
  public boxMapStructLength(key: uint64): boolean {
    const value = new UserStruct({
      name: new arc4.Str('testName'),
      id: new arc4.UintN64(70),
      asset: new arc4.UintN64(1234),
    })

    this.boxMapStruct.set(key, value)

    assert(this.boxMapStruct.get(key).bytes.length === value.bytes.length, 'boxMapStruct bytes length mismatch')
    assert(this.boxMapStruct.length(key) === value.bytes.length, 'boxMapStruct length mismatch')

    return true
  }
  // example: LENGTH_BOX_STORAGE_MAP_STRUCT

  // example: CHECK_BOX_STORAGE_MAP_STRUCT_EXISTS
  /**
   * Checks if the boxMapStruct box exists
   * @param key The key to check for
   * @returns true if the box exists, false otherwise
   */
  @arc4.abimethod()
  public boxMapStructExists(key: uint64): boolean {
    return this.boxMapStruct.has(key)
  }
  // example: CHECK_BOX_STORAGE_MAP_STRUCT_EXISTS

  // BoxRef Operations
  // example: GET_BOX_STORAGE_REF
  /**
   * Retrieves the value stored in the boxRef box
   * @returns The value stored in the boxRef box
   */
  @arc4.abimethod()
  public getBoxRef(): arc4.Address {
    this.boxRef.create({ size: 32 })
    const senderBytes = Txn.sender.bytes
    this.boxRef.put(senderBytes)
    const value = this.boxRef.get({ default: senderBytes })
    assert(value === senderBytes, 'boxRef value mismatch')
    return new arc4.Address(value)
  }
  // example: GET_BOX_STORAGE_REF

  // example: SET_BOX_STORAGE_REF
  /**
   * Creates a box ref with the given key and sets its value to the sender's address
   * @param key The key to use for the box ref
   */
  @arc4.abimethod()
  public setBoxRef(key: string): void {
    const boxRef = BoxRef({ key })
    boxRef.create({ size: 32 })
    const senderBytes = Txn.sender.bytes
    boxRef.put(senderBytes)
  }
  // example: SET_BOX_STORAGE_REF

  // example: DELETE_BOX_STORAGE_REF
  /**
   * Deletes the value of the boxRef box
   * @param key The key to delete the value from
   */
  @arc4.abimethod()
  public deleteBoxRef(key: string): void {
    const boxRef = BoxRef({ key })
    boxRef.delete()
    assertMatch(boxRef.maybe(), [Bytes(''), false])
  }
  // example: DELETE_BOX_STORAGE_REF

  // example: GET_BOX_STORAGE_MAYBE_BOX_REF
  /**
   * Retrieves the value stored in the boxRef box and checks if it exists
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @arc4.abimethod()
  public maybeBoxRef(key: string): [bytes, boolean] {
    const boxRef = BoxRef({ key })
    const [value, exists] = boxRef.maybe()
    return [value, exists]
  }
  // example: GET_BOX_STORAGE_MAYBE_BOX_REF

  // example: LENGTH_BOX_STORAGE_REF
  /**
   * Retrieves the length of the boxRef box
   * @param key The key to get the length for
   * @returns The length of the boxRef box
   */
  @arc4.abimethod()
  public lengthBoxRef(key: string): uint64 {
    const boxRef = BoxRef({ key })
    assert(boxRef.create({ size: 32 }), 'boxRef creation failed')
    return boxRef.length
  }
  // example: LENGTH_BOX_STORAGE_REF

  // example: EXTRACT_BOX_STORAGE_REF
  /**
   * Extracts a value from the boxRef box
   * @param key The key to extract from
   */
  @arc4.abimethod()
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
  // example: EXTRACT_BOX_STORAGE_REF

  // Special Operations
  // example: CREATE_BOX_STORAGE_ARC4
  /**
   * Creates and manipulates a box containing a static array of 8-bit unsigned integers
   * @param key The key for the static array box
   * @returns The static array stored in the box
   */
  @arc4.abimethod()
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
  // example: CREATE_BOX_STORAGE_ARC4
}
