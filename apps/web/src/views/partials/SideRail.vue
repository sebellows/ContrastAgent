<template>
  <div class="flex flex-col items-center gap-2 h-full fixed left-0 overflow-y-auto py-6 w-24 z-10 bg-gradient-to-b from-violet-500 to-violet-800">
    <UiSideRailLink icon="home" title="Home" />
    <UiSideRailLink icon="info" title="About" />
  </div>
</template>

<script setup lang="ts">
import UiSideRailLink from './SideRailLink.vue';


defineOptions({
  name: 'UiSideRail',
})
</script>

<style scoped>

</style>