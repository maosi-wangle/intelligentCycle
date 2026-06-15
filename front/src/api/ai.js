import request from '@/utils/axios'

export const aiAsk = (data) => {
  return request.post('/ai/ask', data)
}

export const draftAnswer = (questionId) => {
  return request.post('/ai/draft-answer', { question_id: questionId })
}

export const aiSearch = (keyword) => {
  return request.get('/ai/search', { params: { keyword } })
}