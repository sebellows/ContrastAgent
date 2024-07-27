import { computed, defineComponent, h, PropType } from 'vue'
import { PaletteColorPath, ThemeSizeAlias, TwSizeSuffix } from '@contrastagent/theme'
import { useSize } from '../../composables/useSize'
import { iconRegistry } from './iconRegistry'

export default defineComponent({
  name: 'UiIcon',
  props: {
    name: {
      type: String,
      required: true,
    },
    size: {
      type: [String, Number] as PropType<ThemeSizeAlias | TwSizeSuffix | number | string>,
      default: 'md',
    },
    color: {
      type: String as PropType<PaletteColorPath>,
    },
    viewBox: {
      type: String,
      default: '0 0 24 24',
    },
  },
  setup(props) {
    const children = computed(() => iconRegistry[props.name])

    const { sizeClass } = useSize(props)

    return () =>
      h(
        'svg',
        {
          xmlns: 'http://www.w3.org/2000/svg',
          class: { 'ui-icon stroke-current': true, ...sizeClass.value },
          viewBox: props.viewBox,
          fill: 'none',
        },
        children.value,
      )
  },
})
