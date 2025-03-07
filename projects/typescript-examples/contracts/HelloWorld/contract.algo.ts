import { Contract } from '@algorandfoundation/algorand-typescript'

/**
 * An abstract base class for a simple example contract
 */
abstract class Intermediate extends Contract {
  /**
   * sayBananas method
   * @returns The string "Bananas"
   */
  public sayBananas(): string {
    return `Bananas`
  }
}

/**
 * A simple hello world example contract
 */
export default class HelloWorld extends Intermediate {
  /**
   * sayHello method
   * @param firstName The first name of the person to greet
   * @param lastName THe last name of the person to greet
   * @returns The string "Hello {firstName} {lastName"}
   */
  public sayHello(firstName: string, lastName: string): string {
    const result = `Hello ${firstName} ${lastName}`
    return result
  }
}
