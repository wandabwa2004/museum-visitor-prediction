import {
  ResponsiveContainer, ComposedChart, Area, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, Legend, Bar,
} from 'recharts'
import { format, parseISO } from 'date-fns'

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null
  return (
    <div className="bg-white border border-gray-200 rounded-lg shadow-lg p-3 text-sm">
      <p className="font-semibold text-gray-700 mb-1">{label}</p>
      {payload.map((p) => (
        <p key={p.name} style={{ color: p.color }}>
          {p.name}: <strong>{Math.round(p.value).toLocaleString()}</strong>
        </p>
      ))}
    </div>
  )
}

export default function HistoricalChart({ data }) {
  if (!data?.length) return (
    <div className="bg-white rounded-xl border border-gray-200 p-6 text-center text-gray-400">
      No historical data loaded.
    </div>
  )

  const chartData = data.map((r) => ({
    date:     format(parseISO(r.date), 'dd MMM yy'),
    visitors: r.visitors,
  }))

  // Compute 30-day rolling average
  const withMA = chartData.map((d, i) => {
    const window = chartData.slice(Math.max(0, i - 29), i + 1)
    const avg = window.reduce((s, w) => s + w.visitors, 0) / window.length
    return { ...d, ma30: Math.round(avg) }
  })

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-800 mb-4">Historical Visitor Trends</h2>
      <ResponsiveContainer width="100%" height={300}>
        <ComposedChart data={withMA} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis
            dataKey="date"
            tick={{ fontSize: 11 }}
            interval={Math.floor(withMA.length / 8)}
          />
          <YAxis tick={{ fontSize: 11 }} />
          <Tooltip content={<CustomTooltip />} />
          <Legend />
          <Bar dataKey="visitors" fill="#bfdbfe" name="Daily Visitors" radius={[2,2,0,0]} />
          <Line
            type="monotone"
            dataKey="ma30"
            stroke="#2563eb"
            strokeWidth={2}
            dot={false}
            name="30-day Average"
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  )
}
