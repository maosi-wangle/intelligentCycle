import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getQuestions, getQuestionDetail, createQuestion, likeQuestion, unlikeQuestion, collectQuestion, uncollectQuestion } from '@/api/questions'
import { getAnswers, createAnswer, likeAnswer, unlikeAnswer, acceptAnswer } from '@/api/answers'

export const useQuestionStore = defineStore('question', () => {
  const questions = ref([])
  const questionDetail = ref(null)
  const answers = ref([])
  const total = ref(0)

  const loadQuestions = async (params = {}) => {
    const res = await getQuestions(params)
    questions.value = res.items
    total.value = res.total
    return res
  }

  const loadQuestionDetail = async (questionId) => {
    const res = await getQuestionDetail(questionId)
    questionDetail.value = res
    return res
  }

  const loadAnswers = async (questionId, params = {}) => {
    const res = await getAnswers(questionId, params)
    answers.value = res.items
    return res
  }

  const addQuestion = async (data) => {
    const res = await createQuestion(data)
    return res
  }

  const addAnswer = async (questionId, content) => {
    const res = await createAnswer(questionId, { content })
    return res
  }

  const toggleLikeQuestion = async (questionId) => {
    if (questionDetail.value?.is_liked) {
      await unlikeQuestion(questionId)
      questionDetail.value.is_liked = false
      questionDetail.value.like_count--
    } else {
      await likeQuestion(questionId)
      questionDetail.value.is_liked = true
      questionDetail.value.like_count++
    }
  }

  const toggleCollectQuestion = async (questionId) => {
    if (questionDetail.value?.is_collected) {
      await uncollectQuestion(questionId)
      questionDetail.value.is_collected = false
    } else {
      await collectQuestion(questionId)
      questionDetail.value.is_collected = true
    }
  }

  const toggleLikeAnswer = async (answerId) => {
    const answer = answers.value.find(a => a.id === answerId)
    if (answer?.is_liked) {
      await unlikeAnswer(answerId)
      answer.is_liked = false
      answer.like_count--
    } else {
      await likeAnswer(answerId)
      answer.is_liked = true
      answer.like_count++
    }
  }

  const confirmAcceptAnswer = async (answerId) => {
    const res = await acceptAnswer(answerId)
    const answer = answers.value.find(a => a.id === answerId)
    if (answer) {
      answer.is_accepted = true
    }
    return res
  }

  return {
    questions,
    questionDetail,
    answers,
    total,
    loadQuestions,
    loadQuestionDetail,
    loadAnswers,
    addQuestion,
    addAnswer,
    toggleLikeQuestion,
    toggleCollectQuestion,
    toggleLikeAnswer,
    confirmAcceptAnswer
  }
})