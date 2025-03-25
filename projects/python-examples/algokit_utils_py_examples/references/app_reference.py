# import { Config, microAlgos } from '@algorandfoundation/algokit-utils'
# import { setupLocalnetEnvironment } from '../setup-localnet-environment'

# async function AppReferenceExampleMethod1() {
#   const { referenceAppAppClient } = await setupLocalnetEnvironment()

#   // example: APP_REFERENCE_EXAMPLE_METHOD_1
#   // Configure automatic resource population per app call
#   const result1 = await referenceAppAppClient.send.incrementViaInner({
#     args: {},
#     populateAppCallResources: true,
#   })

#   console.log('Method #1 Increment via inner', result1.return)

#   // Or set the default value for populateAppCallResources to true globally and apply to all app calls
#   Config.configure({
#     populateAppCallResources: true,
#   })

#   const result2 = await referenceAppAppClient.send.incrementViaInner({
#     args: {},
#     extraFee: microAlgos(1000), // additional fee to cover the inner app call
#   })

#   console.log('Method #1 Increment via inner', result2.return)
#   // example: APP_REFERENCE_EXAMPLE_METHOD_1
# }

# AppReferenceExampleMethod1().catch(console.error)

# async function AppReferenceExampleMethod2() {
#   const { referenceAppAppClient } = await setupLocalnetEnvironment()

#   // example: APP_REFERENCE_EXAMPLE_METHOD_2
#   // Include the app reference in the app call argument to be populated automatically
#   const result = await referenceAppAppClient.send.incrementViaInnerWithArg({
#     args: {
#       app: 1717n,
#     },
#     extraFee: microAlgos(1000), // additional fee to cover the inner app call
#   })

#   console.log('Method #2 Increment via inner', result.return)
#   // example: APP_REFERENCE_EXAMPLE_METHOD_2
# }

# AppReferenceExampleMethod2().catch(console.error)

# async function AppReferenceExampleMethod3() {
#   const { referenceAppAppClient } = await setupLocalnetEnvironment()

#   // example: APP_REFERENCE_EXAMPLE_METHOD_3
#   // Include the app reference in the appReferences array to be populated
#   const result = await referenceAppAppClient.send.incrementViaInner({
#     args: {},
#     appReferences: [1717n],
#     extraFee: microAlgos(1000), // additional fee to cover the inner app call
#   })

#   console.log('Method #3 Increment via inner', result.return)
#   // example: APP_REFERENCE_EXAMPLE_METHOD_3
# }

# AppReferenceExampleMethod3().catch(console.error)
