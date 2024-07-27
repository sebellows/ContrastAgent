interface DebounceOptions {
  leading?: boolean
  trailing?: boolean
  maxWait?: number
  timeoutMs?: number
}

const DEFAULT_DELAY = 500

export function debounce<T extends (...args: Parameters<T>) => void>(
  callback: T,
  options: DebounceOptions = {},
) {
  const {
    timeoutMs = DEFAULT_DELAY,
    leading = false,
    trailing = true,
    maxWait = Infinity,
  } = options ?? {}

  let timerId: NodeJS.Timeout | number
  let startTime: number | null

  if (maxWait < timeoutMs) {
    throw new Error('Value of maxWait cannot be lower than timeoutMs.')
  }

  function debounceCallback(...args: Parameters<T>) {
    if (leading && !startTime) {
      startTime = Date.now()
      timerId = setTimeout(() => (startTime = null), timeoutMs)
      callback(...args)
      return
    }

    let adjustedWaitMs = timeoutMs
    if (maxWait !== Infinity && startTime) {
      const elapsedTime = Date.now() - startTime
      if (timeoutMs > maxWait - elapsedTime) {
        adjustedWaitMs = maxWait - elapsedTime
      }
    }

    clearTimeout(timerId)

    startTime ??= Date.now()
    timerId = setTimeout(() => {
      startTime = null
      if (trailing) {
        callback(...args)
      }
    }, adjustedWaitMs)
  }

  return Object.assign(debounceCallback, {
    cancel() {
      clearTimeout(timerId)
      startTime = null
    },
  })
}
