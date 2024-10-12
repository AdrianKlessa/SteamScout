import navbarLogo from './assets/binoculars-svgrepo-com.svg'
import Navbar from "./components/Navbar.jsx";
import './App.css'
import GameSearch from "./components/GameSearch.jsx";
import {BrowserRouter, Routes, Route } from "react-router-dom";
import About from "./components/About.jsx";
import Resources from "./components/Resources.jsx";
import Github from "./components/Github.jsx";

function App() {

    return (
      <div>
          <BrowserRouter>
          <Navbar navbarLogo={navbarLogo}></Navbar>
              <Routes>
                  <Route path="/" element={<GameSearch/>}/>
                  <Route path="/about" element={<About/>}/>
                  <Route path="/github" element={<Github/>}/>
                  <Route path="/resources" element={<Resources/>}/>
              </Routes>

          </BrowserRouter>
      </div>

    );
}
export default App
