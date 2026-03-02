import axios from 'axios'

// Determine API base URL based on environment
let API_BASE_URL = ''

if (import.meta.env.MODE === 'production') {
  // In production, use the environment variable set by Render
  API_BASE_URL = import.meta.env.VITE_API_URL || window.location.origin
} else {
  // In development, use relative paths (handled by vite proxy)
  API_BASE_URL = ''
}

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
})

// Add request interceptor for debugging
api.interceptors.request.use((config) => {
  console.log(`API Request: ${config.method.toUpperCase()} ${config.baseURL}${config.url}`)
  return config
}, (error) => {
  console.error('Request Error:', error)
  return Promise.reject(error)
})

// Add response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      console.error(`API Response Error: ${error.response.status}`, error.response.data)
    } else if (error.request) {
      console.error('No response received:', error.request)
    } else {
      console.error('Error:', error.message)
    }
    return Promise.reject(error)
  }
)

export default api
