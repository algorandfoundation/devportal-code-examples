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

export const APP_SPEC: Arc56Contract = {"name":"HelloWorldContract","structs":{},"methods":[{"name":"sayHello","args":[{"type":"string","name":"firstName","desc":"The first name of the person to greet"},{"type":"string","name":"lastName","desc":"THe last name of the person to greet"}],"returns":{"type":"string","desc":"The string \"Hello {firstName} {lastName\"}"},"actions":{"create":[],"call":["NoOp"]},"readonly":false,"desc":"sayHello method","events":[],"recommendations":{}},{"name":"sayBananas","args":[],"returns":{"type":"string","desc":"The string \"Bananas\""},"actions":{"create":[],"call":["NoOp"]},"readonly":true,"desc":"sayBananas method","events":[],"recommendations":{}}],"arcs":[22,28],"desc":"A simple hello world example contract","networks":{},"state":{"schema":{"global":{"ints":0,"bytes":0},"local":{"ints":0,"bytes":0}},"keys":{"global":{},"local":{},"box":{}},"maps":{"global":{},"local":{},"box":{}}},"bareActions":{"create":["NoOp"],"call":[]},"sourceInfo":{"approval":{"sourceInfo":[{"pc":[33,59],"errorMessage":"OnCompletion is not NoOp"},{"pc":[106],"errorMessage":"can only call when creating"},{"pc":[36,62],"errorMessage":"can only call when not creating"}],"pcOffsetMethod":"none"},"clear":{"sourceInfo":[],"pcOffsetMethod":"none"}},"source":{"approval":"I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBAYWxnb3JhbmRmb3VuZGF0aW9uL2FsZ29yYW5kLXR5cGVzY3JpcHQvYXJjNC9pbmRleC5kLnRzOjpDb250cmFjdC5hcHByb3ZhbFByb2dyYW0oKSAtPiB1aW50NjQ6Cm1haW46CiAgICAvLyBIZWxsb1dvcmxkL2NvbnRyYWN0LmFsZ28udHM6MjAKICAgIC8vIGV4cG9ydCBkZWZhdWx0IGNsYXNzIEhlbGxvV29ybGRDb250cmFjdCBleHRlbmRzIEludGVybWVkaWF0ZSB7CiAgICB0eG4gTnVtQXBwQXJncwogICAgYnogbWFpbl9iYXJlX3JvdXRpbmdANwogICAgcHVzaGJ5dGVzcyAweDNhYWQ2ZDg2IDB4M2QyNWFlMzEgLy8gbWV0aG9kICJzYXlIZWxsbyhzdHJpbmcsc3RyaW5nKXN0cmluZyIsIG1ldGhvZCAic2F5QmFuYW5hcygpc3RyaW5nIgogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMAogICAgbWF0Y2ggbWFpbl9zYXlIZWxsb19yb3V0ZUAzIG1haW5fc2F5QmFuYW5hc19yb3V0ZUA0CgptYWluX2FmdGVyX2lmX2Vsc2VAMTE6CiAgICAvLyBIZWxsb1dvcmxkL2NvbnRyYWN0LmFsZ28udHM6MjAKICAgIC8vIGV4cG9ydCBkZWZhdWx0IGNsYXNzIEhlbGxvV29ybGRDb250cmFjdCBleHRlbmRzIEludGVybWVkaWF0ZSB7CiAgICBwdXNoaW50IDAgLy8gMAogICAgcmV0dXJuCgptYWluX3NheUJhbmFuYXNfcm91dGVANDoKICAgIC8vIEhlbGxvV29ybGQvY29udHJhY3QuYWxnby50czoxMQogICAgLy8gQGFyYzQuYWJpbWV0aG9kKHsgYWxsb3dBY3Rpb25zOiBbIk5vT3AiXSwgcmVhZG9ubHk6IHRydWUgfSkKICAgIHR4biBPbkNvbXBsZXRpb24KICAgICEKICAgIGFzc2VydCAvLyBPbkNvbXBsZXRpb24gaXMgbm90IE5vT3AKICAgIHR4biBBcHBsaWNhdGlvbklECiAgICBhc3NlcnQgLy8gY2FuIG9ubHkgY2FsbCB3aGVuIG5vdCBjcmVhdGluZwogICAgcHVzaGJ5dGVzIDB4MTUxZjdjNzUwMDA3NDI2MTZlNjE2ZTYxNzMKICAgIGxvZwogICAgcHVzaGludCAxIC8vIDEKICAgIHJldHVybgoKbWFpbl9zYXlIZWxsb19yb3V0ZUAzOgogICAgLy8gSGVsbG9Xb3JsZC9jb250cmFjdC5hbGdvLnRzOjI3CiAgICAvLyBwdWJsaWMgc2F5SGVsbG8oZmlyc3ROYW1lOiBzdHJpbmcsIGxhc3ROYW1lOiBzdHJpbmcpOiBzdHJpbmcgewogICAgdHhuIE9uQ29tcGxldGlvbgogICAgIQogICAgYXNzZXJ0IC8vIE9uQ29tcGxldGlvbiBpcyBub3QgTm9PcAogICAgdHhuIEFwcGxpY2F0aW9uSUQKICAgIGFzc2VydCAvLyBjYW4gb25seSBjYWxsIHdoZW4gbm90IGNyZWF0aW5nCiAgICAvLyBIZWxsb1dvcmxkL2NvbnRyYWN0LmFsZ28udHM6MjAKICAgIC8vIGV4cG9ydCBkZWZhdWx0IGNsYXNzIEhlbGxvV29ybGRDb250cmFjdCBleHRlbmRzIEludGVybWVkaWF0ZSB7CiAgICB0eG5hIEFwcGxpY2F0aW9uQXJncyAxCiAgICBleHRyYWN0IDIgMAogICAgdHhuYSBBcHBsaWNhdGlvbkFyZ3MgMgogICAgZXh0cmFjdCAyIDAKICAgIC8vIEhlbGxvV29ybGQvY29udHJhY3QuYWxnby50czoyNwogICAgLy8gcHVibGljIHNheUhlbGxvKGZpcnN0TmFtZTogc3RyaW5nLCBsYXN0TmFtZTogc3RyaW5nKTogc3RyaW5nIHsKICAgIGNhbGxzdWIgc2F5SGVsbG8KICAgIGR1cAogICAgbGVuCiAgICBpdG9iCiAgICBleHRyYWN0IDYgMgogICAgc3dhcAogICAgY29uY2F0CiAgICBwdXNoYnl0ZXMgMHgxNTFmN2M3NQogICAgc3dhcAogICAgY29uY2F0CiAgICBsb2cKICAgIHB1c2hpbnQgMSAvLyAxCiAgICByZXR1cm4KCm1haW5fYmFyZV9yb3V0aW5nQDc6CiAgICAvLyBIZWxsb1dvcmxkL2NvbnRyYWN0LmFsZ28udHM6MjAKICAgIC8vIGV4cG9ydCBkZWZhdWx0IGNsYXNzIEhlbGxvV29ybGRDb250cmFjdCBleHRlbmRzIEludGVybWVkaWF0ZSB7CiAgICB0eG4gT25Db21wbGV0aW9uCiAgICBibnogbWFpbl9hZnRlcl9pZl9lbHNlQDExCiAgICB0eG4gQXBwbGljYXRpb25JRAogICAgIQogICAgYXNzZXJ0IC8vIGNhbiBvbmx5IGNhbGwgd2hlbiBjcmVhdGluZwogICAgcHVzaGludCAxIC8vIDEKICAgIHJldHVybgoKCi8vIEhlbGxvV29ybGQvY29udHJhY3QuYWxnby50czo6SGVsbG9Xb3JsZENvbnRyYWN0LnNheUhlbGxvKGZpcnN0TmFtZTogYnl0ZXMsIGxhc3ROYW1lOiBieXRlcykgLT4gYnl0ZXM6CnNheUhlbGxvOgogICAgLy8gSGVsbG9Xb3JsZC9jb250cmFjdC5hbGdvLnRzOjI3CiAgICAvLyBwdWJsaWMgc2F5SGVsbG8oZmlyc3ROYW1lOiBzdHJpbmcsIGxhc3ROYW1lOiBzdHJpbmcpOiBzdHJpbmcgewogICAgcHJvdG8gMiAxCiAgICAvLyBIZWxsb1dvcmxkL2NvbnRyYWN0LmFsZ28udHM6MjgKICAgIC8vIGNvbnN0IHJlc3VsdCA9IGBIZWxsbyAke2ZpcnN0TmFtZX0gJHtsYXN0TmFtZX1gOwogICAgcHVzaGJ5dGVzICJIZWxsbyAiCiAgICBmcmFtZV9kaWcgLTIKICAgIGNvbmNhdAogICAgcHVzaGJ5dGVzICIgIgogICAgY29uY2F0CiAgICBmcmFtZV9kaWcgLTEKICAgIGNvbmNhdAogICAgLy8gSGVsbG9Xb3JsZC9jb250cmFjdC5hbGdvLnRzOjI5CiAgICAvLyByZXR1cm4gcmVzdWx0OwogICAgcmV0c3ViCg==","clear":"I3ByYWdtYSB2ZXJzaW9uIDEwCiNwcmFnbWEgdHlwZXRyYWNrIGZhbHNlCgovLyBAYWxnb3JhbmRmb3VuZGF0aW9uL2FsZ29yYW5kLXR5cGVzY3JpcHQvYmFzZS1jb250cmFjdC5kLnRzOjpCYXNlQ29udHJhY3QuY2xlYXJTdGF0ZVByb2dyYW0oKSAtPiB1aW50NjQ6Cm1haW46CiAgICBwdXNoaW50IDEgLy8gMQogICAgcmV0dXJuCg=="},"byteCode":{"approval":"CjEbQQBcggIEOq1thgQ9Ja4xNhoAjgIAHQADgQBDMRkURDEYRIANFR98dQAHQmFuYW5hc7CBAUMxGRREMRhENhoBVwIANhoCVwIAiAAgSRUWVwYCTFCABBUffHVMULCBAUMxGUD/tDEYFESBAUOKAgGABkhlbGxvIIv+UIABIFCL/1CJ","clear":"CoEBQw=="},"compilerInfo":{"compiler":"puya","compilerVersion":{"major":4,"minor":2,"patch":1}},"events":[],"templateVariables":{}} as unknown as Arc56Contract

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
 * The argument types for the HelloWorldContract contract
 */
