export const html = (strings: string[], ...values: string[]) =>
  String.raw({ raw: strings }, ...values)
