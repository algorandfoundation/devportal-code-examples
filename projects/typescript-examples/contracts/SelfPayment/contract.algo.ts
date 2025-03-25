import {
  Global,
  TemplateVar,
  TransactionType,
  Txn,
  bytes,
  uint64,
  op,
  Bytes,
  LogicSig,
} from '@algorandfoundation/algorand-typescript'

// example: LSIG_SELFPAYMENT
/**
 * A contract that authorizes a single self-payment transaction
 */
export default class SelfPayment extends LogicSig {
  /**
   * This Contract Account authorizes a single empty self-payment transaction in a specific block.
   * The contract includes safety measures like lease and network validation to prevent replay attacks.
   * @returns True if the transaction should be approved
   */
  public program(): boolean {
    return (
      Txn.typeEnum === TransactionType.Payment &&
      Txn.receiver === Txn.sender &&
      Txn.amount === 0 &&
      Txn.rekeyTo === Global.zeroAddress &&
      Txn.closeRemainderTo === Global.zeroAddress &&
      Txn.fee === Global.minTxnFee &&
      Global.genesisHash === TemplateVar<bytes>('TARGET_NETWORK_GENESIS') &&
      // Acquiring a lease with last_round and a non-empty lease field prevents replay attacks
      Txn.lastValid === TemplateVar<uint64>('LAST_ROUND') &&
      Txn.lease === op.sha256(Bytes('self-payment'))
    )
  }
  // example: LSIG_SELFPAYMENT
}
