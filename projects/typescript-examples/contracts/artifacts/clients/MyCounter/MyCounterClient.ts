/* eslint-disable */
/**
 * This file was automatically generated by @algorandfoundation/algokit-client-generator.
 * DO NOT MODIFY IT BY HAND.
 * requires: @algorandfoundation/algokit-utils: ^7
 */
import { AlgorandClientInterface } from '@algorandfoundation/algokit-utils/types/algorand-client-interface'
import { ABIReturn, AppReturn, SendAppTransactionResult } from '@algorandfoundation/algokit-utils/types/app'
import { Arc56Contract, getArc56ReturnValue, getABIStructFromABITuple } from '@algorandfoundation/algokit-utils/types/app-arc56'
import {
  AppClient as _AppClient,
  AppClientMethodCallParams,
  AppClientParams,
  AppClientBareCallParams,
  CallOnComplete,
  AppClientCompilationParams,
  ResolveAppClientByCreatorAndName,
  ResolveAppClientByNetwork,
  CloneAppClientParams,
} from '@algorandfoundation/algokit-utils/types/app-client'
import { AppFactory as _AppFactory, AppFactoryAppClientParams, AppFactoryResolveAppClientByCreatorAndNameParams, AppFactoryDeployParams, AppFactoryParams, CreateSchema } from '@algorandfoundation/algokit-utils/types/app-factory'
import { TransactionComposer, AppCallMethodCall, AppMethodCallTransactionArgument, SimulateOptions, RawSimulateOptions, SkipSignaturesSimulateOptions } from '@algorandfoundation/algokit-utils/types/composer'
import { SendParams, SendSingleTransactionResult, SendAtomicTransactionComposerResults } from '@algorandfoundation/algokit-utils/types/transaction'
import { Address, encodeAddress, modelsv2, OnApplicationComplete, Transaction, TransactionSigner } from 'algosdk'
import SimulateResponse = modelsv2.SimulateResponse

