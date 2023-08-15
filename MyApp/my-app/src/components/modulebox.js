import '../App.css';
import * as React from 'react';
import Measuring from './measuring';
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
function ModuleBox({ id, title }) {

  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
  //# RETURN CARD
  //#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---#---
    return (
      <div className="module-container">
        <h2 className="module-title">{title}</h2>
        <div className='unit-name'>MPOD-0</div>
        <div>
          <Measuring />
          <hr style={{margin : '0.5px'}}></hr>
          <Measuring />
          <hr style={{margin : '0.5px'}}></hr>
          <Measuring />
          <hr style={{margin : '0.5px'}}></hr>
        </div>
        
      </div>
    );
  }

export default ModuleBox;