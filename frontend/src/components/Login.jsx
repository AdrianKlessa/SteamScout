import axios from "axios";
import {useState} from "react";
import { useNavigate } from "react-router-dom";

export default function Login() {
    const backend_name_url = "http://127.0.0.1:5000/api/login"
    const [note, setNote] = useState("");
    const [typedUsername, setTypedUsername] = useState("");
    const [typedPassword, setTypedPassword] = useState("");
    const navigate = useNavigate();

    // TODO: Use state for showing that you're logged in, update when JWT is outdated. Might have to start using redux
    async function login(username, password) {
        if (!username || !password) return;  // Return empty array if no input

        try {
            const response = await axios.post(backend_name_url, {
                username: username,
                password: password
            });

            if (response.status!==200){
                setNote("There was an error processing the login request.")
            }else{
                setNote("Successfully logged in!")
                document.cookie = `jwt_token=${response.data.token}`
                navigate("/");
            }
        } catch (error) {
            console.error("logging in :", error);
        }
    }


    return(<div className="login">
            <label className="login_username">
                <input type="text" name="username" required className="login_textfield" onChange={e=> setTypedUsername(e.target.value)}/> Username
            </label>

            <label className="login_password">
                <input type="password" name="password" required className="login_textfield" onChange={e=> setTypedPassword(e.target.value)}/> Password
            </label>
            <label>
                <button className="login_button" type="submit" onClick={e=>login(typedUsername, typedPassword)}>Log in</button>
            </label>
            <label className="login_note">{note}</label>
        </div>
    )
}