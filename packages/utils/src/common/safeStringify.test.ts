import { beforeAll, describe, expect, test } from 'vitest'
import genericClientData from './internal/mockdata/generic-client-data.json'
import { safeStringify } from './safeStringify'

type Client = {
  id: number
  first_name: string
  last_name: string
  email: string
  ip_address: string
  region: string
}

type ClientReceiver = Client & {
  self_reference?: Client
}

function createProxyOjb(client: Client) {
  return new Proxy<ClientReceiver>(client, {
    get(target, p, _receiver) {
      return target[p]
    },
    set(target, p, newValue, _receiver) {
      if (p === 'self_reference') {
        target.self_reference = newValue
        return true
      }

      return true
    },
  })
}

describe('safeStringify', () => {
  let client: Client
  let testProxy2: ClientReceiver

  beforeAll(() => {
    client = genericClientData.clients[1]!
    testProxy2 = createProxyOjb(client)
    testProxy2.self_reference = client
  })

  test('without `safeStringify`, `JSON.stringify`-ing an object that circularly references itself will throw a TypeError', () => {
    const stringifyClient = () => JSON.stringify(client)

    expect(stringifyClient).toThrow(TypeError)
  })

  test('with `safeStringify`, an object that circularly references itself will not throw a TypeError', () => {
    const clonedProxy = JSON.parse(safeStringify(testProxy2))

    expect(clonedProxy).toBeTypeOf('object')
    expect(clonedProxy.self_reference.first_name).toStrictEqual('Audi')
  })
})
