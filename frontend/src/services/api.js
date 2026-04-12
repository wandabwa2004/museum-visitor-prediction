import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL
    ? `${import.meta.env.VITE_API_URL}/api`
    : '/api',   // falls back to Vite proxy in local dev
})

export const getPrediction = (payload) => api.post('/predict', payload)
export const getHistorical = (params = {}) => api.get('/historical', { params })
export const getInsights   = () => api.get('/insights')
export const getDateInfo   = (date) => api.get('/date-info', { params: { date } })
