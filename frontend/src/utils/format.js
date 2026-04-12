export const fmtNum = (n) => Math.round(n).toLocaleString()

export const tierColor = (tier) => ({
  Low:    'bg-green-100 text-green-800',
  Medium: 'bg-yellow-100 text-yellow-800',
  High:   'bg-red-100 text-red-800',
}[tier] ?? 'bg-gray-100 text-gray-800')

export const tierBorder = (tier) => ({
  Low:    'border-green-400',
  Medium: 'border-yellow-400',
  High:   'border-red-400',
}[tier] ?? 'border-gray-300')
