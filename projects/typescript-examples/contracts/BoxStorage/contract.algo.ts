import { Box, arc4, bytes, Bytes, uint64, Uint64 } from '@algorandfoundation/algorand-typescript'

/**
 * A simple box storage example contract
 */
export default class BoxStorage extends arc4.Contract {
  public boxInt = Box<uint64>({ key: 'boxInt' })
  public boxBytes = Box<bytes>({ key: 'boxBytes' })

  /**
   * setBoxInt method
   * @returns boolean
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public setBoxBytes(value: string): boolean {
    this.boxBytes.value = Bytes(value)

    return true
  }

  /**
   * setBoxInt method
   * @returns boolean
   */
  @arc4.abimethod({ allowActions: ['NoOp'], readonly: false })
  public setBoxInt(value: uint64): boolean {
    this.boxInt.value = Uint64(value)

    return true
  }
}