export type HelloWorldContractArgs = {
  /**
   * The object representation of the arguments for each method
   */
  obj: {
    'sayHello(string,string)string': {
      /**
       * The first name of the person to greet
       */
      firstName: string
      /**
       * THe last name of the person to greet
       */
      lastName: string
    }
    'sayBananas()string': Record<string, never>
  }
  /**
   * The tuple representation of the arguments for each method
   */
  tuple: {
    'sayHello(string,string)string': [firstName: string, lastName: string]
    'sayBananas()string': []
  }
}

/**
 * The return type for each method
 */
export type HelloWorldContractReturns = {
  'sayHello(string,string)string': string
  'sayBananas()string': string
}

/**
 * Defines the types of available calls and state of the HelloWorldContract smart contract.
 */
export type HelloWorldContractTypes = {
  /**
   * Maps method signatures / names to their argument and return types.
   */
  methods:
    & Record<'sayHello(string,string)string' | 'sayHello', {
      argsObj: HelloWorldContractArgs['obj']['sayHello(string,string)string']
      argsTuple: HelloWorldContractArgs['tuple']['sayHello(string,string)string']
      /**
       * The string "Hello {firstName} {lastName"}
       */
      returns: HelloWorldContractReturns['sayHello(string,string)string']
    }>
    & Record<'sayBananas()string' | 'sayBananas', {
      argsObj: HelloWorldContractArgs['obj']['sayBananas()string']
      argsTuple: HelloWorldContractArgs['tuple']['sayBananas()string']
      /**
       * The string "Bananas"
       */
      returns: HelloWorldContractReturns['sayBananas()string']
    }>
}

