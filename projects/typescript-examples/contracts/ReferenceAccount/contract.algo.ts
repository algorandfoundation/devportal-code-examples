import { Contract, Account, abimethod } from '@algorandfoundation/algorand-typescript'
import { Address } from '@algorandfoundation/algorand-typescript/arc4'
/**
 * A contract that demonstrates how to use resource usage in a contract using an account reference
 */
export default class ReferenceAccount extends Contract {
  // example: ACCOUNT_REFERENCE_EXAMPLE
  /**
   * Returns the balance of the account
   * @returns The balance of the account
   */
  @abimethod({ readonly: true })
  public getAccountBalance() {
    const address = new Address('R3J76MDPEXQEWBV2LQ6FLQ4PYC4QXNHHPIL2BX2KSFU4WUNJJMDBTLRNEM')
    const addressBytes = address.bytes
    const account = Account(addressBytes)

    return account.balance
  }

  /**
   * Returns the balance of the account
   * @param account The account to get the balance of
   * @returns The balance of the account
   */
  @abimethod({ readonly: true })
  public getAccountBalanceWithArgument(account: Account) {
    return account.balance
  }
  // example: ACCOUNT_REFERENCE_EXAMPLE
}
