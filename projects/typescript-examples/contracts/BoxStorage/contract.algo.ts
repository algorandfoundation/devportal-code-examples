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
  public boxInt = Box<uint64>({ key: 'boxInt' })
  public boxBytes = Box<bytes>({ key: 'boxBytes' })
  public boxDynamicBytes = Box<arc4.DynamicBytes>({ key: 'boxDynamicBytes' })
  public boxString = Box<string>({ key: 'boxString' })
  public boxMap = BoxMap<uint64, string>({ keyPrefix: 'boxMap' })
  public boxRef = BoxRef({ key: 'boxRef' })
  public boxMapStruct = BoxMap<uint64, UserStruct>({ keyPrefix: 'users' })
  // example: INIT_BOX_STORAGE

  // example: GET_BOX_STORAGE_INT
  /**
   * Retrieves the value stored in the boxInt box
   * @returns The uint64 value stored in boxInt
   */
  @arc4.abimethod({ readonly: true })
  public getBox(): uint64 {
    return this.boxInt.value
  }
  // example: GET_BOX_STORAGE_INT

  // example: GET_BOX_STORAGE_MAP
  /**
   * Retrieves the value stored in the boxMap box
   * @param key The key of the boxMap to retrieve the value from
   * @returns The value stored in the boxMap box
   */
  @arc4.abimethod({ readonly: true })
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
  @arc4.abimethod({ readonly: true })
  public getBoxMapWithDefault(key: uint64): string {
    return this.boxMap.get(key, { default: 'default' })
  }
  // example: GET_BOX_STORAGE_MAP_DEFAULT

  // example: GET_BOX_STORAGE_REF
  /**
   * Retrieves the value stored in the boxRef box
   * @returns The value stored in the boxRef box
   */
  @arc4.abimethod({ readonly: false })
  public getBoxRef(): arc4.Address {
    // Create the boxRef with a size of 32 bytes (the size of an Algorand address)
    // The assert ensures the creation was successful
    this.boxRef.create({ size: 32 })
    // Get the sender's bytes
    const senderBytes = Txn.sender.bytes
    // Put the sender's bytes into the boxRef
    this.boxRef.put(senderBytes)
    // Get the value from the boxRef
    const value = this.boxRef.get({ default: senderBytes })
    // Assert the value is the sender's bytes
    assert(value === senderBytes, 'boxRef value mismatch')
    // Return the value
    return new arc4.Address(value)
  }
  // example: GET_BOX_STORAGE_REF

  // example: GET_BOX_STORAGE_MAYBE_BOX
  /**
   * Retrieves the value stored in the boxInt box and checks if it exists
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @arc4.abimethod({ readonly: true })
  public maybeBox(): [uint64, boolean] {
    const [boxIntValue, boxIntExists] = this.boxInt.maybe()
    return [boxIntValue, boxIntExists]
  }
  // example: GET_BOX_STORAGE_MAYBE_BOX

  // example: GET_BOX_STORAGE_MAYBE_BOX_MAP
  /**
   * Retrieves the value stored in the boxMap box and checks if it exists
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @arc4.abimethod({ readonly: true })
  public maybeBoxMap(): [string, boolean] {
    // Create a Uint64 instance with value 1
    const key1 = Uint64(1)
    // Retrieve the value from the boxMap using the key1
    // The maybe method returns a tuple containing the value and a boolean indicating if the box exists
    const [value, exists] = this.boxMap.maybe(key1)
    // Return a tuple containing the value and a boolean indicating if the box exists
    return [exists ? value : '', exists]
  }
  // example: GET_BOX_STORAGE_MAYBE_BOX_MAP

  // example: GET_BOX_STORAGE_MAYBE_BOX_REF
  /**
   * Retrieves the value stored in the boxRef box and checks if it exists
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @arc4.abimethod({ readonly: false })
  public maybeBoxRef(): [bytes, boolean] {
    // Create a BoxRef instance with key 'blob'
    // The native property returns the string as a bytes array
    // But you can also use the string directly as the key
    const boxRef = BoxRef({ key: new arc4.Str('blob').native })
    // Create the boxRef with a size of 32 bytes
    // The assert ensures the creation was successful
    assert(boxRef.create({ size: 32 }))
    // Retrieve the value from the boxRef
    // The maybe method returns a tuple containing the value and a boolean indicating if the box exists
    const [value, exists] = boxRef.maybe()
    // Return a tuple containing the value and a boolean indicating if the box exists
    return [exists ? value : Bytes(''), exists]
  }
  // example: GET_BOX_STORAGE_MAYBE_BOX_REF

  // example: GET_BOX_STORAGE_MAP_STRUCT
  /**
   * Retrieves the value stored in the boxMapStruct box
   * @param key The key to retrieve the value from
   * @returns The value stored in the boxMapStruct box
   */
  @arc4.abimethod({ readonly: true })
  public getBoxMapStruct(key: uint64): UserStruct {
    return this.boxMapStruct.get(key)
  }
  // example: GET_BOX_STORAGE_MAP_STRUCT

  // example: SET_BOX_STORAGE
  /**
   * Sets the value of the boxInt box
   * @param valueInt The uint64 value to set in the boxInt box
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public setBox(valueInt: uint64): void {
    this.boxInt.value = valueInt
  }
  // example: SET_BOX_STORAGE

  // example: SET_BOX_STORAGE_MAP
  /**
   * Sets the value of the boxMap box
   * @param key The key to set the value for
   * @param value The value to set in the boxMap box
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public setBoxMap(key: uint64, value: string): void {
    this.boxMap.set(key, value)
  }
  // example: SET_BOX_STORAGE_MAP

  // example: SET_BOX_STORAGE_MAP_STRUCT
  /**
   * Sets the value of the boxMapStruct box
   * @param key The key to set the value for
   * @param value The value to set in the boxMapStruct box
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public setBoxMapStruct(key: uint64, value: UserStruct): boolean {
    // Set the value in the boxMapStruct
    this.boxMapStruct.set(key, value)
    // Assert that the value is the same as the value we set
    assertMatch(
      this.boxMapStruct.get(key),
      {
        name: value.name,
        id: value.id,
        asset: value.asset,
      },
      'boxMapStruct value mismatch',
    )
    // Return true to indicate that the value was set successfully
    return true
  }
  // example: SET_BOX_STORAGE_MAP_STRUCT

  // example: DELETE_BOX_STORAGE
  /**
   * Deletes the value of the boxInt box
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public deleteBox(): void {
    // Delete the value of the boxInt box
    this.boxInt.delete()
    // Delete the value of the boxDynamicBytes box
    this.boxDynamicBytes.delete()
    // Delete the value of the boxString box
    this.boxString.delete()

    // Assert that the value of the boxInt box is the default value
    assert(this.boxInt.get({ default: Uint64(42) }) === 42)
    // Assert that the value of the boxDynamicBytes box is the default value
    assert(this.boxDynamicBytes.get({ default: new arc4.DynamicBytes('42') }).native === Bytes('42'))
    // Assert that the value of the boxString box is the default value
    assert(this.boxString.get({ default: '42' }) === '42')
  }

  // example: DELETE_BOX_MAP
  /**
   * Deletes the value of the boxMap box
   * @param key The key to delete the value from
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public deleteBoxMap(key: uint64): void {
    this.boxMap.delete(key)
  }
  // example: DELETE_BOX_MAP

  // example: DELETE_BOX_REF
  /**
   * Deletes the value of the boxRef box
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public deleteBoxRef(): void {
    // Create a BoxRef instance with key 'blog'
    const boxRef = BoxRef({ key: 'blog' })
    // Create the boxRef with a size of 32 bytes
    this.boxRef.create({ size: Uint64(32) })
    // Assert that the boxRef has data
    assert(this.boxRef.value, 'has data')
    // Delete the value of the boxRef box
    this.boxRef.delete()
    // Assert that the value of the boxRef box is the default value
    assertMatch(boxRef.maybe(), [Bytes(''), false])
  }
  // example: DELETE_BOX_REF

  // example: LENGTH_BOX_STORAGE
  /**
   * Retrieves the length of the boxMap box
   * @returns The length of the boxMap box
   */
  @arc4.abimethod({ readonly: true })
  public boxMapLength(): uint64 {
    const key0 = Uint64(0)

    if (!this.boxMap.has(key0)) {
      return Uint64(0)
    }

    return this.boxMap.length(key0)
  }
  // example: LENGTH_BOX_STORAGE

  // example: LENGTH_BOX_REF
  /**
   * Retrieves the length of the boxRef box
   * @returns The length of the boxRef box
   */
  @arc4.abimethod({ readonly: false })
  public lengthBoxRef(): uint64 {
    const boxRef = BoxRef({ key: 'blob' })

    assert(boxRef.create({ size: 32 }), 'boxRef creation failed')

    return boxRef.length
  }
  // example: LENGTH_BOX_REF

  // example: LENGTH_BOX_STORAGE_STRUCT
  /**
   * Retrieves the length of the boxMapStruct box
   * @returns The length of the boxMapStruct box
   */
  @arc4.abimethod({ readonly: false })
  public boxMapStructLength(): boolean {
    // Create a Uint64 instance with value 0
    const key0 = Uint64(0)
    // Create a new UserStruct instance with the given values
    const value = new UserStruct({
      name: new arc4.Str('testName'),
      id: new arc4.UintN64(70),
      asset: new arc4.UintN64(1234),
    })

    // Set the value in the boxMapStruct
    this.boxMapStruct.set(key0, value)

    // Assert that the value is the same as the value we set
    assert(this.boxMapStruct.get(key0).bytes.length === value.bytes.length, 'boxMapStruct bytes length mismatch')
    assert(this.boxMapStruct.length(key0) === value.bytes.length, 'boxMapStruct length mismatch')

    // Return true to indicate that the value was set successfully
    return true
  }
  // example: LENGTH_BOX_STORAGE_STRUCT

  // example: EXTRACT_BOX_REF
  /**
   * Extracts a value from the boxRef box
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public extractBoxRef(): void {
    // Get the data we'll be working with
    const senderBytes = Txn.sender.bytes
    const appAddress = Global.currentApplicationAddress.bytes

    // Calculate size needed for our two 32-byte values
    const totalSize = Uint64(appAddress.length + senderBytes.length)

    const boxRef = BoxRef({ key: 'blog' })
    // Create the boxRef with the calculated size
    assert(boxRef.create({ size: totalSize }), 'boxRef creation failed')

    // First, put sender bytes at position 0
    boxRef.replace(0, senderBytes)

    // Then, insert app address at position 0,
    // which pushes sender bytes to position 32
    boxRef.splice(0, 0, appAddress)

    // Extract the parts
    const part1 = boxRef.extract(0, 32)
    const part2 = boxRef.extract(32, 32)

    // Assert that the parts match the expected values
    assert(part1.equals(appAddress), 'First part should match app address')
    assert(part2.equals(senderBytes), 'Second part should match sender bytes')
  }
  // example: EXTRACT_BOX_REF

  // example: VALUE_BOX
  /**
   * Retrieves the value of the boxInt box
   */
  @arc4.abimethod({ readonly: true })
  public valueBox(): uint64 {
    return this.boxInt.value
  }
  // example: VALUE_BOX

  // example: ARC4_BOX
  /**
   * Creates and manipulates a box containing a static array of 8-bit unsigned integers
   * @returns The static array stored in the box
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public arc4Box(): StaticInts {
    // Create a box to store a static array of 4 UintN8 values
    const staticIntBox = Box<StaticInts>({ key: Bytes('static_ints') })

    // Initialize the box with a new static array containing values 0-3
    staticIntBox.value = new arc4.StaticArray<arc4.UintN8, 4>(
      new arc4.UintN8(0),
      new arc4.UintN8(1),
      new arc4.UintN8(2),
      new arc4.UintN8(3),
    )

    // Verify each element has the expected value
    assert(staticIntBox.value[0].native === 0)
    assert(staticIntBox.value[1].native === 1)
    assert(staticIntBox.value[2].native === 2)
    assert(staticIntBox.value[3].native === 3)

    // Return the static array from the box
    return staticIntBox.value
  }
  // example: ARC4_BOX

  // example: BOX_MAP_EXISTS
  /**
   * Checks if the boxMap box exists
   * @param key The key to check for
   * @returns true if the box exists, false otherwise
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public boxMapExists(key: uint64): boolean {
    return this.boxMap.has(key)
  }
  // example: BOX_MAP_EXISTS

  // example: BOX_MAP_STRUCT_EXISTS
  /**
   * Checks if the boxMapStruct box exists
   * @param key The key to check for
   * @returns true if the box exists, false otherwise
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public boxMapStructExists(key: uint64): boolean {
    return this.boxMapStruct.has(key)
  }
  // example: BOX_MAP_STRUCT_EXISTS

  // example: KEY_PREFIX_BOX_MAP
  /**
   * Retrieves the key prefix of the boxMap box
   * @returns The key prefix of the boxMap box
   */
  @arc4.abimethod({ readonly: true })
  public keyPrefixBoxMap(): bytes {
    return this.boxMap.keyPrefix
  }
  // example: KEY_PREFIX_BOX_MAP
}
