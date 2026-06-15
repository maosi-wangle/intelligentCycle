import axios from 'axios'
import { showToast } from 'vant'

const instance = axios.create({
  baseURL: '/api',
  timeout: 10000
})

instance.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => {
    return Promise.reject(error)
  }
)

instance.interceptors.response.use(
  response => {
    const res = response.data
    if (res.code !== 0) {
      showToast(res.message || '请求失败')
      return Promise.reject(new Error(res.message || 'Error'))
    }
    return res.data
  },
  error => {
    if (error.code === 'ECONNABORTED') {
      showToast('请求超时，请检查网络')
    } else if (error.response?.status === 401) {
      localStorage.removeItem('token')
      localStorage.removeItem('user')
      showToast('登录已过期，请重新登录')
      setTimeout(() => {
        window.location.href = '/login'
      }, 1500)
    } else if (error.response?.status === 404) {
      showToast('接口不存在')
    } else if (error.response?.status === 500) {
      showToast('服务器内部错误')
    } else if (error.message?.includes('Network Error')) {
      showToast('网络连接失败，请检查后端服务是否启动')
    } else {
      showToast(error.response?.data?.message || error.message || '请求失败')
    }
    return Promise.reject(error)
  }
)

export default instance