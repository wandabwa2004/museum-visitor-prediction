import { useState, useEffect, useRef } from 'react'
import { getPrediction, getDateInfo } from '../services/api'

const defaultForm = {
  date:               new Date().toISOString().split('T')[0],
  temperature:        '',
  precipitation:      '',
  weather_type:       'Partly Cloudy',
  is_public_holiday:  0,
  is_school_holiday:  0,
  special_exhibition: 0,
  local_event:        0,
  marketing_campaign: 0,
  ticket_promotion:   0,
  ticket_price:       25,
}

// ── small reusable sub-components ─────────────────────────────────────────────

function Badge({ children, color = 'gray' }) {
  const colors = {
    gray:   'bg-gray-100 text-gray-600',
    purple: 'bg-purple-100 text-purple-700',
    orange: 'bg-orange-100 text-orange-700',
    green:  'bg-green-100 text-green-700',
    blue:   'bg-blue-100 text-blue-700',
    teal:   'bg-teal-100 text-teal-700',
  }
  return (
    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${colors[color]}`}>
      {children}
    </span>
  )
}

function SectionLabel({ children }) {
  return <p className="text-sm font-medium text-gray-600">{children}</p>
}

// ── main component ─────────────────────────────────────────────────────────────

export default function PredictionForm({ onResult }) {
  const [form, setForm]                 = useState(defaultForm)
  const [loading, setLoading]           = useState(false)
  const [error, setError]               = useState(null)
  const [dateInfo, setDateInfo]         = useState(null)
  const [dateInfoLoading, setDateInfoLoading] = useState(false)

  // 'auto' → weather fields follow the Open-Meteo response when date changes
  // 'manual' → user has edited at least one weather field; date changes won't overwrite
  const [weatherMode, setWeatherMode]   = useState('auto')

  // Track which holiday toggles have been manually flipped by the user since
  // the last date-info fetch (so we don't overwrite intentional overrides).
  const manualHolidays = useRef({ is_public_holiday: false, is_school_holiday: false })

  const set = (k, v) => setForm((f) => ({ ...f, [k]: v }))

  // ── fetch date info whenever date changes ────────────────────────────────────
  useEffect(() => {
    if (!form.date) return

    setDateInfoLoading(true)
    setDateInfo(null)
    // Reset manual-override flags for the new date
    manualHolidays.current = { is_public_holiday: false, is_school_holiday: false }

    getDateInfo(form.date)
      .then(({ data }) => {
        setDateInfo(data)

        // Auto-populate holidays (unless the user already flipped them)
        setForm((f) => ({
          ...f,
          is_public_holiday: manualHolidays.current.is_public_holiday
            ? f.is_public_holiday
            : data.is_public_holiday,
          is_school_holiday: manualHolidays.current.is_school_holiday
            ? f.is_school_holiday
            : data.is_school_holiday,
          // Auto-populate weather only if in auto mode and data is available
          ...(weatherMode === 'auto' && data.weather
            ? {
                temperature:   data.weather.temperature,
                precipitation: data.weather.precipitation,
                weather_type:  data.weather.weather_type,
              }
            : weatherMode === 'auto' && !data.weather
            ? { temperature: '', precipitation: '', weather_type: 'Partly Cloudy' }
            : {}),
        }))
      })
      .catch(() => setDateInfo(null))
      .finally(() => setDateInfoLoading(false))
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [form.date])

  // When the user re-enables auto weather, re-apply the last fetched data
  useEffect(() => {
    if (weatherMode !== 'auto' || !dateInfo) return
    if (dateInfo.weather) {
      setForm((f) => ({
        ...f,
        temperature:   dateInfo.weather.temperature,
        precipitation: dateInfo.weather.precipitation,
        weather_type:  dateInfo.weather.weather_type,
      }))
    } else {
      setForm((f) => ({ ...f, temperature: '', precipitation: '', weather_type: 'Partly Cloudy' }))
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [weatherMode])

  // ── submit ───────────────────────────────────────────────────────────────────
  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    try {
      const payload = {
        ...form,
        temperature:        form.temperature   !== '' ? parseFloat(form.temperature)   : undefined,
        precipitation:      form.precipitation !== '' ? parseFloat(form.precipitation) : 0,
        special_exhibition: Number(form.special_exhibition),
        local_event:        Number(form.local_event),
        marketing_campaign: Number(form.marketing_campaign),
        ticket_promotion:   Number(form.ticket_promotion),
        ticket_price:       parseFloat(form.ticket_price),
        is_public_holiday:  Number(form.is_public_holiday),
        is_school_holiday:  Number(form.is_school_holiday),
      }
      const { data } = await getPrediction(payload)
      onResult(data)
    } catch (err) {
      setError(err.response?.data?.detail ?? 'Prediction failed. Is the backend running?')
    } finally {
      setLoading(false)
    }
  }

  // ── holiday toggle with auto-badge ───────────────────────────────────────────
  const HolidayToggle = ({ label, field, helperText }) => {
    const isAuto = dateInfo !== null && !manualHolidays.current[field]
    return (
      <label className="flex items-start gap-2 cursor-pointer select-none">
        <div
          onClick={() => {
            manualHolidays.current[field] = true
            set(field, form[field] ? 0 : 1)
          }}
          className={`mt-0.5 flex-shrink-0 w-10 h-6 rounded-full transition-colors relative ${
            form[field] ? 'bg-blue-500' : 'bg-gray-300'
          }`}
        >
          <span
            className={`absolute top-1 w-4 h-4 rounded-full bg-white shadow transition-all ${
              form[field] ? 'left-5' : 'left-1'
            }`}
          />
        </div>
        <div className="min-w-0">
          <div className="flex items-center gap-1.5 flex-wrap">
            <span className="text-sm text-gray-700">{label}</span>
            {isAuto && <Badge color="green">Auto</Badge>}
          </div>
          {helperText && (
            <p className="text-xs text-gray-500 mt-0.5 truncate">{helperText}</p>
          )}
        </div>
      </label>
    )
  }

  // ── event / marketing toggle (no auto-badge needed) ──────────────────────────
  const Toggle = ({ label, field }) => (
    <label className="flex items-center gap-2 cursor-pointer select-none">
      <div
        onClick={() => set(field, form[field] ? 0 : 1)}
        className={`w-10 h-6 rounded-full transition-colors relative flex-shrink-0 ${
          form[field] ? 'bg-blue-500' : 'bg-gray-300'
        }`}
      >
        <span
          className={`absolute top-1 w-4 h-4 rounded-full bg-white shadow transition-all ${
            form[field] ? 'left-5' : 'left-1'
          }`}
        />
      </div>
      <span className="text-sm text-gray-700">{label}</span>
    </label>
  )

  // ── weather source badge ─────────────────────────────────────────────────────
  const WeatherSourceBadge = () => {
    if (weatherMode === 'manual') return <Badge color="orange">Manual</Badge>
    if (!dateInfo) return null
    if (dateInfo.weather?.source === 'archive')  return <Badge color="teal">Historical</Badge>
    if (dateInfo.weather?.source === 'forecast') return <Badge color="blue">Forecast</Badge>
    return <Badge color="gray">Seasonal default</Badge>
  }

  // ── render ───────────────────────────────────────────────────────────────────
  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 space-y-5"
    >
      <h2 className="text-lg font-semibold text-gray-800">Predict Visitors</h2>

      {/* ── Date ─────────────────────────────────────────────────────────────── */}
      <div>
        <label className="block text-sm font-medium text-gray-600 mb-1">Date</label>
        <input
          type="date"
          value={form.date}
          onChange={(e) => set('date', e.target.value)}
          required
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />

        {/* Contextual date badges */}
        <div className="flex flex-wrap gap-1.5 mt-2 min-h-[22px]">
          {dateInfoLoading && (
            <span className="text-xs text-gray-400 italic">Fetching date context…</span>
          )}
          {!dateInfoLoading && dateInfo && (
            <>
              <Badge color="gray">{dateInfo.day_name}</Badge>
              <Badge color="purple">{dateInfo.season}</Badge>
              {dateInfo.is_weekend
                ? <Badge color="orange">Weekend</Badge>
                : <Badge color="gray">Weekday</Badge>
              }
            </>
          )}
        </div>
      </div>

      {/* ── Calendar ─────────────────────────────────────────────────────────── */}
      <div className="space-y-3">
        <SectionLabel>Calendar</SectionLabel>
        <HolidayToggle
          label="Public Holiday"
          field="is_public_holiday"
          helperText={
            dateInfo?.holiday_name
              ? dateInfo.holiday_name
              : form.is_public_holiday
              ? 'Victorian public holiday'
              : null
          }
        />
        <HolidayToggle
          label="School Holiday"
          field="is_school_holiday"
          helperText={dateInfo?.school_holiday_name || null}
        />
      </div>

      {/* ── Weather ──────────────────────────────────────────────────────────── */}
      <div className="space-y-3">
        <div className="flex items-center justify-between">
          <SectionLabel>Weather</SectionLabel>
          {/* Auto-fetch master toggle */}
          <label className="flex items-center gap-1.5 cursor-pointer select-none">
            <span className="text-xs text-gray-500">Auto-fetch</span>
            <div
              onClick={() => setWeatherMode((m) => (m === 'auto' ? 'manual' : 'auto'))}
              className={`w-8 h-5 rounded-full transition-colors relative ${
                weatherMode === 'auto' ? 'bg-blue-500' : 'bg-gray-300'
              }`}
            >
              <span
                className={`absolute top-0.5 w-4 h-4 rounded-full bg-white shadow transition-all ${
                  weatherMode === 'auto' ? 'left-3.5' : 'left-0.5'
                }`}
              />
            </div>
          </label>
        </div>

        <div className="grid grid-cols-2 gap-3">
          <div>
            <div className="flex items-center gap-1.5 mb-1">
              <label className="text-sm font-medium text-gray-600">Temperature (°C)</label>
              <WeatherSourceBadge />
            </div>
            <input
              type="number"
              step="0.1"
              placeholder={weatherMode === 'auto' ? 'auto' : 'enter value'}
              value={form.temperature}
              onChange={(e) => {
                setWeatherMode('manual')
                set('temperature', e.target.value)
              }}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>
          <div>
            <div className="flex items-center gap-1.5 mb-1">
              <label className="text-sm font-medium text-gray-600">Precipitation (mm)</label>
            </div>
            <input
              type="number"
              step="0.1"
              min="0"
              placeholder="0"
              value={form.precipitation}
              onChange={(e) => {
                setWeatherMode('manual')
                set('precipitation', e.target.value)
              }}
              className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
            />
          </div>
        </div>

        <div>
          <div className="flex items-center gap-1.5 mb-1">
            <label className="text-sm font-medium text-gray-600">Weather Type</label>
            <WeatherSourceBadge />
          </div>
          <select
            value={form.weather_type}
            onChange={(e) => {
              setWeatherMode('manual')
              set('weather_type', e.target.value)
            }}
            className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
          >
            {['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy'].map((w) => (
              <option key={w}>{w}</option>
            ))}
          </select>
        </div>
      </div>

      {/* ── Events & Marketing ────────────────────────────────────────────────── */}
      <div className="space-y-3">
        <SectionLabel>Events &amp; Marketing</SectionLabel>
        <div className="grid grid-cols-2 gap-3">
          <Toggle label="Special Exhibition" field="special_exhibition" />
          <Toggle label="Local Event"        field="local_event" />
          <Toggle label="Marketing Campaign" field="marketing_campaign" />
          <Toggle label="Ticket Promotion"   field="ticket_promotion" />
        </div>
      </div>

      {/* ── Ticket Price ─────────────────────────────────────────────────────── */}
      <div>
        <label className="block text-sm font-medium text-gray-600 mb-1">
          Ticket Price (AUD)
        </label>
        <input
          type="number"
          step="0.5"
          min="0"
          value={form.ticket_price}
          onChange={(e) => set('ticket_price', e.target.value)}
          className="w-full border border-gray-300 rounded-lg px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-400"
        />
      </div>

      {error && (
        <p className="text-sm text-red-600 bg-red-50 rounded p-2">{error}</p>
      )}

      <button
        type="submit"
        disabled={loading}
        className="w-full bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-medium py-2.5 rounded-lg transition-colors"
      >
        {loading ? 'Predicting…' : 'Predict'}
      </button>
    </form>
  )
}
