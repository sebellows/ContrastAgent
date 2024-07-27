/**
 * Taken from 'tiny-warning' package by [Alex Reardon](https://github.com/alexreardon)
 * @see {@link https://github.com/alexreardon/tiny-warning/}
 *
 * @description
 * Supports passing in arguments to the warning function in a sprintf style (condition, format, a, b,
 * c, d, e, f). It has internal logic to execute the sprintf substitutions. tiny-warning has dropped
 * all of the sprintf logic. tiny-warning allows you to pass a single string message. With template
 * literals there is really no need for a custom message formatter to be built into the library.
 * If you need a multi part message you can just do this: warning(condition, 'Hello, ${name} -
 * how are you today?')
 */
const isProduction: boolean = process.env.NODE_ENV === 'production'

export function warning(condition: any, message: string): void {
  // don't do anything in production
  // wrapping in production check for better dead code elimination
  if (!isProduction) {
    // condition passed: do not log
    if (condition) {
      return
    }

    // Condition not passed
    const text: string = `Warning: ${message}`

    // check console for IE9 support which provides console
    // only with open devtools
    if (typeof console !== 'undefined') {
      console.warn(text)
    }

    // Throwing an error and catching it immediately
    // to improve debugging
    // A consumer can use 'pause on caught exceptions'
    // https://github.com/facebook/react/issues/4216
    try {
      throw Error(text)
    } catch (x) {}
  }
}
