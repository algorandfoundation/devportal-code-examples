# // implement app box reference example

# import { Config, microAlgos } from '@algorandfoundation/algokit-utils'
# import { setupLocalnetEnvironment } from '../setup-localnet-environment'

# async function AppBoxReferenceExampleMethod1() {
#   const { algorand, randomAccountA, referenceAppBoxAppClient } = await setupLocalnetEnvironment()

#   // Get the box MBR amount from the contract
#   const boxMBRResponse = await referenceAppBoxAppClient.getBoxMbr()
#   const boxMBR = Number(boxMBRResponse)

#   const counterAppAddress = referenceAppBoxAppClient.appAddress

#   // Fund the contract account with enough Algos before proceeding
#   await algorand.send.payment({
#     sender: randomAccountA,
#     receiver: counterAppAddress,
#     amount: microAlgos(1_000_000), // Fund with 1 Algo
#     note: 'METHOD 1: Funding contract account',
#   })

#   // example: APP_BOX_REFERENCE_EXAMPLE_METHOD_1
#   // Create payment for MBR
#   const payMbr = await algorand.createTransaction.payment({
#     amount: microAlgos(boxMBR),
#     sender: randomAccountA,
#     receiver: counterAppAddress,
#   })

#   // Method 1: Using populateAppCallResources in sendParams
#   const response1 = await referenceAppBoxAppClient.send.incrementBoxCounter({
#     args: {
#       payMbr: payMbr,
#     },
#     sender: randomAccountA,
#     populateAppCallResources: true,
#   })

#   console.log('Method #2 Box Counter (explicit)', response1.return)

#   // Method 2: Configure globally
#   // Set the default value for populateAppCallResources to true once and apply to all contract invocations
#   Config.configure({ populateAppCallResources: true })

#   // Create another payment for MBR
#   const payMbr2 = await algorand.createTransaction.payment({
#     amount: microAlgos(boxMBR),
#     sender: randomAccountA,
#     receiver: counterAppAddress,
#   })

#   // With global configuration, we don't need to specify populateAppCallResources
#   const response2 = await referenceAppBoxAppClient.send.incrementBoxCounter({
#     args: {
#       payMbr: payMbr2,
#     },
#     sender: randomAccountA,
#   })

#   console.log('Method #1 Box Counter (global)', response2.return)
#   // example: APP_BOX_REFERENCE_EXAMPLE_METHOD_1
# }

# AppBoxReferenceExampleMethod1().catch(console.error)

# async function AppBoxReferenceExampleMethod2() {
#   const { algorand, randomAccountB, referenceAppBoxAppClient } = await setupLocalnetEnvironment()

#   // Get the box MBR amount from the contract
#   const boxMBRResponse = await referenceAppBoxAppClient.getBoxMbr()
#   const boxMBR = Number(boxMBRResponse)

#   const counterAppAddress = referenceAppBoxAppClient.appAddress

#   // IMPORTANT: Fund the contract account with enough Algo before proceeding
#   await algorand.send.payment({
#     sender: randomAccountB,
#     receiver: counterAppAddress,
#     amount: microAlgos(1_000_000), // Fund with 1 Algo
#     note: 'METHOD 2: Funding contract account',
#   })

#   // example: APP_BOX_REFERENCE_EXAMPLE_METHOD_2
#   const boxPrefix = 'counter' // box identifier prefix
#   const encoder = new TextEncoder()
#   const boxPrefixBytes = encoder.encode(boxPrefix) // UInt8Array of boxPrefix
#   const publicKey = randomAccountB.addr.publicKey

#   // Create the box reference
#   const boxReference = new Uint8Array([...boxPrefixBytes, ...publicKey])

#   // Create payment for MBR
#   const payMbr = await algorand.createTransaction.payment({
#     amount: microAlgos(boxMBR),
#     sender: randomAccountB,
#     receiver: counterAppAddress,
#   })

#   // Call the smart contract with manually specified box reference
#   const response = await referenceAppBoxAppClient.send.incrementBoxCounter({
#     args: {
#       payMbr: payMbr,
#     },
#     boxReferences: [boxReference],
#     sender: randomAccountB,
#   })

#   console.log('Method #2 Box Counter', response.return)
#   // example: APP_BOX_REFERENCE_EXAMPLE_METHOD_2
# }

# AppBoxReferenceExampleMethod2().catch(console.error)
