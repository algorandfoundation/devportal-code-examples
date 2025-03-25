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

/**
 * SelfPayment Contract
 *
 * This contract implements a delegated logic signature that authorizes
 * a single empty self payment in a block known ahead of time.
 */

export default class SelfPayment extends LogicSig {
  // example: LSIG_SELFPAYMENT
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
