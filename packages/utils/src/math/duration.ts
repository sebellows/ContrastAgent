export function easeInOutQuad(duration: number, ratio: number) {
  if (ratio <= 0.5) {
    return duration * Math.sqrt((ratio * 1) / 2)
  }

  if (ratio <= 1) {
    return duration * (1 - Math.sqrt(1 - ratio) / Math.sqrt(2))
  }

  return duration
}

export function calculateDuration(
  easing: string,
  width: number,
  distance: number,
  duration: number,
) {
  const ratio = distance / width

  switch (easing) {
    case 'linear':
      return duration * ratio
    case 'easeInOutQuad':
      return easeInOutQuad(duration, ratio)
    case 'easeInQuart':
      return duration * Math.pow(ratio, 1 / 4)
    default:
      return duration * ratio
  }
}
