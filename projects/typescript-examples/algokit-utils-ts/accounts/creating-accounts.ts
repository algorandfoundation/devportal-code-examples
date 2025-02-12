import { setupLocalnetEnvironment } from "@/algokit-utils-ts/setup-localnet-environment";

async function creatingAccounts() {
  const { algorand } = await setupLocalnetEnvironment();

  // example: RANDOM_ACCOUNTS
  /**
   * Create random accounts that can be used for testing or development.
   * Each account will have a newly generated private/public key pair.
   */
  const randomAccount = algorand.account.random();
  const randomAccount2 = algorand.account.random();
  const randomAccount3 = algorand.account.random();
  // example: RANDOM_ACCOUNTS

  // example: ENV_ACCOUNT
  /**
   * Get or create an account from environment variables.
   * When running against LocalNet, this will create a funded wallet
   * if it doesn't exist.
   */
  const envAccount = algorand.account.fromEnvironment("MY_ACCOUNT", (1).algo());
  // example: ENV_ACCOUNT

  // example: MNEMONIC_ACCOUNT
  /**
   * Create an account from an existing mnemonic phrase.
   * Useful for recovering accounts or using predefined test accounts.
   */
  const mnemonicAccount = algorand.account.fromMnemonic("mnemonic words...");
  // example: MNEMONIC_ACCOUNT

  // example: KMD_ACCOUNT
  /**
   * Get or create an account from LocalNet's KMD (Key Management Daemon)
   * by name. If the account doesn't exist, it will be created.
   */
  const kmdAccount = algorand.account.fromKmd("ACCOUNT_NAME");
  // example: KMD_ACCOUNT

  // example: KMD_WALLET_OPERATIONS
  /**
   * Create a wallet with the KMD client.
   */
  await algorand.client.kmd.createWallet("ACCOUNT_NAME", "password");

  /**
   * Rename a wallet with the KMD client.
   */
  await algorand.client.kmd.renameWallet("ACCOUNT_NAME", "password", "NEW_ACCOUNT_NAME");
  // example: KMD_WALLET_OPERATIONS
}

creatingAccounts();
