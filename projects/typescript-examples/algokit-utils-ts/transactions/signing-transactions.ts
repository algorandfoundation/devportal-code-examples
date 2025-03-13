import { algo } from '@algorandfoundation/algokit-utils'
import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'
import algosdk from 'algosdk'

async function signingTransactions() {
  const { algorand, dispenser, randomAccountA, randomAccountB, randomAccountC } = await setupLocalnetEnvironment()

  // example: TRANSACTION_WITH_NO_SIGNER
  /* When working with account types that do not include a signer,
   * you can set the signer using the `setSigner` method.
   */

  // Generate an account with no signer. The method returns a secret key and address.
  const { sk: accountNoSignerSecretKey, addr: accountNoSignerAddress } = algosdk.generateAccount()

  // Ensure the account is funded from the dispenser account
  await algorand.account.ensureFunded(accountNoSignerAddress, dispenser, algo(10))

  // This payment transaction fails with `Error: No signer found` because the account has no signer
  try {
    await algorand.send.payment({
      sender: accountNoSignerAddress,
      receiver: randomAccountA,
      amount: algo(1),
      note: 'Sending payment with account that has no signer',
    })
  } catch (e) {
    console.log(`Error: ${e}`)
  }

  // Track the given account for later signing.
  // Note: If you are generating accounts via the various methods on AccountManager,
  // e.g., `algorand.account.random`, `algorand.account.fromMnemonic`, `algorand.account.logicsig`, etc.,
  // then they automatically get tracked.
  algorand.account.setSigner(
    accountNoSignerAddress,
    algosdk.makeBasicAccountTransactionSigner({
      sk: accountNoSignerSecretKey,
      addr: accountNoSignerAddress,
    }),
  )

  // Now the account is tracked and has the signer set so it can be used to sign transactions
  const accountWithSigner = algorand.account.getAccount(accountNoSignerAddress)

  // Since we set the signer above, the transaction will be signed by that acccount automatically
  // We have included the optional `signer` parameter for clarity
  await algorand.send.payment({
    sender: accountWithSigner.addr,
    receiver: randomAccountA,
    amount: algo(1),
    signer: accountWithSigner.signer,
    note: 'Sending payment with account that has a signer explicitly set',
  })
  // example: TRANSACTION_WITH_NO_SIGNER

  // example: TRANSACTION_WITH_SIGNER
  /**
   * When working with account types that include a signer, it can be used to sign transactions.
   * There are two ways to sign transactions using the Algorand Client.
   */

  //Method 1: Create an unsigned transaction and sign it with the `signer` attribute of the account object.
  const unsignedPayTxn = await algorand.createTransaction.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algo(1),
    note: 'Sending payment with account that has a signer using method 1',
  })

  await algorand.newGroup().addTransaction(unsignedPayTxn, randomAccountA.signer).send()

  // Method 2: Directly send the transaction using the `send` property of the Algorand Client and pass in the signer.
  await algorand.send.payment({
    sender: randomAccountB,
    receiver: randomAccountA,
    amount: algo(1),
    signer: randomAccountB.signer,
    note: 'Sending payment with account that has a signer using method 2',
  })

  // You can also set a default signer for the Algorand client.
  // The default signer, which is now randomAccountA, will be used when no specific signer is provided.
  algorand.account.setDefaultSigner(randomAccountA.signer)

  // The Algorand Client now knows the default signer and you do not need to pass in the signer.
  await algorand.send.payment({
    sender: randomAccountA,
    receiver: randomAccountB,
    amount: algo(1),
    note: 'Sending payment with account that has a default signer',
  })
  // example: TRANSACTION_WITH_SIGNER

  // example: MULTISIG_SIGNING_TRANSACTIONS

  // Create a 2-of-3 multisig account that requires
  // only 2 signature from the 3 possible signers to authorize transactions
  const multisigAccount = algorand.account.multisig(
    { version: 1, threshold: 2, addrs: [randomAccountA, randomAccountB, randomAccountC] },
    [randomAccountA.account, randomAccountB.account, randomAccountC.account],
  )

  await algorand.account.ensureFunded(multisigAccount, dispenser, algo(10))

  // Method 1: Create an unsigned transaction from the multisig account and sign it
  // with the `signer` attribute of the multisig account.
  const unsignedMultisigPayTxn = await algorand.createTransaction.payment({
    sender: multisigAccount,
    receiver: randomAccountA,
    amount: algo(1),
    note: 'Sending payment with multisig account using method 1',
  })

  await algorand.newGroup().addTransaction(unsignedMultisigPayTxn, multisigAccount.signer).send()

  // Method 2: Send a payment transaction from the multisig account
  // which will automatically collect the required number of signatures
  // from the signing accounts provided when creating the multisig account
  await algorand.send.payment({
    sender: multisigAccount,
    receiver: randomAccountA,
    amount: algo(1),
    note: 'Sending payment with multisig account using method 2',
  })
  // example: MULTISIG_SIGNING_TRANSACTIONS
}

signingTransactions()
