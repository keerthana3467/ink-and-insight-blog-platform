import axios from 'axios'
export const api = axios.create({ baseURL: '/api', withCredentials: true })
function cookie(name) {
  return document.cookie.split('; ').find(row => row.startsWith(name + '='))?.split('=').slice(1).join('=')
}
api.interceptors.request.use(config => {
  const method = (config.method || 'get').toLowerCase()
  if (!['get','head','options','trace'].includes(method)) {
    const token = cookie('csrftoken')
    if (token) config.headers['X-CSRFToken'] = decodeURIComponent(token)
  }
  return config
})
export async function csrf() { await api.get('/csrf/') }
export const media = url => url || ''
export function errorMessage(error) {
  const data = error?.response?.data
  if (!data) return 'Something went wrong. Please try again.'
  if (typeof data.detail === 'string') return data.detail
  return Object.entries(data).map(([key,value]) => `${key}: ${Array.isArray(value) ? value.join(', ') : value}`).join(' · ')
}
