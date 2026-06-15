import request from '@/utils/axios'

export const getHotQuestions = () => {
  return request.get('/rankings/hot-questions')
}

export const getUserRankings = () => {
  return request.get('/rankings/users')
}