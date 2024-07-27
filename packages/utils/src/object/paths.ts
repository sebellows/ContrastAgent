export const SKIP_JS_BUILTINS = new Set([
  '__proto__',
  'constructor',
  'prototype',
])

export function toPathArray(path: string | readonly string[]) {
  return typeof path === 'string' ? path.split('.') : path
}