/**
 * Defines the possible abi call signatures.
 */
export type HelloWorldContractSignatures = keyof HelloWorldContractTypes['methods']
/**
 * Defines the possible abi call signatures for methods that return a non-void value.
 */
export type HelloWorldContractNonVoidMethodSignatures = keyof HelloWorldContractTypes['methods'] extends infer T ? T extends keyof HelloWorldContractTypes['methods'] ? MethodReturn<T> extends void ? never : T  : never : never
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
 * Maps a method signature from the HelloWorldContract smart contract to the method's arguments in either tuple or struct form
 */
export type MethodArgs<TSignature extends HelloWorldContractSignatures> = HelloWorldContractTypes['methods'][TSignature]['argsObj' | 'argsTuple']
/**
 * Maps a method signature from the HelloWorldContract smart contract to the method's return type
 */
export type MethodReturn<TSignature extends HelloWorldContractSignatures> = HelloWorldContractTypes['methods'][TSignature]['returns']


/**
 * Defines supported create method params for this smart contract
 */
export type HelloWorldContractCreateCallParams =
  | Expand<AppClientBareCallParams & {method?: never} & {onComplete?: OnApplicationComplete.NoOpOC} & CreateSchema>
/**
 * Defines arguments required for the deploy method.
 */
export type HelloWorldContractDeployParams = Expand<Omit<AppFactoryDeployParams, 'createParams' | 'updateParams' | 'deleteParams'> & {
  /**
   * Create transaction parameters to use if a create needs to be issued as part of deployment; use `method` to define ABI call (if available) or leave out for a bare call (if available)
   */
  createParams?: HelloWorldContractCreateCallParams
}>


