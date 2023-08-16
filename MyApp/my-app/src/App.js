import './App.css';
//import react from 'react'
import Header from './components/header';
import Card from './components/card';
import CardList from './components/cardlist';
import ModuleBox from './components/modulebox';
import React, { useState, useEffect } from 'react';

function App() {
  const [othersNames, setOthersNames] = useState([]);
  const [othersData, setOthersData] = useState([]);
  const [modulesData, setModulesData] = useState([]);

  // GETTING allothers JSON
  useEffect(() => {
    fetch("http://localhost:8000/allothers")
      .then(response => response.json())
      .then(data => {
        // Get response JSON
        const others_names = Object.keys(data);
        setOthersNames(others_names)
        // Create othersData based on others_names,
        const newOthersData = [];
        for (let i = 0; i < others_names.length; i += 2) {
          newOthersData.push([
            //console.log(JSON.stringify(othersNames.length))
            <Card id={i}
                  title={others_names[i].toUpperCase()}
                  on_message={data[others_names[i]]["on_message"]}
                  off_message={data[others_names[i]]["off_message"]} />,
            <Card id={i+1}
                  title={others_names[i + 1].toUpperCase()}
                  on_message={data[others_names[i+1]]["on_message"]}
                  off_message={data[others_names[i+1]]["off_message"]} />,
          ]);
        
        }
        setOthersData(newOthersData);
      });
  }, []);

  // GETTING modules JSON
  useEffect(() => {
    fetch("http://localhost:8000/allmodules")
      .then(response => response.json())
      .then(data => {
        // Get response JSON
        const modules_names = Object.keys(data);
        setOthersNames(modules_names)
        // Create modulesData based on modules_names,
        const newModulesData = [];
        for (let i = 0; i < modules_names.length; i += 2) {
          const numericPart = modules_names[i].match(/\d+/)[0]
          const numericValue = parseInt(numericPart, 10)
          const formattedString = `Module ${numericValue}`;
          newModulesData.push([
            <ModuleBox id={i}
                  title={formattedString}
                  units={Object.keys(data[modules_names[i]])}/>,
            //<ModuleBox id={i+1}
            //      title={modules_names[i + 1].toUpperCase()}/>,
          ]);
        
        }
        setModulesData(newModulesData);
      });
  }, []);

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
