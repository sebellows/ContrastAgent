<template>
  <header class="flex flex-col items-start mx-auto px-14 pb-5 bg-orange-500">
    <div class="flex items-start justify-between h-24 w-full">
      <div class="relative top-1/2 -translate-y-1/2 w-52" style="line-height: 0">
        <h1 class="font-display text-4xl font-normal uppercase">Contrast Agent</h1>
      </div>

      <div class="flex items-center justify-end relative h-full flex-1 transition-transform ease-in-out duration-300">
        <div class="flex items-center justify-between rounded-3xl relative ml-4 mr-6 w-full h-14 bg-black/15 dark:bg-white/15">
          <UiAutocomplete
            ref="gridAutocomplete"
            class="w-full h-full"
            label="Auto Complete"
            :datum="products"
            :dataKeys="['colour_range', 'name']"
            optionKey="name"
            clearable
            displayAs="grid"
            :text-input-classes="{ 'w-full h-full': true, 'round-full': true }"
            @selected="onSelect"
            @update:model-value="updateResults"
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
    <div class="flex items-center justify-between h-14 w-full">
      <h2 class="text-md font-semibold">Research &amp; Compare Paints for Miniature Hobbyists</h2>
    </div>
  </header>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { UiAutocomplete } from '../../components/autocomplete'
import { useProductStore } from '../../stores/useProductStore';
import { storeToRefs } from 'pinia';
import { Type } from '@contrastagent/utils';

const emit = defineEmits(['selected', 'update:modelValue'])

const sortBy = ref('')

const onSort = (value: string) => {
  sortBy.value = value
}

const matchedPaint = ref<any>()
const productsStore = useProductStore()
const { products } = storeToRefs(productsStore)
const { updateResults } = productsStore

const options = computed(() => ['Option 1', 'Option 2', 'Option 3'])

const gridAutocomplete = ref<InstanceType<Type<typeof UiAutocomplete>> | null>(null)

// const matchedPaints = computed(() => {
//   if (gridAutocomplete.value?.['results']?.length) {
//     return gridAutocomplete.value?.['results']
//   }
//   return []
// })

const onSelect = (value: any) => {
  matchedPaint.value = value
}
</script>

<style scoped>

</style>