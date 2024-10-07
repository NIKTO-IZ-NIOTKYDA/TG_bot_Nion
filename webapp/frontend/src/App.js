import './App.css';

const tg = window.Telegram.WebApp;


function App() {

  tg.ready();

  const onClose = () => {
    tg.close();
  }

  return (
    <div className="App">
      <button onClick={onClose}>Закрыть</button>
    </div>
  );
}

export default App;
