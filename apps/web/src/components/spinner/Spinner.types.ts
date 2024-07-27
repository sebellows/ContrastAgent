import { ThemeSizeAlias } from '@contrastagent/theme'
import { SizeProps } from '../../composables/useSize'

export type UiSpinnerProps = {
  color?: string
  hue?: number | string
  size?: ThemeSizeAlias
  thickness?: number
  miterLimit?: number
} & SizeProps