/**
 * Exposes methods for constructing `AppClient` params objects for ABI calls to the HelloWorldContract smart contract
 */
export abstract class HelloWorldContractParamsFactory {
  /**
   * Constructs a no op call for the sayHello(string,string)string ABI method
   *
   * sayHello method
   *
   * @param params Parameters for the call
   * @returns An `AppClientMethodCallParams` object for the call
   */
  static sayHello(params: CallParams<HelloWorldContractArgs['obj']['sayHello(string,string)string'] | HelloWorldContractArgs['tuple']['sayHello(string,string)string']> & CallOnComplete): AppClientMethodCallParams & CallOnComplete {
    return {
      ...params,
      method: 'sayHello(string,string)string' as const,
      args: Array.isArray(params.args) ? params.args : [params.args.firstName, params.args.lastName],
    }
  }
  /**
   * Constructs a no op call for the sayBananas()string ABI method
   *
   * sayBananas method
   *
   * @param params Parameters for the call
   * @returns An `AppClientMethodCallParams` object for the call
   */
  static sayBananas(params: CallParams<HelloWorldContractArgs['obj']['sayBananas()string'] | HelloWorldContractArgs['tuple']['sayBananas()string']> & CallOnComplete): AppClientMethodCallParams & CallOnComplete {
    return {
      ...params,
      method: 'sayBananas()string' as const,
      args: Array.isArray(params.args) ? params.args : [],
    }
  }
}

/**
 * A factory to create and deploy one or more instance of the HelloWorldContract smart contract and to create one or more app clients to interact with those (or other) app instances
 */
export class HelloWorldContractFactory {
  /**
   * The underlying `AppFactory` for when you want to have more flexibility
   */
  public readonly appFactory: _AppFactory

  /**
   * Creates a new instance of `HelloWorldContractFactory`
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
    return new HelloWorldContractClient(this.appFactory.getAppClientById(params))
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
    return new HelloWorldContractClient(await this.appFactory.getAppClientByCreatorAndName(params))
  }

  /**
   * Idempotently deploys the HelloWorldContract smart contract.
   *
   * @param params The arguments for the contract calls and any additional parameters for the call
   * @returns The deployment result
   */
  public async deploy(params: HelloWorldContractDeployParams = {}) {
    const result = await this.appFactory.deploy({
      ...params,
    })
    return { result: result.result, appClient: new HelloWorldContractClient(result.appClient) }
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
       * Creates a new instance of the HelloWorldContract smart contract using a bare call.
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
       * Creates a new instance of the HelloWorldContract smart contract using a bare call.
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
       * Creates a new instance of the HelloWorldContract smart contract using a bare call.
       *
       * @param params The params for the bare (raw) call
       * @returns The create result
       */
      bare: async (params?: Expand<AppClientBareCallParams & AppClientCompilationParams & CreateSchema & SendParams & {onComplete?: OnApplicationComplete.NoOpOC}>) => {
        const result = await this.appFactory.send.bare.create(params)
        return { result: result.result, appClient: new HelloWorldContractClient(result.appClient) }
      },
    },

  }

}
/**
 * A client to make calls to the HelloWorldContract smart contract
 */
