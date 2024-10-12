import navbarLogo from './assets/binoculars-svgrepo-com.svg'
import Navbar from "./components/Navbar.jsx";
import './App.css'
import GameSearch from "./components/GameSearch.jsx";

function App() {

    return (
      <div>
          <Navbar navbarLogo={navbarLogo}></Navbar>
          <GameSearch></GameSearch>

      </div>

    )
}
export default App
