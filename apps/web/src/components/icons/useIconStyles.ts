import { ThemeSizeAlias } from '@contrastagent/theme'
import { computed } from 'vue'

type UseIconStylesProps = {
  size?: ThemeSizeAlias | number | string
}

export const useIconStyles = ({ size = 'md' }: UseIconStylesProps = {}) => {
  const iconSizeClass = computed(() => {
    return {
      'size-4': size === 'xs',
      'size-5': size === 'sm',
      'size-6': size === 'md',
      'size-7': size === 'lg',
      'size-8': size === 'xl',
      [size]: typeof size === 'string' && /:?size-\d+/.test(size),
    }
  })

  return {
    iconSizeClass,
  }
}