export const APP_SPEC: Arc56Contract = {"name":"MyCounter","structs":{},"methods":[{"name":"optIn","args":[],"returns":{"type":"void"},"actions":{"create":[],"call":["OptIn"]},"readonly":false,"desc":"Initialize the counter when an account opts in","events":[],"recommendations":{}},{"name":"incrementMyCounter","args":[],"returns":{"type":"uint64","desc":"The new counter value"},"actions":{"create":[],"call":["NoOp"]},"readonly":false,"desc":"Increment the counter for the sender and return its new value","events":[],"recommendations":{}}],"arcs":[22,28],"desc":"A contract that maintains a per-account counter in local state\nAccounts must opt in to use the counter","networks":{},"state":{"schema":{"global":{"ints":0,"bytes":0},"local":{"ints":1,"bytes":0}},"keys":{"global":{},"local":{"myCounter":{"keyType":"AVMString","valueType":"AVMUint64","key":"bXlfY291bnRlcg=="}},"box":{}},"maps":{"global":{},"local":{},"box":{}}},"bareActions":{"create":["NoOp"],"call":[]},"sourceInfo":{"approval":{"sourceInfo":[{"pc":[103],"errorMessage":"Account must opt in to contract first"},{"pc":[49],"errorMessage":"OnCompletion is not NoOp"},{"pc":[72],"errorMessage":"OnCompletion is not OptIn"},{"pc":[89],"errorMessage":"can only call when creating"},{"pc":[52,75],"errorMessage":"can only call when not creating"},{"pc":[109,123],"errorMessage":"check LocalState exists"}],"pcOffsetMethod":"none"},"clear":{"sourceInfo":[],"pcOffsetMethod":"none"}},"source":{"approval":"I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBAYWxnb3JhbmRmb3VuZGF0aW9uL2FsZ29yYW5kLXR5cGVzY3JpcHQvYXJjNC9pbmRleC5kLnRzOjpDb250cmFjdC5hcHByb3ZhbFByb2dyYW0oKSAtPiB1aW50NjQ6Cm1haW46CiAgICBpbnRjYmxvY2sgMSAwCiAgICBieXRlY2Jsb2NrICJteV9jb3VudGVyIgogICAgLy8gY29udHJhY3RzL1JlZmVyZW5jZUFjY291bnRBcHAvY29udHJhY3QuYWxnby50czoyMAogICAgLy8gZXhwb3J0IGNsYXNzIE15Q291bnRlciBleHRlbmRzIENvbnRyYWN0IHsKICAgIHR4biBOdW1BcHBBcmdzCiAgICBieiBtYWluX2JhcmVfcm91dGluZ0A3CiAgICBwdXNoYnl0ZXNzIDB4MjkzMTRkOTUgMHhlNmRiZWQ3ZiAvLyBtZXRob2QgIm9wdEluKCl2b2lkIiwgbWV0aG9kICJpbmNyZW1lbnRNeUNvdW50ZXIoKXVpbnQ2NCIKICAgIHR4bmEgQXBwbGljYXRpb25BcmdzIDAKICAgIG1hdGNoIG1haW5fb3B0SW5fcm91dGVAMyBtYWluX2luY3JlbWVudE15Q291bnRlcl9yb3V0ZUA0CgptYWluX2FmdGVyX2lmX2Vsc2VAMTE6CiAgICAvLyBjb250cmFjdHMvUmVmZXJlbmNlQWNjb3VudEFwcC9jb250cmFjdC5hbGdvLnRzOjIwCiAgICAvLyBleHBvcnQgY2xhc3MgTXlDb3VudGVyIGV4dGVuZHMgQ29udHJhY3QgewogICAgaW50Y18xIC8vIDAKICAgIHJldHVybgoKbWFpbl9pbmNyZW1lbnRNeUNvdW50ZXJfcm91dGVANDoKICAgIC8vIGNvbnRyYWN0cy9SZWZlcmVuY2VBY2NvdW50QXBwL2NvbnRyYWN0LmFsZ28udHM6MzYKICAgIC8vIEBhYmltZXRob2QoKQogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBub3QgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICBjYWxsc3ViIGluY3JlbWVudE15Q291bnRlcgogICAgaXRvYgogICAgcHVzaGJ5dGVzIDB4MTUxZjdjNzUKICAgIHN3YXAKICAgIGNvbmNhdAogICAgbG9nCiAgICBpbnRjXzAgLy8gMQogICAgcmV0dXJuCgptYWluX29wdEluX3JvdXRlQDM6CiAgICAvLyBjb250cmFjdHMvUmVmZXJlbmNlQWNjb3VudEFwcC9jb250cmFjdC5hbGdvLnRzOjI3CiAgICAvLyBAYWJpbWV0aG9kKHsgYWxsb3dBY3Rpb25zOiAnT3B0SW4nIH0pCiAgICB0eG4gT25Db21wbGV0aW9uCiAgICBpbnRjXzAgLy8gT3B0SW4KICAgID09CiAgICBhc3NlcnQgLy8gT25Db21wbGV0aW9uIGlzIG5vdCBPcHRJbgogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICBjYWxsc3ViIG9wdEluCiAgICBpbnRjXzAgLy8gMQogICAgcmV0dXJuCgptYWluX2JhcmVfcm91dGluZ0A3OgogICAgLy8gY29udHJhY3RzL1JlZmVyZW5jZUFjY291bnRBcHAvY29udHJhY3QuYWxnby50czoyMAogICAgLy8gZXhwb3J0IGNsYXNzIE15Q291bnRlciBleHRlbmRzIENvbnRyYWN0IHsKICAgIHR4biBPbkNvbXBsZXRpb24KICAgIGJueiBtYWluX2FmdGVyX2lmX2Vsc2VAMTEKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICAhCiAgICBhc3NlcnQgLy8gY2FuIG9ubHkgY2FsbCB3aGVuIGNyZWF0aW5nCiAgICBpbnRjXzAgLy8gMQogICAgcmV0dXJuCgoKLy8gY29udHJhY3RzL1JlZmVyZW5jZUFjY291bnRBcHAvY29udHJhY3QuYWxnby50czo6TXlDb3VudGVyLm9wdEluKCkgLT4gdm9pZDoKb3B0SW46CiAgICAvLyBjb250cmFjdHMvUmVmZXJlbmNlQWNjb3VudEFwcC9jb250cmFjdC5hbGdvLnRzOjI5CiAgICAvLyB0aGlzLm15Q291bnRlcihUeG4uc2VuZGVyKS52YWx1ZSA9IDAKICAgIHR4biBTZW5kZXIKICAgIC8vIGNvbnRyYWN0cy9SZWZlcmVuY2VBY2NvdW50QXBwL2NvbnRyYWN0LmFsZ28udHM6MjIKICAgIC8vIHB1YmxpYyBteUNvdW50ZXIgPSBMb2NhbFN0YXRlPHVpbnQ2ND4oeyBrZXk6ICdteV9jb3VudGVyJyB9KQogICAgYnl0ZWNfMCAvLyAibXlfY291bnRlciIKICAgIC8vIGNvbnRyYWN0cy9SZWZlcmVuY2VBY2NvdW50QXBwL2NvbnRyYWN0LmFsZ28udHM6MjkKICAgIC8vIHRoaXMubXlDb3VudGVyKFR4bi5zZW5kZXIpLnZhbHVlID0gMAogICAgaW50Y18xIC8vIDAKICAgIGFwcF9sb2NhbF9wdXQKICAgIHJldHN1YgoKCi8vIGNvbnRyYWN0cy9SZWZlcmVuY2VBY2NvdW50QXBwL2NvbnRyYWN0LmFsZ28udHM6Ok15Q291bnRlci5pbmNyZW1lbnRNeUNvdW50ZXIoKSAtPiB1aW50NjQ6CmluY3JlbWVudE15Q291bnRlcjoKICAgIC8vIGNvbnRyYWN0cy9SZWZlcmVuY2VBY2NvdW50QXBwL2NvbnRyYWN0LmFsZ28udHM6MzgKICAgIC8vIGFzc2VydChUeG4uc2VuZGVyLmlzT3B0ZWRJbihHbG9iYWwuY3VycmVudEFwcGxpY2F0aW9uSWQpLCAnQWNjb3VudCBtdXN0IG9wdCBpbiB0byBjb250cmFjdCBmaXJzdCcpCiAgICB0eG4gU2VuZGVyCiAgICBnbG9iYWwgQ3VycmVudEFwcGxpY2F0aW9uSUQKICAgIGFwcF9vcHRlZF9pbgogICAgYXNzZXJ0IC8vIEFjY291bnQgbXVzdCBvcHQgaW4gdG8gY29udHJhY3QgZmlyc3QKICAgIC8vIGNvbnRyYWN0cy9SZWZlcmVuY2VBY2NvdW50QXBwL2NvbnRyYWN0LmFsZ28udHM6NDAKICAgIC8vIHRoaXMubXlDb3VudGVyKFR4bi5zZW5kZXIpLnZhbHVlID0gdGhpcy5teUNvdW50ZXIoVHhuLnNlbmRlcikudmFsdWUgKyAxCiAgICB0eG4gU2VuZGVyCiAgICBpbnRjXzEgLy8gMAogICAgLy8gY29udHJhY3RzL1JlZmVyZW5jZUFjY291bnRBcHAvY29udHJhY3QuYWxnby50czoyMgogICAgLy8gcHVibGljIG15Q291bnRlciA9IExvY2FsU3RhdGU8dWludDY0Pih7IGtleTogJ215X2NvdW50ZXInIH0pCiAgICBieXRlY18wIC8vICJteV9jb3VudGVyIgogICAgLy8gY29udHJhY3RzL1JlZmVyZW5jZUFjY291bnRBcHAvY29udHJhY3QuYWxnby50czo0MAogICAgLy8gdGhpcy5teUNvdW50ZXIoVHhuLnNlbmRlcikudmFsdWUgPSB0aGlzLm15Q291bnRlcihUeG4uc2VuZGVyKS52YWx1ZSArIDEKICAgIGFwcF9sb2NhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBMb2NhbFN0YXRlIGV4aXN0cwogICAgdHhuIFNlbmRlcgogICAgc3dhcAogICAgaW50Y18wIC8vIDEKICAgICsKICAgIC8vIGNvbnRyYWN0cy9SZWZlcmVuY2VBY2NvdW50QXBwL2NvbnRyYWN0LmFsZ28udHM6MjIKICAgIC8vIHB1YmxpYyBteUNvdW50ZXIgPSBMb2NhbFN0YXRlPHVpbnQ2ND4oeyBrZXk6ICdteV9jb3VudGVyJyB9KQogICAgYnl0ZWNfMCAvLyAibXlfY291bnRlciIKICAgIC8vIGNvbnRyYWN0cy9SZWZlcmVuY2VBY2NvdW50QXBwL2NvbnRyYWN0LmFsZ28udHM6NDAKICAgIC8vIHRoaXMubXlDb3VudGVyKFR4bi5zZW5kZXIpLnZhbHVlID0gdGhpcy5teUNvdW50ZXIoVHhuLnNlbmRlcikudmFsdWUgKyAxCiAgICBzd2FwCiAgICBhcHBfbG9jYWxfcHV0CiAgICAvLyBjb250cmFjdHMvUmVmZXJlbmNlQWNjb3VudEFwcC9jb250cmFjdC5hbGdvLnRzOjQyCiAgICAvLyByZXR1cm4gdGhpcy5teUNvdW50ZXIoVHhuLnNlbmRlcikudmFsdWUKICAgIHR4biBTZW5kZXIKICAgIGludGNfMSAvLyAwCiAgICAvLyBjb250cmFjdHMvUmVmZXJlbmNlQWNjb3VudEFwcC9jb250cmFjdC5hbGdvLnRzOjIyCiAgICAvLyBwdWJsaWMgbXlDb3VudGVyID0gTG9jYWxTdGF0ZTx1aW50NjQ+KHsga2V5OiAnbXlfY291bnRlcicgfSkKICAgIGJ5dGVjXzAgLy8gIm15X2NvdW50ZXIiCiAgICAvLyBjb250cmFjdHMvUmVmZXJlbmNlQWNjb3VudEFwcC9jb250cmFjdC5hbGdvLnRzOjQyCiAgICAvLyByZXR1cm4gdGhpcy5teUNvdW50ZXIoVHhuLnNlbmRlcikudmFsdWUKICAgIGFwcF9sb2NhbF9nZXRfZXgKICAgIGFzc2VydCAvLyBjaGVjayBMb2NhbFN0YXRlIGV4aXN0cwogICAgcmV0c3ViCg==","clear":"I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBAYWxnb3JhbmRmb3VuZGF0aW9uL2FsZ29yYW5kLXR5cGVzY3JpcHQvYmFzZS1jb250cmFjdC5kLnRzOjpCYXNlQ29udHJhY3QuY2xlYXJTdGF0ZVByb2dyYW0oKSAtPiB1aW50NjQ6Cm1haW46CiAgICBwdXNoaW50IDEgLy8gMQogICAgcmV0dXJuCg=="},"byteCode":{"approval":"CiACAQAmAQpteV9jb3VudGVyMRtBADqCAgQpMU2VBObb7X82GgCOAgAYAAIjQzEZFEQxGESIACoWgAQVH3x1TFCwIkMxGSISRDEYRIgADSJDMRlA/9YxGBREIkMxACgjZokxADIIYUQxACMoY0QxAEwiCChMZjEAIyhjRIk=","clear":"CoEBQw=="},"compilerInfo":{"compiler":"puya","compilerVersion":{"major":4,"minor":4,"patch":4}},"events":[],"templateVariables":{}} as unknown as Arc56Contract

