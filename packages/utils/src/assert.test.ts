import { describe, expect, it } from 'vitest'
import {
  is,
  isEmpty,
  isEmptyString,
  isNil,
  isNumeric,
  isNumericString,
  isPlainObject,
  isPositiveNumericString,
  lengthLessThan,
  lengthMoreThan,
  notEmpty,
  notEmptyString,
  notNumericString,
} from './assert'

describe('collection/assert', () => {
  describe('is', () => {
    it('returns the type of an object in lowercase format', () => {
      expect(is({ id: 5, foo: 'bar' }, 'object')).toStrictEqual('object')
    })

    it('returns the type of a symbol in lowercase format', () => {
      expect(is(Symbol.for('__TEST__'), 'symbol')).toStrictEqual('symbol')
    })
  })

  describe('isPlainObject', () => {
    it('returns TRUE if the passed argument is a plain object', () => {
      expect(isPlainObject({})).toBe(true)
    })

    it('returns FALSE if an array is passed', () => {
      expect(isPlainObject([1, 2, 3])).toBe(false)
    })

    it('returns FALSE if NULL is passed', () => {
      expect(isPlainObject(null)).toBe(false)
    })
  })

  describe('isNil', () => {
    it('returns TRUE if the passed argument is undefined', () => {
      expect(isNil(undefined)).toBe(true)
    })

    it('returns TRUE if the passed argument is null', () => {
      expect(isNil(null)).toBe(true)
    })

    it('returns FALSE if an empty string is passed', () => {
      expect(isNil('')).toBe(false)
    })

    it('returns FALSE if the number "0" is passed', () => {
      expect(isNil(0)).toBe(false)
    })
  })

  describe('isEmpty', () => {
    it('returns TRUE if passed an empty string', () => {
      expect(isEmpty('')).toBe(true)
    })

    it('returns TRUE if passed an empty object', () => {
      expect(isEmpty({})).toBe(true)
    })

    it('returns TRUE if passed an empty array', () => {
      expect(isEmpty([])).toBe(true)
    })

    it('returns FALSE if a non-empty string is passed', () => {
      expect(isEmpty('a')).toBe(false)
    })

    it('returns FALSE if the number "0" is passed', () => {
      expect(isEmpty(0)).toBe(false)
    })
  })

  describe('isNumeric', () => {
    it('returns TRUE if the passed argument is a numeric string', () => {
      expect(isNumeric('123')).toBe(true)
    })

    it("returns TRUE if the passed argument is a unit of measure ('px', '%', etc.)", () => {
      expect(isNumeric('20px')).toBe(true)
    })

    it('returns TRUE if the passed argument is a number', () => {
      expect(isNumeric(3123)).toBe(true)
    })

    it('returns FALSE the passed argument is a string not starting with a number', () => {
      expect(isNumeric('Ste. #6E')).toBe(false)
    })
  })

  describe('lengthMoreThan', () => {
    it('returns a function that returns false for inputs with length less than the given value', () => {
      const lengthMoreThanFour = lengthMoreThan(4)

      expect(lengthMoreThanFour('woo')).toBe(false)
      expect(lengthMoreThanFour({ length: 1 })).toBe(false)
      expect(lengthMoreThanFour([1])).toBe(false)
    })

    it('returns a function that returns false for inputs with length equal to the given value', () => {
      const lengthMoreThanTwo = lengthMoreThan(2)

      expect(lengthMoreThanTwo('yo')).toBe(false)
      expect(lengthMoreThanTwo({ length: 2 })).toBe(false)
      expect(lengthMoreThanTwo([1, 2])).toBe(false)
    })

    it('returns a function that returns true for inputs with length more than the given value', () => {
      const lengthMoreThanThree = lengthMoreThan(3)

      expect(
        lengthMoreThanThree('are you going to eat the rest of that bagel?'),
      ).toBe(true)
      expect(lengthMoreThanThree({ length: 10 })).toBe(true)
      expect(lengthMoreThanThree([1, 2, 3, 4])).toBe(true)
    })
  })

  describe('lengthLessThan', () => {
    it('returns a function that returns true for inputs with length less than the given value', () => {
      const lengthLessThanFour = lengthLessThan(4)

      expect(lengthLessThanFour('a')).toBe(true)
      expect(lengthLessThanFour({ length: 1 })).toBe(true)
      expect(lengthLessThanFour([1])).toBe(true)
    })

    it('returns a function that returns false for inputs with length equal to the given value', () => {
      const lengthLessThanTwo = lengthLessThan(2)

      expect(lengthLessThanTwo('yo')).toBe(false)
      expect(lengthLessThanTwo({ length: 2 })).toBe(false)
      expect(lengthLessThanTwo([1, 2])).toBe(false)
    })

    it('returns a function that returns false for inputs with length more than the given value', () => {
      const lengthLessThanThree = lengthLessThan(3)

      expect(lengthLessThanThree('I am so very cool')).toBe(false)
      expect(lengthLessThanThree({ length: 10 })).toBe(false)
      expect(lengthLessThanThree([1, 2, 3, 4])).toBe(false)
    })
  })

  describe('isPositiveNumericString', () => {
    it('returns false for numeric strings which are negative', () => {
      expect(isPositiveNumericString('-1.00')).toBe(false)
      expect(isPositiveNumericString('-9999')).toBe(false)
    })

    it('returns true for numeric strings which are positive', () => {
      expect(isPositiveNumericString('254')).toBe(true)
      expect(isPositiveNumericString('0.23')).toBe(true)
    })

    it('returns false for non-numeric strings', () => {
      expect(isPositiveNumericString('Grots')).toBe(false)
    })
  })

  describe('isNumericString', () => {
    it('returns true for numeric strings', () => {
      expect(isNumericString('25499')).toBe(true)
      expect(isNumericString('-0.23')).toBe(true)
      expect(isNumericString('-76')).toBe(true)
      expect(isNumericString('12312312321.123')).toBe(true)
    })

    it('returns false for non-numeric strings', () => {
      expect(isNumericString('stomp the humies!')).toBe(false)
    })
  })

  describe('notNumericString', () => {
    it('returns false for numeric strings', () => {
      expect(notNumericString('25499')).toBe(false)
      expect(notNumericString('-0.23')).toBe(false)
      expect(notNumericString('-76')).toBe(false)
      expect(notNumericString('12312312321.123')).toBe(false)
    })

    it('returns true for non-numeric strings', () => {
      expect(notNumericString('stomp the humies!')).toBe(true)
    })
  })

  describe('isEmptyString', () => {
    it('returns true for empty strings', () => {
      expect(isEmptyString('')).toBe(true)
    })

    it('returns true for strings with only whitespace', () => {
      expect(isEmptyString(' ')).toBe(true)
      expect(isEmptyString('\t')).toBe(true)
      expect(isEmptyString('\n\n')).toBe(true)
    })

    it('returns false for strings with non-whitespace characters', () => {
      expect(isEmptyString('everybody in the 313...')).toBe(false)
    })
  })

  describe('notEmptyString', () => {
    it('returns false for empty strings', () => {
      expect(notEmptyString('')).toBe(false)
    })

    it('returns false for strings with only whitespace', () => {
      expect(notEmptyString(' ')).toBe(false)
      expect(notEmptyString('\t')).toBe(false)
      expect(notEmptyString('\n\n')).toBe(false)
    })

    it('returns true for strings with non-whitespace characters', () => {
      expect(notEmptyString('everybody in the 313...')).toBe(true)
    })
  })

  describe('isEmpty', () => {
    it('returns true for null', () => {
      expect(isEmpty(null)).toBe(true)
    })

    it('returns true for undefined', () => {
      expect(isEmpty(undefined)).toBe(true)
    })

    it('returns true for values with a `length` property of 0', () => {
      expect(isEmpty([])).toBe(true)
      expect(isEmpty({ length: 0 })).toBe(true)
      expect(isEmpty('')).toBe(true)
    })

    it('returns false for values with a non-zero `length` property', () => {
      expect(isEmpty([1, 2])).toBe(false)
      expect(isEmpty({ length: 1 })).toBe(false)
      expect(isEmpty("What's the deal with airplane food?")).toBe(false)
    })

    it('returns false for objects that do not have a length property', () => {
      expect(isEmpty({ foo: 'bar' })).toBe(false)
    })
  })

  describe('notEmpty', () => {
    it('returns false for null', () => {
      expect(notEmpty(null)).toBe(false)
    })

    it('returns false for undefined', () => {
      expect(notEmpty(undefined)).toBe(false)
    })

    it('returns false for values with a `length` property of 0', () => {
      expect(notEmpty([])).toBe(false)
      expect(notEmpty({ length: 0 })).toBe(false)
      expect(notEmpty('')).toBe(false)
    })

    it('returns true for values with a non-zero `length` property', () => {
      expect(notEmpty([1, 2])).toBe(true)
      expect(notEmpty({ length: 1 })).toBe(true)
      expect(notEmpty("What's the deal with airplane food?")).toBe(true)
    })

    it('returns true for objects that do not have a length property', () => {
      expect(notEmpty({ foo: 'bar' })).toBe(true)
    })
  })
})
