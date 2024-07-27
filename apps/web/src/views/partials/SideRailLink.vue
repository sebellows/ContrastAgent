<template>
  <a href="javascript:void(0)" class="side-rail-link flex flex-col items-center h-14 w-20 no-underline text-slate-200 outline-none">
    <span class="flex items-center justify-center relative overflow-hidden w-14 h-8 rounded-2xl mb-2 bg-orange-200 active:bg-pink-300/40">
      <span class="block absolute top-0 left-0 w-full h-full bg-slate-100 active:bg-pink-300 opacity-40"></span>
      <UiIcon :name="icon" size="sm" role="presentation" aria-hidden="true" class="relative text-slate-700" />
    </span>
    <span class="block text-center text-xs font-medium tracking-tight">{{ title }}</span>
  </a>
</template>

<script setup lang="ts">
import UiIcon from '../../components/icons/Icon';

type Props = {
  title?: string
  icon: string
}

defineProps<Props>()

const emit = defineEmits<{
  (e: MouseEvent): void
}>()
</script>
