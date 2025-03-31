import NavbarButton from "./NavbarButton.jsx";
import Logo from "./Logo.jsx";

export default function Navbar({navbarLogo}){
    return(
        <div className="navbar_top">
            <Logo navbarLogo={navbarLogo}></Logo>
            <NavbarButton button_text="Game Search" path="/"></NavbarButton>
            <NavbarButton button_text="About" path="/about"></NavbarButton>
            <NavbarButton button_text="Technologies used" path="/resources"></NavbarButton>
            <ul className="navbar_item"><a href="https://github.com/AdrianKlessa/SteamScout">Github repo</a></ul>
            <NavbarButton button_text="Log in" path="/userlogin">Log in</NavbarButton>
        </div>
    )
}