export function isNumberKey(
  eventOrKeyCode: KeyboardEvent | string,
  { includeNumpad = false } = {},
): boolean {
  const code =
    typeof eventOrKeyCode === 'string' ? eventOrKeyCode : eventOrKeyCode.code

  const withNumpad = includeNumpad
    ? isNumPadKey(code, { includeNonNumericCodes: false })
    : false

  return /^Digit\d$/.test(code) || withNumpad
}

const nonNumericNumpadKeys = [
  'NumpadAdd',
  'NumpadSubtract',
  'NumpadMultiply',
  'NumpadDivide',
  'NumpadDecimal',
]

export function isNumPadKey(
  eventOrKeyCode: KeyboardEvent | string,
  { includeNonNumericCodes = true } = {},
): boolean {
  const code =
    typeof eventOrKeyCode === 'string' ? eventOrKeyCode : eventOrKeyCode.code

  return (
    /^Numpad\d$/.test(code) ||
    (includeNonNumericCodes && nonNumericNumpadKeys.includes(code))
  )
}

export function isLetterKey(eventOrKeyCode: KeyboardEvent | string): boolean {
  const code =
    typeof eventOrKeyCode === 'string' ? eventOrKeyCode : eventOrKeyCode.code

  return /^Key[A-Z]$/.test(code)
}

export function isPrintableKeyCode(
  eventOrKeyCode: KeyboardEvent | string,
): boolean {
  const code =
    typeof eventOrKeyCode === 'string' ? eventOrKeyCode : eventOrKeyCode.code

  return (
    isNumberKey(code) ||
    code === 'Space' ||
    code === 'Backspace' ||
    isLetterKey(code) ||
    isNumPadKey(code) ||
    [
      'Minus',
      'Equal',
      'BracketLeft',
      'BracketRight',
      'Semicolon',
      'Quote',
      'Backquote',
      'Backslash',
      'Forwardslash',
      'Comma',
      'Period',
      'Slash',
    ].includes(code)
  )
}
