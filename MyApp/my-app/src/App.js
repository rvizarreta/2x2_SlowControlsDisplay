import './App.css';
//import react from 'react'
import Header from './components/header';
import Card from './components/card';
import CardList from './components/cardlist';
import ModuleBox from './components/modulebox';
import React, { useState, useEffect } from 'react';

function App() {
  const [othersNames, setOthersNames] = useState([]);

  useEffect(() => {
    fetch("http://localhost:8000/allothers")
      .then(response => response.json())
      .then(data => {
        const others_names = Object.keys(data);
        setOthersNames(others_names)
        console.log(others_names)
      });
  }, []);
  

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
      {othersNames.map((name, index) => (
          <span key={index}>{name} gg </span>
        ))}
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