export class HelloWorldContractClient {
  /**
   * The underlying `AppClient` for when you want to have more flexibility
   */
  public readonly appClient: _AppClient

  /**
   * Creates a new instance of `HelloWorldContractClient`
   *
   * @param appClient An `AppClient` instance which has been created with the HelloWorldContract app spec
   */
  constructor(appClient: _AppClient)
  /**
   * Creates a new instance of `HelloWorldContractClient`
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
  decodeReturnValue<TSignature extends HelloWorldContractNonVoidMethodSignatures>(method: TSignature, returnValue: ABIReturn | undefined) {
    return returnValue !== undefined ? getArc56ReturnValue<MethodReturn<TSignature>>(returnValue, this.appClient.getABIMethod(method), APP_SPEC.structs) : undefined
  }
  
  /**
   * Returns a new `HelloWorldContractClient` client, resolving the app by creator address and name
   * using AlgoKit app deployment semantics (i.e. looking for the app creation transaction note).
   * @param params The parameters to create the app client
   */
  public static async fromCreatorAndName(params: Omit<ResolveAppClientByCreatorAndName, 'appSpec'>): Promise<HelloWorldContractClient> {
    return new HelloWorldContractClient(await _AppClient.fromCreatorAndName({...params, appSpec: APP_SPEC}))
  }
  
  /**
   * Returns an `HelloWorldContractClient` instance for the current network based on
   * pre-determined network-specific app IDs specified in the ARC-56 app spec.
   *
   * If no IDs are in the app spec or the network isn't recognised, an error is thrown.
   * @param params The parameters to create the app client
   */
  static async fromNetwork(
    params: Omit<ResolveAppClientByNetwork, 'appSpec'>
  ): Promise<HelloWorldContractClient> {
    return new HelloWorldContractClient(await _AppClient.fromNetwork({...params, appSpec: APP_SPEC}))
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
     * Makes a clear_state call to an existing instance of the HelloWorldContract smart contract.
     *
     * @param params The params for the bare (raw) call
     * @returns The clearState result
     */
    clearState: (params?: Expand<AppClientBareCallParams>) => {
      return this.appClient.params.bare.clearState(params)
    },

    /**
     * Makes a call to the HelloWorldContract smart contract using the `sayHello(string,string)string` ABI method.
     *
     * sayHello method
     *
     * @param params The params for the smart contract call
     * @returns The call params: The string "Hello {firstName} {lastName"}
     */
    sayHello: (params: CallParams<HelloWorldContractArgs['obj']['sayHello(string,string)string'] | HelloWorldContractArgs['tuple']['sayHello(string,string)string']> & {onComplete?: OnApplicationComplete.NoOpOC}) => {
      return this.appClient.params.call(HelloWorldContractParamsFactory.sayHello(params))
    },

    /**
     * Makes a call to the HelloWorldContract smart contract using the `sayBananas()string` ABI method.
     * 
     * This method is a readonly method; calling it with onComplete of NoOp will result in a simulated transaction rather than a real transaction.
     *
     * sayBananas method
     *
     * @param params The params for the smart contract call
     * @returns The call params: The string "Bananas"
     */
    sayBananas: (params: CallParams<HelloWorldContractArgs['obj']['sayBananas()string'] | HelloWorldContractArgs['tuple']['sayBananas()string']> & {onComplete?: OnApplicationComplete.NoOpOC} = {args: []}) => {
      return this.appClient.params.call(HelloWorldContractParamsFactory.sayBananas(params))
    },

  }

