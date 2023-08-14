import './App.css';
//import react from 'react'
import Header from './components/header';
import Card from './components/card';
import CardList from './components/cardlist';
import ModuleBox from './components/modulebox';

function App() {
  const othersData = [
    [<Card />, <Card />],
    [<Card />, <Card />],
  ];
  const modulesData = [
    [<ModuleBox />, <ModuleBox />],
    [<ModuleBox />, <ModuleBox />]
  ];
  return (
    <div className="mother_container">
      <Header />
      <div className='title-container'>
        <div className='modules_group'>
          <div className='circle'>
            <CardList cardData={modulesData}/>
          </div>
        </div>
        <div className='other_units_group'>
          <CardList cardData={othersData}/>
        </div>
      </div>
    </div>
  )
}

export default App;
