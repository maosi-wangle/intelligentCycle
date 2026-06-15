import request from '@/utils/axios'

export const getQuestions = (params) => {
  return request.get('/questions', { params })
}

export const getQuestionDetail = (questionId) => {
  return request.get(`/questions/${questionId}`)
}

export const createQuestion = (data) => {
  return request.post('/questions', data)
}

export const likeQuestion = (questionId) => {
  return request.post(`/questions/${questionId}/like`)
}

export const unlikeQuestion = (questionId) => {
  return request.delete(`/questions/${questionId}/like`)
}

export const collectQuestion = (questionId) => {
  return request.post(`/questions/${questionId}/collect`)
}

export const uncollectQuestion = (questionId) => {
  return request.delete(`/questions/${questionId}/collect`)
}