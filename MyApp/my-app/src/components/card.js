import '../App.css';
import * as React from 'react';
import Button from '@mui/material/Button';
import { createTheme, colors, ThemeProvider } from '@mui/material';

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
function Card() {
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# BUTTON STATUS CONFIGURATION
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  const [clicked, setClicked] = React.useState(false);
  const handleClick = () => {
    setClicked((prevClicked) => !prevClicked);
  };
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN CARD
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
      <div className={clicked ? 'card-off' : 'card-on'}>
        <div style={{display : 'flex'}}>
          <h2 className="card-title">MPOD Crate</h2>
          <div style={{marginTop : '8px', paddingLeft : '40px'}}>
            <ThemeProvider theme={theme}>
              <div>
                <Button color={clicked ? 'secondary' : 'primary'}
                        variant="contained"
                        style={{width: 82, height: 30, borderRadius: 0}}
                        onClick={handleClick}>
                        {clicked ? 'OFF' : 'ON'}
                </Button>
              </div>
            </ThemeProvider>
          </div>
        </div>
        <p className={clicked ? 'card-text-off' : 'card-text-on'}>
        {clicked ? 'MPOD crate is off. Nothing is supplied to the modules.' : 'MPOD crate is on. Turning it off will affect all modules.'}
        </p>
      </div>
    );
  }

export default Card;