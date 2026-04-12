import { useState, useEffect } from 'react'
import { BarChart2, Calendar, TrendingUp, Info } from 'lucide-react'
import { getHistorical, getInsights } from './services/api'
import PredictionForm   from './components/PredictionForm'
import PredictionResult from './components/PredictionResult'
import HistoricalChart  from './components/HistoricalChart'
import InsightsPanel    from './components/InsightsPanel'
import StatCard         from './components/StatCard'
import { fmtNum }       from './utils/format'

const TABS = [
  { id: 'predict',    label: 'Predict',   icon: Calendar },
  { id: 'historical', label: 'Historical', icon: TrendingUp },
  { id: 'insights',   label: 'Insights',  icon: BarChart2 },
]

export default function App() {
  const [tab,        setTab]        = useState('predict')
  const [prediction, setPrediction] = useState(null)
  const [historical, setHistorical] = useState([])
  const [insights,   setInsights]   = useState(null)
  const [loading,    setLoading]    = useState(false)

  useEffect(() => {
    setLoading(true)
    Promise.all([
      getHistorical({ limit: 365 }).then((r) => setHistorical(r.data.records)),
      getInsights().then((r) => setInsights(r.data)),
    ]).catch(console.error).finally(() => setLoading(false))
  }, [])

  // Summary stats from historical data
  const totalVisitors = historical.reduce((s, r) => s + r.visitors, 0)
  const avgVisitors   = historical.length ? Math.round(totalVisitors / historical.length) : 0
  const peakVisitors  = historical.length ? Math.max(...historical.map((r) => r.visitors)) : 0

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-blue-700 text-white shadow-md">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold">Museum Visitor Prediction</h1>
            <p className="text-blue-200 text-xs mt-0.5">Melbourne Museum of Migration</p>
          </div>
          {loading && (
            <span className="text-blue-200 text-sm animate-pulse">Loading data…</span>
          )}
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-4 py-6 space-y-6">

        {/* Summary stat cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <StatCard label="Avg Daily Visitors"  value={fmtNum(avgVisitors)}   color="blue"   icon={TrendingUp} />
          <StatCard label="Peak Day Visitors"   value={fmtNum(peakVisitors)}  color="purple" icon={BarChart2} />
          <StatCard label="Days of History"     value={historical.length}     color="green"  icon={Calendar} />
          <StatCard
            label="Best Model"
            value={insights?.best_model ?? '—'}
            sub={insights ? `R² ${insights.metrics.r2}` : ''}
            color="yellow"
            icon={Info}
          />
        </div>

        {/* Tabs */}
        <div className="flex gap-1 bg-white border border-gray-200 rounded-xl p-1 w-fit shadow-sm">
          {TABS.map(({ id, label, icon: Icon }) => (
            <button
              key={id}
              onClick={() => setTab(id)}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                tab === id
                  ? 'bg-blue-600 text-white shadow'
                  : 'text-gray-600 hover:bg-gray-100'
              }`}
            >
              <Icon size={15} />
              {label}
            </button>
          ))}
        </div>

        {/* Tab content */}
        {tab === 'predict' && (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <PredictionForm onResult={setPrediction} />
            <PredictionResult result={prediction} />
          </div>
        )}

        {tab === 'historical' && (
          <HistoricalChart data={historical} />
        )}

        {tab === 'insights' && (
          <InsightsPanel insights={insights} />
        )}
      </main>

      <footer className="text-center text-xs text-gray-400 py-6 mt-8 border-t">
        Museum Visitor Prediction System &nbsp;·&nbsp; Melbourne Museum of Migration
      </footer>
    </div>
  )
}
