export function uniq<T = any>(arr: T[]) {
  return Array.from(new Set([...arr]))
}
