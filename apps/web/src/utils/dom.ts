export const getTargetValue = (evt: Event) => {
  const target = evt.target as any

  return target?.value ?? ''
}