/**
 * A state record containing binary data
 */
export interface BinaryState {
  /**
   * Gets the state value as a Uint8Array
   */
  asByteArray(): Uint8Array | undefined
  /**
   * Gets the state value as a string
   */
  asString(): string | undefined
}

class BinaryStateValue implements BinaryState {
  constructor(private value: Uint8Array | undefined) {}

  asByteArray(): Uint8Array | undefined {
    return this.value
  }

  asString(): string | undefined {
    return this.value !== undefined ? Buffer.from(this.value).toString('utf-8') : undefined
  }
}

/**
 * Expands types for IntelliSense so they are more human readable
 * See https://stackoverflow.com/a/69288824
 */
export type Expand<T> = T extends (...args: infer A) => infer R
  ? (...args: Expand<A>) => Expand<R>
  : T extends infer O
    ? { [K in keyof O]: O[K] }
    : never


/**
 * The argument types for the MyCounter contract
 */
export type MyCounterArgs = {
  /**
   * The object representation of the arguments for each method
   */
  obj: {
    'optIn()void': Record<string, never>
    'incrementMyCounter()uint64': Record<string, never>
  }
  /**
   * The tuple representation of the arguments for each method
   */
  tuple: {
    'optIn()void': []
    'incrementMyCounter()uint64': []
  }
}