  /**
   * Create transactions for the current app
   */
  readonly createTransaction = {
    /**
     * Makes a clear_state call to an existing instance of the HelloWorldContract smart contract.
     *
     * @param params The params for the bare (raw) call
     * @returns The clearState result
     */
    clearState: (params?: Expand<AppClientBareCallParams>) => {
      return this.appClient.createTransaction.bare.clearState(params)
    },

    /**
     * Makes a call to the HelloWorldContract smart contract using the `sayHello(string,string)string` ABI method.
     *
     * sayHello method
     *
     * @param params The params for the smart contract call
     * @returns The call transaction: The string "Hello {firstName} {lastName"}
     */
    sayHello: (params: CallParams<HelloWorldContractArgs['obj']['sayHello(string,string)string'] | HelloWorldContractArgs['tuple']['sayHello(string,string)string']> & {onComplete?: OnApplicationComplete.NoOpOC}) => {
      return this.appClient.createTransaction.call(HelloWorldContractParamsFactory.sayHello(params))
    },

    /**
     * Makes a call to the HelloWorldContract smart contract using the `sayBananas()string` ABI method.
     * 
     * This method is a readonly method; calling it with onComplete of NoOp will result in a simulated transaction rather than a real transaction.
     *
     * sayBananas method
     *
     * @param params The params for the smart contract call
     * @returns The call transaction: The string "Bananas"
     */
    sayBananas: (params: CallParams<HelloWorldContractArgs['obj']['sayBananas()string'] | HelloWorldContractArgs['tuple']['sayBananas()string']> & {onComplete?: OnApplicationComplete.NoOpOC} = {args: []}) => {
      return this.appClient.createTransaction.call(HelloWorldContractParamsFactory.sayBananas(params))
    },

  }

  /**
   * Send calls to the current app
   */
  readonly send = {
    /**
     * Makes a clear_state call to an existing instance of the HelloWorldContract smart contract.
     *
     * @param params The params for the bare (raw) call
     * @returns The clearState result
     */
    clearState: (params?: Expand<AppClientBareCallParams & SendParams>) => {
      return this.appClient.send.bare.clearState(params)
    },

    /**
     * Makes a call to the HelloWorldContract smart contract using the `sayHello(string,string)string` ABI method.
     *
     * sayHello method
     *
     * @param params The params for the smart contract call
     * @returns The call result: The string "Hello {firstName} {lastName"}
     */
    sayHello: async (params: CallParams<HelloWorldContractArgs['obj']['sayHello(string,string)string'] | HelloWorldContractArgs['tuple']['sayHello(string,string)string']> & SendParams & {onComplete?: OnApplicationComplete.NoOpOC}) => {
      const result = await this.appClient.send.call(HelloWorldContractParamsFactory.sayHello(params))
      return {...result, return: result.return as unknown as (undefined | HelloWorldContractReturns['sayHello(string,string)string'])}
    },

    /**
     * Makes a call to the HelloWorldContract smart contract using the `sayBananas()string` ABI method.
     * 
     * This method is a readonly method; calling it with onComplete of NoOp will result in a simulated transaction rather than a real transaction.
     *
     * sayBananas method
     *
     * @param params The params for the smart contract call
     * @returns The call result: The string "Bananas"
     */
    sayBananas: async (params: CallParams<HelloWorldContractArgs['obj']['sayBananas()string'] | HelloWorldContractArgs['tuple']['sayBananas()string']> & SendParams & {onComplete?: OnApplicationComplete.NoOpOC} = {args: []}) => {
      const result = await this.appClient.send.call(HelloWorldContractParamsFactory.sayBananas(params))
      return {...result, return: result.return as unknown as (undefined | HelloWorldContractReturns['sayBananas()string'])}
    },

  }

  /**
   * Clone this app client with different params
   *
   * @param params The params to use for the the cloned app client. Omit a param to keep the original value. Set a param to override the original value. Setting to undefined will clear the original value.
   * @returns A new app client with the altered params
   */
  public clone(params: CloneAppClientParams) {
    return new HelloWorldContractClient(this.appClient.clone(params))
  }

  /**
   * Makes a readonly (simulated) call to the HelloWorldContract smart contract using the `sayBananas()string` ABI method.
   * 
   * This method is a readonly method; calling it with onComplete of NoOp will result in a simulated transaction rather than a real transaction.
   *
   * sayBananas method
   *
   * @param params The params for the smart contract call
   * @returns The call result: The string "Bananas"
   */
  async sayBananas(params: CallParams<HelloWorldContractArgs['obj']['sayBananas()string'] | HelloWorldContractArgs['tuple']['sayBananas()string']> = {args: []}) {
    const result = await this.appClient.send.call(HelloWorldContractParamsFactory.sayBananas(params))
    return result.return as unknown as HelloWorldContractReturns['sayBananas()string']
  }

  /**
   * Methods to access state for the current HelloWorldContract app
   */
  state = {
  }

