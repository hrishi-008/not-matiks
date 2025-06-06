export default function QuestionDisplay({ question }) {
  return (
    <div className="question-display">
      <h3>Question:</h3>
      <div>{question}</div>
    </div>
  );
}