/**
 * The return type for each method
 */
export type MyCounterReturns = {
  'optIn()void': void
  'incrementMyCounter()uint64': bigint
}

/**
 * Defines the types of available calls and state of the MyCounter smart contract.
 */
export type MyCounterTypes = {
  /**
   * Maps method signatures / names to their argument and return types.
   */
  methods:
    & Record<'optIn()void' | 'optIn', {
      argsObj: MyCounterArgs['obj']['optIn()void']
      argsTuple: MyCounterArgs['tuple']['optIn()void']
      returns: MyCounterReturns['optIn()void']
    }>
    & Record<'incrementMyCounter()uint64' | 'incrementMyCounter', {
      argsObj: MyCounterArgs['obj']['incrementMyCounter()uint64']
      argsTuple: MyCounterArgs['tuple']['incrementMyCounter()uint64']
      /**
       * The new counter value
       */
      returns: MyCounterReturns['incrementMyCounter()uint64']
    }>
  /**
   * Defines the shape of the state of the application.
   */
  state: {
    local: {
      keys: {
        myCounter: bigint
      }
      maps: {}
    }
  }
}

/**
 * Defines the possible abi call signatures.
 */
export type MyCounterSignatures = keyof MyCounterTypes['methods']
/**
 * Defines the possible abi call signatures for methods that return a non-void value.
 */
export type MyCounterNonVoidMethodSignatures = keyof MyCounterTypes['methods'] extends infer T ? T extends keyof MyCounterTypes['methods'] ? MethodReturn<T> extends void ? never : T  : never : never
/**
 * Defines an object containing all relevant parameters for a single call to the contract.
 */
export type CallParams<TArgs> = Expand<
  Omit<AppClientMethodCallParams, 'method' | 'args' | 'onComplete'> &
    {
      /** The args for the ABI method call, either as an ordered array or an object */
      args: Expand<TArgs>
    }
>
/**
 * Maps a method signature from the MyCounter smart contract to the method's arguments in either tuple or struct form
 */
export type MethodArgs<TSignature extends MyCounterSignatures> = MyCounterTypes['methods'][TSignature]['argsObj' | 'argsTuple']
/**
 * Maps a method signature from the MyCounter smart contract to the method's return type
 */
export type MethodReturn<TSignature extends MyCounterSignatures> = MyCounterTypes['methods'][TSignature]['returns']

/**
 * Defines the shape of the keyed local state of the application.
 */
export type LocalKeysState = MyCounterTypes['state']['local']['keys']


/**
 * Defines supported create method params for this smart contract
 */
export type MyCounterCreateCallParams =
  | Expand<AppClientBareCallParams & {method?: never} & {onComplete?: OnApplicationComplete.NoOpOC} & CreateSchema>
/**
 * Defines arguments required for the deploy method.
 */
