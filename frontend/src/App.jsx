//import { useState } from 'react'
//import reactLogo from './assets/react.svg'
//import viteLogo from '/vite.svg'
import navbarLogo from './assets/binoculars-svgrepo-com.svg'
import Navbar from "./components/Navbar.jsx";
import './App.css'
import GameSearch from "./components/GameSearch.jsx";

function App() {
  //const [count, setCount] = useState(0)

    return (
      <div>
          <Navbar navbarLogo={navbarLogo}></Navbar>
          <GameSearch></GameSearch>

      </div>

    )
/*
  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
*/
}
export default App
