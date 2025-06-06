export default function TimerDisplay({ timeLeft }) {
  return (
    <div className="timer-display">
      <strong>Time Left:</strong> {timeLeft}s
    </div>
  );
}
