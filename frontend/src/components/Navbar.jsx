import NavbarButton from "./NavbarButton.jsx";
import Logo from "./Logo.jsx";

export default function Navbar({navbarLogo}){
    return(
        <div className="navbar_top">
            <Logo navbarLogo={navbarLogo}></Logo>
            <NavbarButton button_text="Game Search"></NavbarButton>
            <NavbarButton button_text="About"></NavbarButton>
            <NavbarButton button_text="Github repo"></NavbarButton>
            <NavbarButton button_text="Resources used"></NavbarButton>
        </div>
    )
}