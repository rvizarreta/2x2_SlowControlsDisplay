import '../App.css';
import * as React from 'react';
import Button from '@mui/material/Button';
import { createTheme, colors, ThemeProvider } from '@mui/material';
import { useEffect } from 'react';

// SETTING UP BUTTON THEME
const theme = createTheme({
  palette : {
    primary:{
      main: colors.green[700]
    },
    secondary:{
      main: colors.red[700]
    },
    disabled:{
      main: colors.red[700]
    }
  }
})

// COMPONENT FUNCTION
const Card = ({ id, title, on_message, off_message }) => {

  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# BUTTON STATUS CONFIGURATION
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---

  const [status, setStatus] = React.useState(false); // Initialize status
  const [clicked, setClicked] = React.useState(false);
  const handleClick = () => {
    setClicked((prevClicked) => !prevClicked);
    const endpoint = clicked ? `http://localhost:8000/other_units/${id}/turn-on` : `http://localhost:8000/other_units/${id}/turn-off`;
    fetch(endpoint, {method: "PUT"})
    .then(response => response.json())
    }
  
  const fetchStatus = () => {
    // Getting status
    fetch(`http://localhost:8000/other_units/${id}/status`, {cache: 'no-cache'})
    .then(response => response.json())
    .then(state => {
      const parsedStatus = Boolean(state);
      setStatus(!parsedStatus);
      setClicked(!parsedStatus);
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

  const buttonStyle = {
    width: 82,
    height: 30,
    borderRadius: 0,
  };

  if (off_message === "Disabled") {
    buttonStyle.color = "disabled";
  }

  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN CARD
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
      <div className={clicked ? 'card-off' : 'card-on'}>
        <div style={{display : 'flex', justifyContent : 'space-between'}}>
          <div className="card-title">{title}</div>
          <div style={{marginTop : '8px', paddingRight : '8px'}}>
            <ThemeProvider theme={theme}>
              <div>
                <Button color={clicked ? 'secondary' : 'primary'}
                        variant="contained"
                        style={buttonStyle}
                        onClick={handleClick}
                        disabled={off_message === "Disabled"}>
                        {clicked ? 'OFF' : 'ON'}
                </Button>
              </div>
            </ThemeProvider>
          </div>
        </div>
        <p className={clicked ? 'card-text-off' : 'card-text-on'}>
        {clicked ? off_message : on_message}
        </p>
      </div>
    );
  }

export default Card;