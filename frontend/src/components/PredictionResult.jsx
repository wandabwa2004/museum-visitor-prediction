import { fmtNum, tierColor, tierBorder } from '../utils/format'

export default function PredictionResult({ result }) {
  if (!result) return null

  const { date, predicted_visitors, lower_80, upper_80, lower_95, upper_95,
          traffic_tier, confidence, model_used } = result

  const revenue = predicted_visitors * 25

  return (
    <div className={`bg-white rounded-xl shadow-sm border-2 ${tierBorder(traffic_tier)} p-6 space-y-5`}>
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-800">Prediction — {date}</h2>
        <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${tierColor(traffic_tier)}`}>
          {traffic_tier} Traffic
        </span>
      </div>

      {/* Main number */}
      <div className="text-center py-4">
        <div className="text-6xl font-bold text-blue-700">{fmtNum(predicted_visitors)}</div>
        <div className="text-gray-500 mt-1 text-sm">expected visitors</div>
      </div>

      {/* Intervals */}
      <div className="space-y-2">
        <div className="flex justify-between text-sm bg-blue-50 rounded-lg px-4 py-2">
          <span className="text-gray-600">80% interval</span>
          <span className="font-medium text-blue-700">{fmtNum(lower_80)} – {fmtNum(upper_80)}</span>
        </div>
        <div className="flex justify-between text-sm bg-gray-50 rounded-lg px-4 py-2">
          <span className="text-gray-600">95% interval</span>
          <span className="font-medium text-gray-700">{fmtNum(lower_95)} – {fmtNum(upper_95)}</span>
        </div>
      </div>

      {/* Business insight */}
      <div className="border-t pt-4 grid grid-cols-2 gap-3">
        <div className="text-center">
          <div className="text-lg font-bold text-green-700">${fmtNum(revenue)}</div>
          <div className="text-xs text-gray-500">Est. revenue @ $25/ticket</div>
        </div>
        <div className="text-center">
          <div className="text-lg font-bold text-purple-700">{(confidence * 100).toFixed(0)}%</div>
          <div className="text-xs text-gray-500">Model confidence (R²)</div>
        </div>
      </div>

      <div className="text-xs text-gray-400 text-center">Model: {model_used}</div>
    </div>
  )
}