export type MyCounterDeployParams = Expand<Omit<AppFactoryDeployParams, 'createParams' | 'updateParams' | 'deleteParams'> & {
  /**
   * Create transaction parameters to use if a create needs to be issued as part of deployment; use `method` to define ABI call (if available) or leave out for a bare call (if available)
   */
  createParams?: MyCounterCreateCallParams
}>


/**
 * Exposes methods for constructing `AppClient` params objects for ABI calls to the MyCounter smart contract
 */
export abstract class MyCounterParamsFactory {
  /**
   * Gets available optIn ABI call param factories
   */
  static get optIn() {
    return {
      /**
       * Constructs opt-in ABI call params for the MyCounter smart contract using the optIn()void ABI method
       *
       * @param params Parameters for the call
       * @returns An `AppClientMethodCallParams` object for the call
       */
      optIn(params: CallParams<MyCounterArgs['obj']['optIn()void'] | MyCounterArgs['tuple']['optIn()void']>): AppClientMethodCallParams {
        return {
          ...params,
          method: 'optIn()void' as const,
          args: Array.isArray(params.args) ? params.args : [],
        }
      },
    }
  }

  /**
   * Constructs a no op call for the incrementMyCounter()uint64 ABI method
   *
   * Increment the counter for the sender and return its new value
   *
   * @param params Parameters for the call
   * @returns An `AppClientMethodCallParams` object for the call
   */
  static incrementMyCounter(params: CallParams<MyCounterArgs['obj']['incrementMyCounter()uint64'] | MyCounterArgs['tuple']['incrementMyCounter()uint64']> & CallOnComplete): AppClientMethodCallParams & CallOnComplete {
    return {
      ...params,
      method: 'incrementMyCounter()uint64' as const,
      args: Array.isArray(params.args) ? params.args : [],
    }
  }
}

/**
 * A factory to create and deploy one or more instance of the MyCounter smart contract and to create one or more app clients to interact with those (or other) app instances
 */
export class MyCounterFactory {
  /**
   * The underlying `AppFactory` for when you want to have more flexibility
   */
  public readonly appFactory: _AppFactory

  /**
   * Creates a new instance of `MyCounterFactory`
   *
   * @param params The parameters to initialise the app factory with
   */
  constructor(params: Omit<AppFactoryParams, 'appSpec'>) {
    this.appFactory = new _AppFactory({
      ...params,
      appSpec: APP_SPEC,
    })
  }
  
  /** The name of the app (from the ARC-32 / ARC-56 app spec or override). */
  public get appName() {
    return this.appFactory.appName
  }
  
  /** The ARC-56 app spec being used */
  get appSpec() {
    return APP_SPEC
  }
  
  /** A reference to the underlying `AlgorandClient` this app factory is using. */
  public get algorand(): AlgorandClientInterface {
    return this.appFactory.algorand
  }
  
  /**
   * Returns a new `AppClient` client for an app instance of the given ID.
   *
   * Automatically populates appName, defaultSender and source maps from the factory
   * if not specified in the params.
   * @param params The parameters to create the app client
   * @returns The `AppClient`
   */
  public getAppClientById(params: AppFactoryAppClientParams) {
    return new MyCounterClient(this.appFactory.getAppClientById(params))
  }
  
  /**
   * Returns a new `AppClient` client, resolving the app by creator address and name
   * using AlgoKit app deployment semantics (i.e. looking for the app creation transaction note).
   *
   * Automatically populates appName, defaultSender and source maps from the factory
   * if not specified in the params.
   * @param params The parameters to create the app client
   * @returns The `AppClient`
   */
  public async getAppClientByCreatorAndName(
    params: AppFactoryResolveAppClientByCreatorAndNameParams,
  ) {
    return new MyCounterClient(await this.appFactory.getAppClientByCreatorAndName(params))
  }

  /**
   * Idempotently deploys the MyCounter smart contract.
   *
   * @param params The arguments for the contract calls and any additional parameters for the call
   * @returns The deployment result
   */
  public async deploy(params: MyCounterDeployParams = {}) {
    const result = await this.appFactory.deploy({
      ...params,
    })
    return { result: result.result, appClient: new MyCounterClient(result.appClient) }
  }

  /**
   * Get parameters to create transactions (create and deploy related calls) for the current app. A good mental model for this is that these parameters represent a deferred transaction creation.
   */
  readonly params = {
    /**
     * Gets available create methods
     */
    create: {
      /**
       * Creates a new instance of the MyCounter smart contract using a bare call.
       *
       * @param params The params for the bare (raw) call
       * @returns The params for a create call
       */
      bare: (params?: Expand<AppClientBareCallParams & AppClientCompilationParams & CreateSchema & {onComplete?: OnApplicationComplete.NoOpOC}>) => {
        return this.appFactory.params.bare.create(params)
      },
    },

  }

  /**
   * Create transactions for the current app
   */
  readonly createTransaction = {
    /**
     * Gets available create methods
     */
    create: {
      /**
       * Creates a new instance of the MyCounter smart contract using a bare call.
       *
       * @param params The params for the bare (raw) call
       * @returns The transaction for a create call
       */
      bare: (params?: Expand<AppClientBareCallParams & AppClientCompilationParams & CreateSchema & {onComplete?: OnApplicationComplete.NoOpOC}>) => {
        return this.appFactory.createTransaction.bare.create(params)
      },
    },

  }

