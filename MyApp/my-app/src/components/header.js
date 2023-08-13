//import react from "react"
import '../App.css';

function Header() {
    return (
        <div className="title-container">
        <div>
        <p className="title">Mx2 Slow Controls Configuration Room</p>
        <p className="subtitle">Turn ON/OFF each unit by pressing the toggle switches. To monitor the output data in real-time go to Grafana.</p>
        </div>
        <div className="title-image"></div>
        </div>
      );
}

export default Header;