  public newGroup(): HelloWorldContractComposer {
    const client = this
    const composer = this.algorand.newGroup()
    let promiseChain:Promise<unknown> = Promise.resolve()
    const resultMappers: Array<undefined | ((x: ABIReturn | undefined) => any)> = []
    return {
      /**
       * Add a sayHello(string,string)string method call against the HelloWorldContract contract
       */
      sayHello(params: CallParams<HelloWorldContractArgs['obj']['sayHello(string,string)string'] | HelloWorldContractArgs['tuple']['sayHello(string,string)string']> & {onComplete?: OnApplicationComplete.NoOpOC}) {
        promiseChain = promiseChain.then(async () => composer.addAppCallMethodCall(await client.params.sayHello(params)))
        resultMappers.push((v) => client.decodeReturnValue('sayHello(string,string)string', v))
        return this
      },
      /**
       * Add a sayBananas()string method call against the HelloWorldContract contract
       */
      sayBananas(params: CallParams<HelloWorldContractArgs['obj']['sayBananas()string'] | HelloWorldContractArgs['tuple']['sayBananas()string']> & {onComplete?: OnApplicationComplete.NoOpOC}) {
        promiseChain = promiseChain.then(async () => composer.addAppCallMethodCall(await client.params.sayBananas(params)))
        resultMappers.push((v) => client.decodeReturnValue('sayBananas()string', v))
        return this
      },
      /**
       * Add a clear state call to the HelloWorldContract contract
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
    } as unknown as HelloWorldContractComposer
  }
}
export type HelloWorldContractComposer<TReturns extends [...any[]] = []> = {
  /**
   * Calls the sayHello(string,string)string ABI method.
   *
   * sayHello method
   *
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The typed transaction composer so you can fluently chain multiple calls or call execute to execute all queued up transactions
   */
  sayHello(params?: CallParams<HelloWorldContractArgs['obj']['sayHello(string,string)string'] | HelloWorldContractArgs['tuple']['sayHello(string,string)string']>): HelloWorldContractComposer<[...TReturns, HelloWorldContractReturns['sayHello(string,string)string'] | undefined]>

  /**
   * Calls the sayBananas()string ABI method.
   *
   * sayBananas method
   *
   * @param args The arguments for the contract call
   * @param params Any additional parameters for the call
   * @returns The typed transaction composer so you can fluently chain multiple calls or call execute to execute all queued up transactions
   */
  sayBananas(params?: CallParams<HelloWorldContractArgs['obj']['sayBananas()string'] | HelloWorldContractArgs['tuple']['sayBananas()string']>): HelloWorldContractComposer<[...TReturns, HelloWorldContractReturns['sayBananas()string'] | undefined]>

  /**
   * Makes a clear_state call to an existing instance of the HelloWorldContract smart contract.
   *
   * @param args The arguments for the bare call
   * @returns The typed transaction composer so you can fluently chain multiple calls or call execute to execute all queued up transactions
   */
  clearState(params?: AppClientBareCallParams): HelloWorldContractComposer<[...TReturns, undefined]>

  /**
   * Adds a transaction to the composer
   *
   * @param txn A transaction to add to the transaction group
   * @param signer The optional signer to use when signing this transaction.
   */
  addTransaction(txn: Transaction, signer?: TransactionSigner): HelloWorldContractComposer<TReturns>
  /**
   * Returns the underlying AtomicTransactionComposer instance
   */
  composer(): TransactionComposer
  /**
   * Simulates the transaction group and returns the result
   */
  simulate(): Promise<HelloWorldContractComposerResults<TReturns> & { simulateResponse: SimulateResponse }>
  simulate(options: SkipSignaturesSimulateOptions): Promise<HelloWorldContractComposerResults<TReturns> & { simulateResponse: SimulateResponse }>
  simulate(options: RawSimulateOptions): Promise<HelloWorldContractComposerResults<TReturns> & { simulateResponse: SimulateResponse }>
  /**
   * Sends the transaction group to the network and returns the results
   */
  send(params?: SendParams): Promise<HelloWorldContractComposerResults<TReturns>>
}
export type HelloWorldContractComposerResults<TReturns extends [...any[]]> = Expand<SendAtomicTransactionComposerResults & {
  returns: TReturns
}>