  /**
   * Send calls to the current app
   */
  readonly send = {
    /**
     * Gets available create methods
     */
    create: {
      /**
       * Creates a new instance of the MyCounter smart contract using a bare call.
       *
       * @param params The params for the bare (raw) call
       * @returns The create result
       */
      bare: async (params?: Expand<AppClientBareCallParams & AppClientCompilationParams & CreateSchema & SendParams & {onComplete?: OnApplicationComplete.NoOpOC}>) => {
        const result = await this.appFactory.send.bare.create(params)
        return { result: result.result, appClient: new MyCounterClient(result.appClient) }
      },
    },

  }

}
/**
 * A client to make calls to the MyCounter smart contract
 */
export class MyCounterClient {
  /**
   * The underlying `AppClient` for when you want to have more flexibility
   */
  public readonly appClient: _AppClient

  /**
   * Creates a new instance of `MyCounterClient`
   *
   * @param appClient An `AppClient` instance which has been created with the MyCounter app spec
   */
  constructor(appClient: _AppClient)
  /**
   * Creates a new instance of `MyCounterClient`
   *
   * @param params The parameters to initialise the app client with
   */
  constructor(params: Omit<AppClientParams, 'appSpec'>)
  constructor(appClientOrParams: _AppClient | Omit<AppClientParams, 'appSpec'>) {
    this.appClient = appClientOrParams instanceof _AppClient ? appClientOrParams : new _AppClient({
      ...appClientOrParams,
      appSpec: APP_SPEC,
    })
  }
  
  /**
   * Checks for decode errors on the given return value and maps the return value to the return type for the given method
   * @returns The typed return value or undefined if there was no value
   */
  decodeReturnValue<TSignature extends MyCounterNonVoidMethodSignatures>(method: TSignature, returnValue: ABIReturn | undefined) {
    return returnValue !== undefined ? getArc56ReturnValue<MethodReturn<TSignature>>(returnValue, this.appClient.getABIMethod(method), APP_SPEC.structs) : undefined
  }
  
  /**
   * Returns a new `MyCounterClient` client, resolving the app by creator address and name
   * using AlgoKit app deployment semantics (i.e. looking for the app creation transaction note).
   * @param params The parameters to create the app client
   */
  public static async fromCreatorAndName(params: Omit<ResolveAppClientByCreatorAndName, 'appSpec'>): Promise<MyCounterClient> {
    return new MyCounterClient(await _AppClient.fromCreatorAndName({...params, appSpec: APP_SPEC}))
  }
  
  /**
   * Returns an `MyCounterClient` instance for the current network based on
   * pre-determined network-specific app IDs specified in the ARC-56 app spec.
   *
   * If no IDs are in the app spec or the network isn't recognised, an error is thrown.
   * @param params The parameters to create the app client
   */
  static async fromNetwork(
    params: Omit<ResolveAppClientByNetwork, 'appSpec'>
  ): Promise<MyCounterClient> {
    return new MyCounterClient(await _AppClient.fromNetwork({...params, appSpec: APP_SPEC}))
  }
  
  /** The ID of the app instance this client is linked to. */
  public get appId() {
    return this.appClient.appId
  }
  
  /** The app address of the app instance this client is linked to. */
  public get appAddress() {
    return this.appClient.appAddress
  }
  
  /** The name of the app. */
  public get appName() {
    return this.appClient.appName
  }
  
  /** The ARC-56 app spec being used */
  public get appSpec() {
    return this.appClient.appSpec
  }
  
  /** A reference to the underlying `AlgorandClient` this app client is using. */
  public get algorand(): AlgorandClientInterface {
    return this.appClient.algorand
  }

  /**
   * Get parameters to create transactions for the current app. A good mental model for this is that these parameters represent a deferred transaction creation.
   */
  readonly params = {
    /**
     * Gets available optIn methods
     */
    optIn: {
      /**
       * Opts the user into an existing instance of the MyCounter smart contract using the `optIn()void` ABI method.
       *
       * Initialize the counter when an account opts in
       *
       * @param params The params for the smart contract call
       * @returns The optIn params
       */
      optIn: (params: CallParams<MyCounterArgs['obj']['optIn()void'] | MyCounterArgs['tuple']['optIn()void']> = {args: []}) => {
        return this.appClient.params.optIn(MyCounterParamsFactory.optIn.optIn(params))
      },

    },

    /**
     * Makes a clear_state call to an existing instance of the MyCounter smart contract.
     *
     * @param params The params for the bare (raw) call
     * @returns The clearState result
     */
    clearState: (params?: Expand<AppClientBareCallParams>) => {
      return this.appClient.params.bare.clearState(params)
    },

    /**
     * Makes a call to the MyCounter smart contract using the `incrementMyCounter()uint64` ABI method.
     *
     * Increment the counter for the sender and return its new value
     *
     * @param params The params for the smart contract call
     * @returns The call params: The new counter value
     */
    incrementMyCounter: (params: CallParams<MyCounterArgs['obj']['incrementMyCounter()uint64'] | MyCounterArgs['tuple']['incrementMyCounter()uint64']> & {onComplete?: OnApplicationComplete.NoOpOC} = {args: []}) => {
      return this.appClient.params.call(MyCounterParamsFactory.incrementMyCounter(params))
    },

  }

