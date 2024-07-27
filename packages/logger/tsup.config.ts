import { defineConfig, Options } from 'tsup'

export default defineConfig((options: Options) => ({
  entryPoints: ['src/index.ts'],
  format: ['esm'],
  dts: true,
  clean: true,
  ...options,
}))
