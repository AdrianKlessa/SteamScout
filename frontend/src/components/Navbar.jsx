import NavbarButton from "./NavbarButton.jsx";
import Logo from "./Logo.jsx";

export default function Navbar({navbarLogo}){
    return(
        <div className="navbar_top">
            <Logo navbarLogo={navbarLogo}></Logo>
            <NavbarButton button_text="Game Search" path="/"></NavbarButton>
            <NavbarButton button_text="About" path="/about"></NavbarButton>
            <NavbarButton button_text="Github repo" path="/github"></NavbarButton>
            <NavbarButton button_text="Resources used" path="/resources"></NavbarButton>
        </div>
    )
}