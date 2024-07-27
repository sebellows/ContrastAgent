import { SizeProps } from '../../composables/useSize'
import { ElementAttrs } from '../../types/dom'

export interface UiIconProps extends SizeProps, ElementAttrs<'svg'> {
  name: string
}
