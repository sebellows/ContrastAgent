import { RouteLocation } from 'vue-router'
import { ElementType } from '../../types/dom'
import { ComponentStyleProps } from '../../composables/useTwStyles'

export interface UiButtonProps extends ElementType<'button'>, ComponentStyleProps {
  href?: string
  icon?: string
  label?: string
  type?: 'button' | 'submit' | 'reset' | 'menu'
  tag?: string
  to?: RouteLocation

  // Wrap the button contents?
  nowrap?: boolean

  // Button appearance props
  outline?: boolean
  round?: boolean
  square?: boolean
}

export interface UiIconButtonProps extends ElementType<'button'>, ComponentStyleProps {
  href?: string
  icon: string
  label?: string
  type?: 'button' | 'submit' | 'reset' | 'menu'
  tag?: string
  to?: RouteLocation

  // Button appearance props
  round?: boolean
  square?: boolean
}
