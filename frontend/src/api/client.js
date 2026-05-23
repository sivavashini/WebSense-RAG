import axios from 'axios'

// Vercel deployment: the FastAPI service is mounted under /api.
// VITE_API_URL can override this for custom environments, but production uses same-origin requests.
export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
  timeout: 60000,
})

export const reportUrl = (id) => `${api.defaults.baseURL}/reports/${id}.pdf`
