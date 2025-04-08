
export default function Logo({navbarLogo}) {
    return (
        <div className="logo">
            <img src={navbarLogo} className="navbar_logo" alt="React logo"/>
            <span className="logo_text">Steam game similarity search</span>
        </div>
    )
}