import {Link} from "react-router-dom";

export default function NavbarButton({button_text, button_link, path}) {
    return (
        <ul className="navbar_item"> <Link to={path}>{button_text}</Link></ul>
    )
}