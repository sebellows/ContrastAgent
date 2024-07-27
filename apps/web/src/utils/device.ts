export function isIOS() {
  return (
    typeof navigator != null &&
    !!(
      navigator.userAgent.match(/(iPhone|iPad)/g) &&
      navigator.userAgent.match(/AppleWebKit/g)
    )
  )
}
