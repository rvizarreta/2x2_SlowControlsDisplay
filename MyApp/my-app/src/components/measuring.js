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

function Measuring(){

  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# BUTTON STATUS CONFIGURATION
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  const [clicked, setClicked] = React.useState(false);
  const handleClick = () => {
    setClicked((prevClicked) => !prevClicked);
  };

  return (
      <div className={clicked ? 'measuring-row-off' : 'measuring-row-on'}>
        <div className='measuring'>
          Light Readout
        </div>
        <ThemeProvider theme={theme}>
          <div style={{paddingLeft : '10px'}}> 
            <Button color={clicked ? 'secondary' : 'primary'}
                    variant="contained"
                    style={{width: 82, height: 30, borderRadius: 0}}
                    onClick={handleClick}>
                    {clicked ? 'OFF' : 'ON'}
            </Button>
          </div>
        </ThemeProvider>
      </div>
  )
}

export default Measuring;