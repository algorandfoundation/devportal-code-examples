import { setupLocalnetEnvironment } from '@/algokit-utils-ts/setup-localnet-environment'

async function assetCreate() {
  const { algorand, randomAccountA } = await setupLocalnetEnvironment()

  // example: ASSET_CREATE_TRANSACTION

  /**
   * Send an asset create transaction creating a fungible ASA with 10 million units
   *
   * Parameters for creating a new asset:
   * - sender: The address of the account that will send the transaction
   * - total: The total amount of the smallest divisible unit to create
   * - decimals: The amount of decimal places the asset should have, defaults to undefined
   * - defaultFrozen: Whether the asset is frozen by default in the creator address, defaults to undefined
   * - manager: The address that can change the manager, reserve, clawback, and freeze addresses, defaults to undefined
   * - reserve: The address that holds the uncirculated supply, defaults to undefined
   * - freeze: The address that can freeze the asset in any account, defaults to undefined
   * - clawback: The address that can clawback the asset from any account, defaults to undefined
   * - unitName: The short ticker name for the asset, defaults to undefined
   * - assetName: The full name of the asset, defaults to undefined
   */
  const createFungibleResult = await algorand.send.assetCreate({
    sender: randomAccountA.addr,
    total: 10_000_000n,
    decimals: 6,
    defaultFrozen: false,
    manager: randomAccountA.addr,
    reserve: randomAccountA.addr,
    freeze: randomAccountA.addr,
    clawback: randomAccountA.addr,
    unitName: 'MYA',
    assetName: 'My Asset',
  })

  console.log('Fungible asset created with ID:', createFungibleResult.assetId)

  /**
   * Send an asset create transaction creating a 1 to 1 unique NFT
   */
  const createNFTResult = await algorand.send.assetCreate({
    sender: randomAccountA.addr,
    total: 1n,
    assetName: 'My NFT',
    unitName: 'MNFT',
    decimals: 0,
    url: 'metadata URL',
    metadataHash: new Uint8Array(Buffer.from('Hash of the metadata URL')),
  })

  console.log('NFT created with ID:', createNFTResult.assetId)

  // example: ASSET_CREATE_TRANSACTION
}

assetCreate().catch(console.error)
