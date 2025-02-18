import { Config } from '@algorandfoundation/algokit-utils'
import { registerDebugEventHandlers } from '@algorandfoundation/algokit-utils-debug'
import { consoleLogger } from '@algorandfoundation/algokit-utils/types/logging'
import * as fs from 'node:fs'
import * as path from 'node:path'

// Uncomment the traceAll option to enable auto generation of AVM Debugger compliant sourceMap and simulation trace file for all AVM calls.
// Learn more about using AlgoKit AVM Debugger to debug your TEAL source codes and inspect various kinds of Algorand transactions in atomic groups -> https://github.com/algorandfoundation/algokit-avm-vscode-Debugger

Config.configure({
  logger: consoleLogger,
  debug: true,
  traceAll: true,
})
registerDebugEventHandlers()

// base directory
const baseDir = path.resolve(__dirname)

// function to validate and dynamically import a module
async function importDeployerIfExists(dir: string) {
  const deployerPath = path.resolve(dir, 'deploy-config')
  // Check if deploy config exists in current directory
  if (fs.existsSync(deployerPath + '.ts') || fs.existsSync(deployerPath + '.js')) {
    const deployer = await import(deployerPath)
    return { ...deployer, name: path.basename(dir) }
  }
  return null
}

// get a list of all deployers recursively from subdirectories
async function getDeployers() {
  function getDirectoriesRecursive(dir: string): string[] {
    const entries = fs.readdirSync(dir, { withFileTypes: true })

    const dirs = entries.filter((entry) => entry.isDirectory()).map((entry) => path.resolve(dir, entry.name))

    const subdirs = dirs.flatMap((d) => getDirectoriesRecursive(d))
    return [...dirs, ...subdirs]
  }

  const directories = getDirectoriesRecursive(baseDir).filter(
    (dir) => !dir.includes('artifacts') && !dir.includes('clients'),
  ) // Exclude artifacts and clients dirs

  const deployers = await Promise.all(directories.map(importDeployerIfExists))
  return deployers.filter((deployer): deployer is NonNullable<typeof deployer> => deployer !== null)
}

// execute all the deployers
async function main() {
  const contractName = process.argv.length > 2 ? process.argv[2] : undefined
  const contractDeployers = await getDeployers()

  const filteredDeployers = contractName
    ? contractDeployers.filter((deployer) => deployer.name === contractName)
    : contractDeployers

  if (contractName && filteredDeployers.length === 0) {
    console.warn(`No deployer found for contract name: ${contractName}`)
    return
  }

  for (const deployer of filteredDeployers) {
    try {
      await deployer.deploy()
    } catch (e) {
      console.error(`Error deploying ${deployer.name}:`, e)
    }
  }
}

// Only run if this file is being run directly
if (require.main === module) {
  main().catch(console.error)
}
