<template>
  <ui-card class="ui-swatch-card">
    <ui-card-section class="swatch relative rounded-t-inherit overflow-hidden" :pad="false">
      <svg class="color-card-skein absolute top-0 left-0 w-full h-full" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 200" fill="none">
        <rect height="100%" width="100%" :fill="`url(#${gradientId})`"/>
        <text v-if="showTitle" x="50%" y="50%" dominant-baseline="middle" text-anchor="middle" :fill="titleColor">
          {{ productName }}
        </text>
        <defs>
          <linearGradient :id="gradientId" x1="0" x2="100%" y1="100%" y2="0" :gradientTransform="gradientTransform" gradientUnits="userSpaceOnUse">
            <stop offset="0%" :stop-color="gradientStart" />
            <stop offset="100%" :stop-color="gradientEnd" />
          </linearGradient>
        </defs>
      </svg>
    </ui-card-section>

    <ui-card-section class="ui-swatch-card-section w-details">
      <h2 class="text-md font-semibold mb-2">{{ productName }}</h2>

      <div class="details">
        <dl :class="dlClasses">
          <template v-for="detail in productDetails" :key="detail.term">
            <dt :id="detail.term" class="col-start-1 whitespace-nowrap font-semibold">{{ detail.term }}:</dt>
            <dd :aria-labelledby="detail.term" class="col-auto">{{ detail.definition }}</dd>
          </template>
        </dl>
      </div>
    </ui-card-section>
  </ui-card>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import UiCard from './Card.vue';
import UiCardSection from './CardSection.vue';
import { startCase, titleCase } from '@contrastagent/utils';

type Props = {
  colorValue: string
  gradientStart?: string
  gradientEnd?: string
  gradientTransform?: string
  productName: string
  showTitle?: boolean
  titleColor?: string
  details: {
    manufacturer: string
    productType: string
    colorRange: string
    price: string
    hex: string
  }
}

const props = withDefaults(defineProps<Props>(), {
  showTitle: false,
  titleColor: '#FFFFFF',
  gradientTransform: 'rotate(45)',
})

const gradient = computed(() => ({ start: props.gradientStart ?? props.colorValue, end: props.gradientEnd ?? props.colorValue }))
const gradientId = computed(() => `gradient_${gradient.value.start}_${gradient.value.end}`)

const dlClasses = computed(() => {
  const count = Object.keys(props.details).length
  return {
    [`grid grid-rows-${count} grid-flow-col text-xs`]: true,
  }
})

const productDetails = computed(() => {
  return Object.entries(props.details).map(([term, definition]) => {
    if (term === 'price') {
      definition = `$${parseFloat(definition).toFixed(2)}`
    }

    return {
      term: startCase(term),
      definition,
    }
  })
})
</script>

<style scoped>
.swatch {
  aspect-ratio: 3 / 2;
}
</style>