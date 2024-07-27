import { computed } from 'vue'
import { useSize } from '../../composables/useSize'
import { UiSpinnerProps } from './Spinner.types'

export const useSpinner = (props: UiSpinnerProps) => {
  const { sizeClasses, rawDimensions } = useSize(props)

  const colorClasses = computed(() => {
    const color = props.color ?? 'orange'

    return {
      'text-white': color === 'white',
      'text-black': color === 'black',
      'text-orange-500': color === 'orange',
      'text-blue-500': color === 'blue',
      'text-green-500': color === 'green',
      'text-red-500': color === 'red',
      'text-purple-500': color === 'purple',
      'text-pink-500': color === 'pink',
      'text-yellow-500': color === 'yellow',
      'text-indigo-500': color === 'indigo',
      'text-cyan-500': color === 'cyan',
      'text-teal-500': color === 'teal',
      'text-gray-500': color === 'gray',
    }
  })

  const rawSize = computed(() => rawDimensions.value?.width ?? 48)

  const strokeWidth = computed(() => props.thickness ?? 4)

  const radius = computed(() => rawSize.value / 2 - strokeWidth.value)

  const viewBox = computed(() => {
    const size = rawSize.value
    const xy = size / 2

    return `${xy} ${xy} ${size} ${size}`
  })

  return {
    colorClasses,
    radius,
    rawSize,
    sizeClasses,
    strokeWidth,
    viewBox,
  }
}
