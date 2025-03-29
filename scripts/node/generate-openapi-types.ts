import { readFileSync } from 'fs'
import { resolve } from 'path'
import { createClient }from '@hey-api/openapi-ts'
import { API_SRC_PATH, OPENAPI_URL_LOCAL } from './paths'

const OPENAPI_URL_LOCAL = 'http://127.0.0.1:8000/openapi.json'

async function generateTypes() {
  await createClient({
    client: '@hey-api/client-fetch',
    input: OPENAPI_URL_LOCAL,
    output: {
      format: 'prettier',
      path: API_SRC_PATH
    },
    types: {
      enums: false,
    },
    schemas: {
      type: 'json',
    },
  }).catch(reason => {
    throw new Error('generate-openapi-types Error: ', reason)
  })
}

generateTypes()
