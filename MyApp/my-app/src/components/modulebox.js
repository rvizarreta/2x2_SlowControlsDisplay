import '../App.css';
import * as React from 'react';
import Measuring from './measuring';
import { createTheme, colors, ThemeProvider } from '@mui/material';
import { useState, useEffect } from 'react';

// SETTING UP BUTTON THEME
const theme = createTheme({
  palette : {
    primary:{
      main: colors.green[700]
    },
    secondary:{
      main: colors.red[700]
    }
  }
})

// COMPONENT FUNCTION
function ModuleBox({ id, title, units }) {

  const [data, setData] = useState([]);
  const [buttonStatus, setButtonStatus] = useState();

  // GETTING READOUTS STATUS JSON
  const fetchStatus = () => {
    // Getting status
    fetch(`http://localhost:8000/attached_units/${id}/status`, {cache: 'no-cache'})
    .then(response => response.json())
    .then(dict => {
      setData(dict);
    })

    fetch(`http://localhost:8000/attached_units/${id}/crate_status`, {cache: 'no-cache'})
    .then(response => response.json())
    .then(status => {
      setButtonStatus(status);
    })    
  };

  // Fetch the status initially and then set up polling
  useEffect(() => {
    fetchStatus(); // Fetch initial status
    // Set up polling every 10 seconds
    const intervalId = setInterval(fetchStatus, 10000);
    // Clean up the interval when the component unmounts
    return () => clearInterval(intervalId);
  }, [id]);

  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN CARD
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
      <div className="module-container">
        <h2 className="module-title">{title}</h2>
        {units.map((unitName, index) => (
          <React.Fragment key={index}>
            <div className='unit-name'>{unitName.toUpperCase()}</div>
            <div>
            {Object.keys(data).map((readoutName, index2) => (
              console.log(readoutName),
              console.log(index2),
              <React.Fragment key={index2}>
                <Measuring id={id}
                           title={readoutName}
                           status={Boolean(data[readoutName])}
                           button_status={buttonStatus}/>
                <hr style={{margin : '0.5px'}}></hr>
              </React.Fragment>
            ))}  
            </div>
          </React.Fragment>
        ))}
      </div>
    );
  }

export default ModuleBox;