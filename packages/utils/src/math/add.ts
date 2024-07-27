export function add(...nums: number[]): number {
  let i: number
  let sum: number
  const len = nums.length

  i = sum = 0

  while (i++ < len) {
    sum += nums[i]
  }

  return sum
}
