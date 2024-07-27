<template>
  <div class="h-screen overflow-hidden rounded-tr-2xl rounded-br-2xl z-10 bg-slate-200 dark:bg-slate-700" style="width: 320px;">
    <div class="ui-side-nav-inner w-full h-full overflow-auto scroll">
      <div class="block px-5 py-6">
        <div class="flex justify-end items-center">
          <UiButton icon="refresh" flat label="Reset All" />
          <UiIconButton icon="close" round flat label="Close side navigation" />
        </div>

        <div class="flex justify-between items-center mb-4">
          <h2 class="text-xl my-4 font-medium">Filter</h2>
        </div>

        <div class="flex items-center mb-4">
          <UiIcon name="search" class="text-slate-200 mr-2" />
          <h3 class="text-lg my-4 font-medium">Product</h3>
        </div>

        <div class="flex flex-col gap-4">
          <div class="flex flex-col gap-2">
            <UiSelectField v-model="brand" :options="brands" label="Brand" />
          </div>

          <div class="flex flex-col gap-2">
            <UiSelectField v-model="productType" :options="productTypes" label="Product Type" />
          </div>

          <div class="flex flex-col gap-2">
            <UiSelectField v-model="colorType" :options="colorRange" label="Color" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { UiButton, UiIconButton } from '../../components/button';
import { UiIcon } from '../../components/icons';
import { UiSelectField } from '../../components/forms';
import { useProductStore } from '../../stores/useProductStore';
import { storeToRefs } from 'pinia';

defineOptions({
  name: 'UiSideNav',
})

const productsStore = useProductStore()

// const brands = productsStore.brands
const { colorRange, productTypes } = storeToRefs(productsStore)

const brands = computed(() => ['Citadel', 'Army Painer', 'Vallejo'])

const brand = ref('');
const productType = ref('');
const colorType = ref('');
</script>

<style scoped>
.ui-side-nav-inner {
  scrollbar-color: #4B5563 #1F2937;
  scrollbar-width: thin;
}
</style>