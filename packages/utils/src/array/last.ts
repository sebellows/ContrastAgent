import { isString } from '../assert'

export function last(value: any) {
  if ((Array.isArray(value) || isString(value)) && value.length > 0) {
    return value[value.length - 1]
  }

  return undefined
}
