import { RouteLocation } from 'vue-router'
import { ElementType } from '../../types/dom'

export interface UiLinkProps extends ElementType<'a'> {
  active?: boolean
  href?: string
  label?: string
  target?: string
  as?: string
  to?: RouteLocation
}
