import { v4 as uuid } from 'uuid'

export const useId = (id?: string) => {
  const uid = id ?? uuid()

  return uid
}
