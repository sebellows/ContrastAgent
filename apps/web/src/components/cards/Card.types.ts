import { ComponentPublicInstance } from 'vue'
import { ComponentStyleProps } from '../../composables/useTwStyles'

export interface UiCardProps extends ComponentStyleProps {
  tag?: string | ComponentPublicInstance
}

export interface UiCardSectionProps extends ComponentStyleProps {
  tag?: string | ComponentPublicInstance
}

export interface UiSwatchCardProps extends UiCardProps {
  colorValue: string
  gradientStart?: string
  gradientEnd?: string
  gradientTransform?: string
  productName: string
  showSvgTitle?: boolean
  svgTitleColor?: string
  details: {
    manufacturer: string
    productType: string
    colorRange: string
    price: string
    hex: string
  }
}
