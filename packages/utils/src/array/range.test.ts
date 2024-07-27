import { describe, expect, it } from 'vitest'
import { range } from './range'

describe('collection/array', () => {
  describe('range', () => {
    it('creates a new array based on arguments used to shape a range of values', () => {
      const arr = range(10, 100, 10, 'HELLO!')
      expect(arr).toHaveLength(10)
      expect(arr.toString()).toStrictEqual(
        'HELLO!,HELLO!,HELLO!,HELLO!,HELLO!,HELLO!,HELLO!,HELLO!,HELLO!,HELLO!',
      )
    })

    it('will create a new array of an exact length if only the first argument is passed', () => {
      const arr = range(12)
      expect(arr).toHaveLength(12)
      expect(arr[0]).toStrictEqual(0)
      expect(arr.at(-1)).toStrictEqual(11)
    })

    it('will create a numeric array with values starting at first arg and ending at second arg when second arg is another number', () => {
      const arr = range(0, 10)
      expect(arr).toHaveLength(11)
      expect(arr.at(-1)).toStrictEqual(10)
    })

    it('will create a numeric array that skips a number of indexes based on third arg, if second and third arg are both numbers', () => {
      const arr = range(5, 50, 2)
      expect(arr).toHaveLength(23)
      expect(arr[0]).toStrictEqual(5)
      expect(arr[10]).toStrictEqual(25)
      expect(arr.at(-1)).toStrictEqual(49)
    })
  })
})