  /**
   * Create transactions for the current app
   */
  readonly createTransaction = {
    /**
     * Gets available optIn methods
     */
    optIn: {
      /**
       * Opts the user into an existing instance of the MyCounter smart contract using the `optIn()void` ABI method.
       *
       * Initialize the counter when an account opts in
       *
       * @param params The params for the smart contract call
       * @returns The optIn transaction
       */
      optIn: (params: CallParams<MyCounterArgs['obj']['optIn()void'] | MyCounterArgs['tuple']['optIn()void']> = {args: []}) => {
        return this.appClient.createTransaction.optIn(MyCounterParamsFactory.optIn.optIn(params))
      },

    },

    /**
     * Makes a clear_state call to an existing instance of the MyCounter smart contract.
     *
     * @param params The params for the bare (raw) call
     * @returns The clearState result
     */
    clearState: (params?: Expand<AppClientBareCallParams>) => {
      return this.appClient.createTransaction.bare.clearState(params)
    },

    /**
     * Makes a call to the MyCounter smart contract using the `incrementMyCounter()uint64` ABI method.
     *
     * Increment the counter for the sender and return its new value
     *
     * @param params The params for the smart contract call
     * @returns The call transaction: The new counter value
     */
    incrementMyCounter: (params: CallParams<MyCounterArgs['obj']['incrementMyCounter()uint64'] | MyCounterArgs['tuple']['incrementMyCounter()uint64']> & {onComplete?: OnApplicationComplete.NoOpOC} = {args: []}) => {
      return this.appClient.createTransaction.call(MyCounterParamsFactory.incrementMyCounter(params))
    },

  }

  /**
   * Send calls to the current app
   */
  readonly send = {
    /**
     * Gets available optIn methods
     */
    optIn: {
      /**
       * Opts the user into an existing instance of the MyCounter smart contract using the `optIn()void` ABI method.
       *
       * Initialize the counter when an account opts in
       *
       * @param params The params for the smart contract call
       * @returns The optIn result
       */
      optIn: async (params: CallParams<MyCounterArgs['obj']['optIn()void'] | MyCounterArgs['tuple']['optIn()void']> & SendParams = {args: []}) => {
        const result = await this.appClient.send.optIn(MyCounterParamsFactory.optIn.optIn(params))
        return {...result, return: result.return as unknown as (undefined | MyCounterReturns['optIn()void'])}
      },

    },

    /**
     * Makes a clear_state call to an existing instance of the MyCounter smart contract.
     *
     * @param params The params for the bare (raw) call
     * @returns The clearState result
     */
    clearState: (params?: Expand<AppClientBareCallParams & SendParams>) => {
      return this.appClient.send.bare.clearState(params)
    },

    /**
     * Makes a call to the MyCounter smart contract using the `incrementMyCounter()uint64` ABI method.
     *
     * Increment the counter for the sender and return its new value
     *
     * @param params The params for the smart contract call
     * @returns The call result: The new counter value
     */
    incrementMyCounter: async (params: CallParams<MyCounterArgs['obj']['incrementMyCounter()uint64'] | MyCounterArgs['tuple']['incrementMyCounter()uint64']> & SendParams & {onComplete?: OnApplicationComplete.NoOpOC} = {args: []}) => {
      const result = await this.appClient.send.call(MyCounterParamsFactory.incrementMyCounter(params))
      return {...result, return: result.return as unknown as (undefined | MyCounterReturns['incrementMyCounter()uint64'])}
    },

  }

  /**
   * Clone this app client with different params
   *
   * @param params The params to use for the the cloned app client. Omit a param to keep the original value. Set a param to override the original value. Setting to undefined will clear the original value.
   * @returns A new app client with the altered params
   */
  public clone(params: CloneAppClientParams) {
    return new MyCounterClient(this.appClient.clone(params))
  }

  /**
   * Methods to access state for the current MyCounter app
   */
  state = {
    /**
     * Methods to access local state for the current MyCounter app
     */
    local: (address: string | Address) => {
      const encodedAddress = typeof address === 'string' ? address : encodeAddress(address.publicKey)
      return {
        /**
         * Get all current keyed values from local state
         */
        getAll: async (): Promise<Partial<Expand<LocalKeysState>>> => {
          const result = await this.appClient.state.local(encodedAddress).getAll()
          return {
            myCounter: result.myCounter,
          }
        },
        /**
         * Get the current value of the myCounter key in local state
         */
        myCounter: async (): Promise<bigint | undefined> => { return (await this.appClient.state.local(encodedAddress).getValue("myCounter")) as bigint | undefined },
      }
    },
  }

