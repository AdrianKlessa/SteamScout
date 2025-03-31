import navbarLogo from './assets/binoculars-svgrepo-com.svg'
import Navbar from "./components/Navbar.jsx";
import './App.css'
import GameSearch from "./components/GameSearch.jsx";
import {BrowserRouter, Routes, Route } from "react-router-dom";
import About from "./components/About.jsx";
import Resources from "./components/Resources.jsx";
import Login from "./components/Login.jsx";

function App() {

    //TODO: Don't show login if logged in and JWT is still valid. Use redux state for this
    return (
      <div>
          <BrowserRouter>
          <Navbar navbarLogo={navbarLogo}></Navbar>
              <Routes>
                  <Route path="/" element={<GameSearch/>}/>
                  <Route path="/about" element={<About/>}/>
                  <Route path="/resources" element={<Resources/>}/>
                  <Route path="/userlogin" element={<Login/>}/>
              </Routes>

          </BrowserRouter>
      </div>

    );
}
export default App
