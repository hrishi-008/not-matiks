import { useState } from 'react';

export default function AnswerInput({ onSubmit, disabled }) {
  const [answer, setAnswer] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(answer);
    setAnswer('');
  };

  return (
    <form onSubmit={handleSubmit} className="answer-input">
      <input
        type="number"
        value={answer}
        onChange={e => setAnswer(e.target.value)}
        disabled={disabled}
        placeholder="Your answer"
        required
      />
      <button type="submit" disabled={disabled}>Submit</button>
    </form>
  );
}