  public newGroup(): MyCounterComposer {
    const client = this
    const composer = this.algorand.newGroup()
    let promiseChain:Promise<unknown> = Promise.resolve()
    const resultMappers: Array<undefined | ((x: ABIReturn | undefined) => any)> = []
    return {
      /**
       * Add a incrementMyCounter()uint64 method call against the MyCounter contract
       */
      incrementMyCounter(params: CallParams<MyCounterArgs['obj']['incrementMyCounter()uint64'] | MyCounterArgs['tuple']['incrementMyCounter()uint64']> & {onComplete?: OnApplicationComplete.NoOpOC}) {
        promiseChain = promiseChain.then(async () => composer.addAppCallMethodCall(await client.params.incrementMyCounter(params)))
        resultMappers.push((v) => client.decodeReturnValue('incrementMyCounter()uint64', v))
        return this
      },
      get optIn() {
        return {
          optIn: (params: CallParams<MyCounterArgs['obj']['optIn()void'] | MyCounterArgs['tuple']['optIn()void']>) => {
            promiseChain = promiseChain.then(async () => composer.addAppCallMethodCall(await client.params.optIn.optIn(params)))
            resultMappers.push(undefined)
            return this
          },
        }
      },
      /**
       * Add a clear state call to the MyCounter contract
       */
      clearState(params: AppClientBareCallParams) {
        promiseChain = promiseChain.then(() => composer.addAppCall(client.params.clearState(params)))
        return this
      },
      addTransaction(txn: Transaction, signer?: TransactionSigner) {
        promiseChain = promiseChain.then(() => composer.addTransaction(txn, signer))
        return this
      },
      async composer() {
        await promiseChain
        return composer
      },
      async simulate(options?: SimulateOptions) {
        await promiseChain
        const result = await (!options ? composer.simulate() : composer.simulate(options))
        return {
          ...result,
          returns: result.returns?.map((val, i) => resultMappers[i] !== undefined ? resultMappers[i]!(val) : val.returnValue)
        }
      },
      async send(params?: SendParams) {
        await promiseChain
        const result = await composer.send(params)
        return {
          ...result,
          returns: result.returns?.map((val, i) => resultMappers[i] !== undefined ? resultMappers[i]!(val) : val.returnValue)
        }
      }
    } as unknown as MyCounterComposer
  }
}
export type MyCounterComposer<TReturns extends [...any[]] = []> = {
  /**
   * Calls the incrementMyCounter()uint64 ABI method.
   *
   * Increment the counter for the sender and return its new value
   *
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The typed transaction composer so you can fluently chain multiple calls or call execute to execute all queued up transactions
   */
  incrementMyCounter(params?: CallParams<MyCounterArgs['obj']['incrementMyCounter()uint64'] | MyCounterArgs['tuple']['incrementMyCounter()uint64']>): MyCounterComposer<[...TReturns, MyCounterReturns['incrementMyCounter()uint64'] | undefined]>

  /**
   * Gets available optIn methods
   */
  readonly optIn: {
    /**
     * Opts the user into an existing instance of the MyCounter smart contract using the optIn()void ABI method.
     *
     * @param args The arguments for the smart contract call
     * @param params Any additional parameters for the call
     * @returns The typed transaction composer so you can fluently chain multiple calls or call execute to execute all queued up transactions
     */
    optIn(params?: CallParams<MyCounterArgs['obj']['optIn()void'] | MyCounterArgs['tuple']['optIn()void']>): MyCounterComposer<[...TReturns, MyCounterReturns['optIn()void'] | undefined]>
  }

  /**
   * Makes a clear_state call to an existing instance of the MyCounter smart contract.
   *
   * @param args The arguments for the bare call
   * @returns The typed transaction composer so you can fluently chain multiple calls or call execute to execute all queued up transactions
   */
  clearState(params?: AppClientBareCallParams): MyCounterComposer<[...TReturns, undefined]>

  /**
   * Adds a transaction to the composer
   *
   * @param txn A transaction to add to the transaction group
   * @param signer The optional signer to use when signing this transaction.
   */
  addTransaction(txn: Transaction, signer?: TransactionSigner): MyCounterComposer<TReturns>
  /**
   * Returns the underlying AtomicTransactionComposer instance
   */
  composer(): Promise<TransactionComposer>
  /**
   * Simulates the transaction group and returns the result
   */
  simulate(): Promise<MyCounterComposerResults<TReturns> & { simulateResponse: SimulateResponse }>
  simulate(options: SkipSignaturesSimulateOptions): Promise<MyCounterComposerResults<TReturns> & { simulateResponse: SimulateResponse }>
  simulate(options: RawSimulateOptions): Promise<MyCounterComposerResults<TReturns> & { simulateResponse: SimulateResponse }>
  /**
   * Sends the transaction group to the network and returns the results
   */
  send(params?: SendParams): Promise<MyCounterComposerResults<TReturns>>
}
export type MyCounterComposerResults<TReturns extends [...any[]]> = Expand<SendAtomicTransactionComposerResults & {
  returns: TReturns
}>

