<template>
  <MainLayout>
    <header class="flex flex-col items-start mx-auto px-14 pb-5 bg-orange-500">
      <div class="flex items-start justify-between h-24 w-full">
        <div class="relative top-1/2 -translate-y-1/2 w-52" style="line-height: 0">
          <h1 class="font-display text-4xl font-normal uppercase">Topcoat</h1>
          <h2 class="text-md font-semibold">Research &amp; Compare Paints for Miniature Hobbyists</h2>
        </div>

        <div class="flex items-center justify-end relative h-full flex-1 transition-transform ease-in-out duration-300">
          <div class="flex items-center justify-between rounded-3xl relative ml-4 mr-6 w-full h-14 bg-black/15 dark:bg-white/15">
            <ui-autocomplete
              ref="gridAutocomplete"
              label="Auto Complete"
              :datum="products"
              :dataKeys="['colour_range', 'name']"
              optionKey="name"
              clearable
              displayAs="grid"
              @selected="onSelect"
            />
            <div class="flex justify-end min-w-fit mx-4">
              <UiSelectField
                :model-value="sortBy"
                :options="options"
                label="Sort By"
                class="w-36"
                @update:model-value="onSort"
              />
            </div>
          </div>
        </div>
      </div>
    </header>

    <!-- <ui-autocomplete
      v-if="!!products?.length"
      label="Auto Complete"
      :datum="products"
      :dataKeys="['colour_range', 'name']"
      optionKey="name"
      clearable
      @selected="onSelect"
    >
      <template v-slot:option="option">
        <div class="grid grid-cols-3 gap-2 w-full p-2">
          <div class="flex align-center col-span-2">
            <div class="w-8 h-6 border border-white shadow-sm mr-2" :style="{ backgroundColor: `${option.props.colour_value}` }"></div>
            <span>{{ option.props.name }}</span>
          </div>
          <b class="ml-2"><small>[{{ option.props.colour_range }}]</small></b>
        </div>
      </template>
    </ui-autocomplete> -->

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-2 mt-4" v-if="matchedPaints.length">
      <SwatchCard
        v-for="paint in matchedPaints"
        :key="paint.id"
        :colorValue="paint.colour_value"
        :productName="paint.name"
        :gradientStart="paint.gradient_range[0]"
        :gradientEnd="paint.gradient_range[1]"
        :details="{ manufacturer: 'Citadel', productType: paint.paint_type, colorRange: paint.colour_range, price: paint.price, hex: paint.colour_value }"
      />
    </div>

  </MainLayout>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue';
import TextField from './components/forms/TextField.vue'
import SelectField from './components/forms/SelectField.vue'
import UiAutocomplete from './components/autocomplete/Autocomplete.vue'
// import UiSpinner from './components/Spinner/UiSpinner.vue'
// import CitadelPaints from './mockData/citadel-product-list.json'
import { Type } from '@contrastagent/utils/*';
import SwatchCard from './components/cards/SwatchCard.vue';
import MainLayout from './views/MainLayout.vue';
import { useProductStore } from './stores/useProductStore';
import { storeToRefs } from 'pinia';
import { UiSelectField } from './components/forms';

const sortBy = ref('')

const onSort = (value: string) => {
  sortBy.value = value
}

const matchedPaint = ref<any>()
const productsStore = useProductStore()
const { products } = storeToRefs(productsStore)

const options = computed(() => ['Option 1', 'Option 2', 'Option 3'])

const gridAutocomplete = ref<InstanceType<Type<typeof UiAutocomplete>> | null>(null)

const matchedPaints = computed(() => {
  if (gridAutocomplete.value?.['results']?.length) {
    return gridAutocomplete.value?.['results']
  }
  return []
})

const onAutocomplete = (value: any[]) => {
  // console.log('onAutocomplete', value)
  // matchedPaints.value = value
}

const onSelect = (value: any) => {
  matchedPaint.value = value
}

// const formatLabel = (option: typeof CitadelPaints.products[number]) => {
//   // console.log('formatLabel', option)
//   return `${option.name} - (${option.colour_range})`

// }

onMounted(() => {
  // paints.value = CitadelPaints.products
})
</script>

<style scoped>
.container {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
}
</style>
