import {
  Box,
  arc4,
  Contract,
  bytes,
  Bytes,
  uint64,
  Uint64,
  BoxMap,
  Global,
  Txn,
  clone,
  FixedArray,
  readonly,
} from '@algorandfoundation/algorand-typescript'
import { assert, assertMatch } from '@algorandfoundation/algorand-typescript'
import { Uint8 } from '@algorandfoundation/algorand-typescript/arc4'

type Uint8x4 = FixedArray<arc4.Uint8, 4>

type User = {
  name: string
  id: uint64
  asset: uint64
}

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
  public boxMap = BoxMap<uint64, string>({ keyPrefix: 'boxMap' })
  public boxMapObject = BoxMap<uint64, User>({ keyPrefix: 'users' })
  // example: INIT_BOX_STORAGE

  // example: GET_BOX_STORAGE
  /**
   * Retrieves the value stored in the boxInt box
   * @returns The uint64 value stored in boxInt
   */
  @readonly
  public getBox(): uint64 {
    return this.boxInt.value
  }

  /**
   * Retrieves the value of the boxInt box
   */
  @readonly
  public valueBox(): uint64 {
    return this.boxInt.value
  }

  /**
   * Retrieves the value stored in the boxInt box and checks if it exists
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @readonly
  public maybeBox(): [uint64, boolean] {
    const [boxIntValue, boxIntExists] = this.boxInt.maybe()
    return [boxIntValue, boxIntExists]
  }

  /**
   * Retrieves the value stored in the boxMap box
   * @param key The key of the boxMap to retrieve the value from
   * @returns The value stored in the boxMap box
   */
  @readonly
  public getBoxMap(key: uint64): string {
    return this.boxMap(key).value
  }

  /**
   * Retrieves the value stored in the boxMap box with a default value if the key does not exist
   * @param key The key of the boxMap to retrieve the value from
   * @returns The value stored in the boxMap box
   */
  @readonly
  public getBoxMapWithDefault(key: uint64): string {
    return this.boxMap(key).get({ default: 'default' })
  }

  /**
   * Retrieves the value stored in the boxMap box and checks if it exists
   * @param key The key to check in the boxMap
   * @returns A tuple containing the value and a boolean indicating if the box exists
   */
  @readonly
  public maybeBoxMap(key: uint64): [string, boolean] {
    const [value, exists] = this.boxMap(key).maybe()
    return [exists ? value : '', exists]
  }

  /**
   * Retrieves the key prefix of the boxMap box
   * @returns The key prefix of the boxMap box
   */
  @readonly
  public keyPrefixBoxMap(): bytes {
    return this.boxMap.keyPrefix
  }

  /**
   * Checks if the boxMap box exists
   * @param key The key to check for
   * @returns true if the box exists, false otherwise
   */
  @readonly
  public boxMapExists(key: uint64): boolean {
    return this.boxMap(key).exists
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
  // example: SET_BOX_STORAGE

  // example: LENGTH_BOX_STORAGE
  /**
   * Retrieves the length of the boxMap box
   * @param key The key to get the length for
   * @returns The length of the boxMap box
   */
  @readonly
  public boxMapLength(key: uint64): uint64 {
    if (!this.boxMap(key).exists) {
      return Uint64(0)
    }

    return this.boxMap(key).length
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
  // example: DELETE_BOX_STORAGE

  // example: EXTRACT_BOX_STORAGE
  /**
   * Extracts a value from the boxRef box
   * @param key The key to extract from
   */
  public extractBox(key: string): void {
    const senderBytes = Txn.sender.bytes
    const appAddress = Global.currentApplicationAddress.bytes
    const totalSize = Uint64(appAddress.length + senderBytes.length)
    const box = Box<bytes>({ key })

    assert(box.create({ size: totalSize }), 'box creation failed')

    box.replace(0, senderBytes)
    box.splice(0, 0, appAddress)

    const part1 = box.extract(0, 32)
    const part2 = box.extract(32, 32)

    assert(part1.equals(appAddress), 'First part should match app address')
    assert(part2.equals(senderBytes), 'Second part should match sender bytes')
  }
  // example: EXTRACT_BOX_STORAGE

  // example: STRUCT_BOX_STORAGE
  /**
   * Retrieves the value stored in the boxMapObject box
   * @param key The key to retrieve the value from
   * @returns The value stored in the boxMapObject box
   */
  @readonly
  public getBoxMapObject(key: uint64): User {
    return this.boxMapObject(key).value
  }

  /**
   * Checks if the boxMapObject box exists
   * @param key The key to check for
   * @returns true if the box exists, false otherwise
   */
  @readonly
  public boxMapObjectExists(key: uint64): boolean {
    return this.boxMapObject(key).exists
  }

  /**
   * Sets the value of the boxMapObject box
   * @param key The key to set the value for
   * @param value The value to set in the boxMapObject box
   */
  public setBoxMapObject(key: uint64, value: User): boolean {
    this.boxMapObject(key).value = clone(value)
    assertMatch(
      this.boxMapObject(key).value,
      {
        name: value.name,
        id: value.id,
        asset: value.asset,
      },
      'boxMapObject value mismatch',
    )
    return true
  }

  /**
   * Retrieves the length of the boxMapObject box
   * @param key The key to get the length for
   * @returns The length of the boxMapObject box
   */
  public boxMapObjectLength(key: uint64): uint64 {
    const value = {
      name: 'testName',
      id: Uint64(70),
      asset: Uint64(1234),
    }

    this.boxMapObject(key).value = clone(value)

    return this.boxMapObject(key).length
  }
  // example: STRUCT_BOX_STORAGE

  // example: OTHER_OPS_BOX
  /**
   * Creates and manipulates a box containing a fixed array of 8-bit unsigned integers
   * @param key The key for the static array box
   * @returns The static array stored in the box
   */
  public arc4Box(key: string): Uint8x4 {
    const staticIntBox = Box<Uint8x4>({ key: Bytes(key) })

    staticIntBox.value = new FixedArray<arc4.Uint8, 4>(new Uint8(0), new Uint8(1), new Uint8(2), new Uint8(3))

    assert(staticIntBox.value[0].asUint64() === 0)
    assert(staticIntBox.value[1].asUint64() === 1)
    assert(staticIntBox.value[2].asUint64() === 2)
    assert(staticIntBox.value[3].asUint64() === 3)

    return staticIntBox.value
  }
  // example: OTHER_OPS_BOX
}
