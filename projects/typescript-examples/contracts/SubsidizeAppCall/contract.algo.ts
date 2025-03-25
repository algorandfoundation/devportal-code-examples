import {
  TransactionType,
  Txn,
  Global,
  TemplateVar,
  gtxn,
  LogicSig,
  type uint64,
  type bytes,
  type Application,
} from '@algorandfoundation/algorand-typescript'

// example: LSIG_SUBSIDIZEAPPCALL
/**
 * A contract that subsidizes app call fees
 */
export default class SubsidizeAppCall extends LogicSig {
  /**
   * This Contract Account will subsidize the fees for any AppCall transaction directed to an application.
   * @returns True if the transaction should be approved
   */
  public program(): boolean {
    const prevTxn = gtxn.Transaction(Txn.groupIndex - 1)

    return (
      // is it safe to pay for the fees of the previous transaction?
      Txn.typeEnum === TransactionType.Payment &&
      Txn.receiver === Txn.sender &&
      Txn.amount === 0 &&
      Txn.rekeyTo === Global.zeroAddress &&
      Txn.closeRemainderTo === Global.zeroAddress &&
      Txn.fee === 2 * Global.minTxnFee &&
      Txn.lastValid <= TemplateVar<uint64>('EXPIRATION_ROUND') &&
      Global.genesisHash === TemplateVar<bytes>('TARGET_NETWORK_GENESIS') &&
      // is the previous transaction in the group an application call to a known app?
      prevTxn.type === TransactionType.ApplicationCall &&
      prevTxn.appId === TemplateVar<Application>('KNOWN_APP') &&
      prevTxn.fee === 0
    )
  }
}
// example: LSIG_SUBSIDIZEAPPCALL
