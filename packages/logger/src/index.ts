const state = new Map<string, boolean>()

/**
 * Exectutes the given function only once for the given key.
 */
function once(cb: () => void, key: string) {
  if (state.has(key)) return

  state.set(key, true)

  cb()
}

once.clear = () => state.clear()

class Logger {
  static _instance: Logger

  static getInstance() {
    if (!Logger._instance) {
      Logger._instance = new Logger(this.name)
    }

    return Logger._instance
  }

  readonly name: string

  constructor(context: string) {
    this.name = context
  }

  static log(...logContent: any[]) {
    console.log(...logContent)
  }

  static warn(message: string, ...logContent: any[]) {
    console.warn(`AG Charts - ${message}`, ...logContent)
  }

  static error(message: any, ...logContent: any[]) {
    if (typeof message === 'object') {
      console.error(`${Logger.name} error`, message, ...logContent)
    } else {
      console.error(`${Logger.name} - ${message}`, ...logContent)
    }
  }

  static table(...logContent: any[]) {
    console.table(...logContent)
  }

  static warnOnce(message: any, ...logContent: any[]) {
    once(() => Logger.warn(message, ...logContent), `Logger.warn: ${message}`)
  }

  static errorOnce(message: any, ...logContent: any[]) {
    once(() => Logger.error(message, ...logContent), `Logger.error: ${message}`)
  }
}

export const createLogger = (context: string) => new Logger(context)
