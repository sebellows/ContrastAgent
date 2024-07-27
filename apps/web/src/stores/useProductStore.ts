import { defineStore } from 'pinia'
import CitadelPaints from '../mockData/citadel-product-list.json'
import { computed, reactive, toRefs } from 'vue'
import { getKeys } from '@contrastagent/utils'

export interface Product {
  id: string
  name: string
  slug: string
  price: number
  currency_code: string
  paint_type: string
  colour_range: string
  colour_value: string
  gradient_range: string[]
}

export const useProductStore = defineStore('products', () => {
  const state = reactive({
    // The current selected brand
    brand: '',
    // The current search query
    query: '',
    // The current selected product type
    productType: '',
    // The current selected color type
    colorType: '',

    results: [] as Product[],
  })

  const brands = computed(() => ['Citadel', 'Army Painer', 'Vallejo'])

  const products = computed(() => CitadelPaints.products)

  const colorRange = computed(() =>
    getKeys(CitadelPaints.paint_colour_range).map(
      key => `${key} (${CitadelPaints.paint_colour_range[key]})`,
    ),
  )

  const productTypes = computed(() =>
    getKeys(CitadelPaints.paint_types).map(key => `${key} (${CitadelPaints.paint_types[key]})`),
  )

  const updateBrand = (payload: string) => {
    state.brand = payload
    console.log('onBrandChange', payload)
  }

  const updateProductType = (payload: string) => {
    state.productType = payload
    console.log('onProductTypeChange', payload)
  }

  const updateColorType = (payload: string) => {
    state.colorType = payload
    console.log('onColorTypeChange', payload)
  }

  // const search = (query: string) => {
  //   state.query = query
  //   console.log('onSearch', query)
  // }

  const updateResults = ({ query, results }: { query: string; results: Product[] }) => {
    state.query = query
    state.results = results
    console.log('onResults', results)
  }

  return {
    ...toRefs(state),
    brands,
    products,
    colorRange,
    productTypes,
    updateBrand,
    updateProductType,
    updateColorType,
    updateResults,
  }
})
