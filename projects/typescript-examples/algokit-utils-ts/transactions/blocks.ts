import { setupLocalnetEnvironment } from '../setup-localnet-environment'

async function blocks(): Promise<void> {
  // Setup the test environment
  const { algorand } = await setupLocalnetEnvironment()

  // example: BLOCKS
  /**
   * Gets the block info for the given round.
   *
   * @param roundNumber - The round number of the block to get.
   * @category GET
   */
  const block = await algorand.client.algod.block(1).do()

  console.log(block)
  /**
   * BlockResponse {
   *  block: Block {
   *    header: BlockHeader {
   *      round: 1n,
   *      branch: [Uint8Array],
   *      seed: [Uint8Array],
   *      txnCommitments: [TxnCommitments],
   *      timestamp: 1742832892n,
   *      genesisID: 'dockernet-v1',
   *      genesisHash: [Uint8Array],
   *      proposer: [Address],
   *      feesCollected: 1000n,
   *      bonus: 10000000n,
   *      proposerPayout: 0n,
   *      rewardState: [RewardState],
   *      upgradeState: [UpgradeState],
   *      upgradeVote: [UpgradeVote],
   *      txnCounter: 1001n,
   *      stateproofTracking: [Map],
   *      participationUpdates: [ParticipationUpdates]
   *    },
   *    payset: [ [SignedTxnInBlock] ]
   *  },
   *  cert: UntypedValue { data: Map(1) { 'rnd' => 1n } }
   * }
   */
  // example: BLOCKS
}

blocks().catch(console.error)
