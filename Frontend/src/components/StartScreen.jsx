export default function StartScreen({ onStart }) {
  return (
    <div className="start-screen">
      <h2>Math Quiz Game</h2>
      <button onClick={onStart}>Start Game</button>
    </div>
  );
}
