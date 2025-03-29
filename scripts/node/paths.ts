const { readFileSync } = require('fs')
const { resolve } = require('path')

const ROOT_PATH = resolve(__dirname, '..')
const API_SRC_PATH = resolve(ROOT_PATH, 'apps/api/src')

/**
 * Get the .prettierrc file so that we can use Prettier to format the output
 * of the generated files.
 */
const PRETTIER_CONFIG_FILE = readFileSync(resolve(ROOT_PATH, '.prettierrc'), 'utf8')

module.exports = {
  ROOT_PATH,
  PRETTIER_CONFIG_FILE,
}
