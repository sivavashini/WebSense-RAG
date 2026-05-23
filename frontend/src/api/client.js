import axios from 'axios'

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  timeout: 60000,
})

export const reportUrl = (id) => `${api.defaults.baseURL}/reports/${id}.pdf`
