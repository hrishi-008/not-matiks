import { useState, useEffect, useRef } from 'react'
import StartScreen from './components/StartScreen'
import QuestionDisplay from './components/QuestionDisplay'
import AnswerInput from './components/AnswerInput'
import TimerDisplay from './components/TimerDisplay'
import ScoreDisplay from './components/ScoreDisplay'
import './App.css'

const BACKEND_URL = 'http://127.0.0.1:5000';

function App() {
  const [gameStarted, setGameStarted] = useState(false)
  const [question, setQuestion] = useState('')
  const [token, setToken] = useState('')
  const [score, setScore] = useState(0)
  const [timeLeft, setTimeLeft] = useState(60)
  const [inputDisabled, setInputDisabled] = useState(false)
  const [feedback, setFeedback] = useState('')
  const timerRef = useRef(null)

  // Fetch a new question from backend
  const fetchQuestion = async () => {
    try {
      const res = await fetch(`${BACKEND_URL}/question`)
      const data = await res.json()
      setQuestion(data.question)
      setToken(data.token)
    } catch (err) {
      setQuestion('Error fetching question')
      setToken('')
    }
  }

  // Start timer and fetch first question when game starts
  useEffect(() => {
    if (gameStarted) {
      setTimeLeft(60)
      setInputDisabled(false)
      setScore(0)
      setFeedback('')
      fetchQuestion()
      timerRef.current = setInterval(() => {
        setTimeLeft(prev => {
          if (prev <= 1) {
            clearInterval(timerRef.current)
            setInputDisabled(true)
            return 0
          }
          return prev - 1
        })
      }, 1000)
    } else {
      clearInterval(timerRef.current)
    }
    return () => clearInterval(timerRef.current)
  }, [gameStarted])

  // Handle answer submission
  const handleAnswer = async (answer) => {
    if (!token) return
    try {
      const res = await fetch(`${BACKEND_URL}/check`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answer, token })
      })
      const data = await res.json()
      if (res.ok) {
        if (data.correct) {
          setScore(s => s + 1)
          setFeedback('Correct!')
        } else {
          setFeedback('Wrong!')
        }
        setQuestion(data.new_question)
        setToken(data.token)
      } else {
        setFeedback(data.error || 'Error')
      }
    } catch (err) {
      setFeedback('Error connecting to backend')
    }
  }

  // Reset state when restarting game
  const handleStart = () => {
    setScore(0)
    setQuestion('')
    setToken('')
    setGameStarted(true)
    setFeedback('')
  }

  return (
    <div>
      {!gameStarted ? (
        <StartScreen onStart={handleStart} />
      ) : (
        <>
          <TimerDisplay timeLeft={timeLeft} />
          <ScoreDisplay score={score} />
          <QuestionDisplay question={question} />
          <AnswerInput onSubmit={handleAnswer} disabled={inputDisabled} />
          {feedback && (
            <div className={`feedback ${feedback === 'Correct!' ? 'correct' : feedback === 'Wrong!' ? 'wrong' : ''}`}>
              {feedback}
            </div>
          )}
          {inputDisabled && (
            <div className="final-score">Time's up! Final Score: {score}</div>
          )}
        </>
      )}
    </div>
  )
}

export default App
