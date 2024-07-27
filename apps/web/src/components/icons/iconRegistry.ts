import { titleCase } from '@contrastagent/utils'
import { h } from 'vue'
import icons from './icons'

const registry = {} as { [name: string]: ReturnType<typeof h>[] }

const iconRegistry = (() =>
  Object.entries(icons).reduce((acc, [name, children]) => {
    acc[name] = []
    acc[name].push(h('title', titleCase(name)))
    acc[name].push(...children.map(child => h(child[0], child[1])))
    return acc
  }, registry))()

export { iconRegistry }
