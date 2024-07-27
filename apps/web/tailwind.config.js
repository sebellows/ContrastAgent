import colors from 'tailwindcss/colors'
import { generateThemeConfig } from '@contrastagent/theme'

const customTheme = generateThemeConfig({
  primary: colors.orange,
  secondary: colors.violet,
  accent: colors.pink,
})

export default {
  content: ['./index.html', 'src/**/*.{vue,js,ts,jsx,tsx}'],
  darkMode: 'class',
  theme: customTheme,
}
