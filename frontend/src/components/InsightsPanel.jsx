import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, Cell } from 'recharts'

const COLORS = ['#2563eb','#3b82f6','#60a5fa','#93c5fd','#bfdbfe',
                 '#dbeafe','#1d4ed8','#1e40af','#1e3a8a','#172554']

export default function InsightsPanel({ insights }) {
  if (!insights) return null

  const { best_model, metrics, feature_count, training_records, top_features, all_model_results } = insights

  const modelRows = Object.entries(all_model_results ?? {}).map(([name, m]) => ({
    name, MAE: m.MAE?.toFixed(1), RMSE: m.RMSE?.toFixed(1),
    R2: m.R2?.toFixed(3), MAPE: m.MAPE?.toFixed(1) + '%',
  }))

  return (
    <div className="space-y-6">

      {/* Key metrics */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">
          Best Model: <span className="text-blue-600">{best_model}</span>
        </h2>
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          {[
            { label: 'MAE',  value: metrics.mae,        unit: 'visitors' },
            { label: 'RMSE', value: metrics.rmse,       unit: 'visitors' },
            { label: 'R²',   value: metrics.r2,         unit: '' },
            { label: 'MAPE', value: metrics.mape + '%', unit: '' },
          ].map(({ label, value, unit }) => (
            <div key={label} className="bg-gray-50 rounded-lg p-3 text-center">
              <div className="text-xs text-gray-500 mb-1">{label}</div>
              <div className="text-xl font-bold text-blue-700">{value}</div>
              {unit && <div className="text-xs text-gray-400">{unit}</div>}
            </div>
          ))}
        </div>
        <div className="mt-3 text-xs text-gray-400">
          Trained on {training_records?.toLocaleString()} days &nbsp;·&nbsp; {feature_count} features
        </div>
      </div>

      {/* Feature importance */}
      <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
        <h2 className="text-lg font-semibold text-gray-800 mb-4">Top 10 Feature Importances</h2>
        <ResponsiveContainer width="100%" height={260}>
          <BarChart
            layout="vertical"
            data={[...top_features].reverse()}
            margin={{ left: 140, right: 20, top: 5, bottom: 5 }}
          >
            <XAxis type="number" tick={{ fontSize: 11 }} />
            <YAxis dataKey="feature" type="category" tick={{ fontSize: 11 }} width={140} />
            <Tooltip formatter={(v) => v.toFixed(4)} />
            <Bar dataKey="importance" radius={[0,4,4,0]}>
              {top_features.map((_, i) => (
                <Cell key={i} fill={COLORS[i % COLORS.length]} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Model comparison table */}
      {modelRows.length > 0 && (
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <h2 className="text-lg font-semibold text-gray-800 mb-4">All Model Results</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-sm">
              <thead>
                <tr className="border-b text-gray-500">
                  <th className="text-left py-2 pr-4">Model</th>
                  <th className="text-right py-2 px-2">MAE</th>
                  <th className="text-right py-2 px-2">RMSE</th>
                  <th className="text-right py-2 px-2">R²</th>
                  <th className="text-right py-2 pl-2">MAPE</th>
                </tr>
              </thead>
              <tbody>
                {modelRows.map((r) => (
                  <tr key={r.name} className={`border-b last:border-0 ${r.name === best_model ? 'bg-blue-50 font-semibold' : ''}`}>
                    <td className="py-2 pr-4">{r.name} {r.name === best_model && '★'}</td>
                    <td className="text-right px-2">{r.MAE}</td>
                    <td className="text-right px-2">{r.RMSE}</td>
                    <td className="text-right px-2">{r.R2}</td>
                    <td className="text-right pl-2">{r.MAPE}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  )
}
