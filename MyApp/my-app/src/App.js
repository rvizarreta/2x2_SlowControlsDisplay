import './App.css';
//import react from 'react'
import Header from './components/header';
import Card from './components/card';

function App() {
  return (
    <div className="mother_container">
      <Header />
      <Card />
      <Card />
      <Card />
    </div>
  )
}

export default App;
