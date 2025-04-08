import AsyncSelect from 'react-select/async';
import {useState} from "react";
import axios from "axios";

export default function Searchbox({gameList, selectedGame, setSelectedGame, setGameList}){

    const [inputValue, setInputValue] = useState("");
    const [inputSave, setSave] = useState("");

    const baseUrl = new URL(document.location.origin);
    baseUrl.port = document.location.port;
    function getCookie(name) {
        function escape(s) { return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, '\\$1'); }
        var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
        return match ? match[1] : null;
    }

    // Fetch the games based on the input value
    async function getGamesByName(inputValue) {
        if (!inputValue) return [];  // Return empty array if no input
        let jwt_token = getCookie('jwt_token');
        if (!jwt_token){
            window.alert("Login is required to use search functionality.")
        }
        const url = new URL("/api/get-games-by-name", baseUrl).href;
        try {
            const response = await axios.get(url, {
                params: { game_name: inputValue },
                headers: {"Authorization": `Bearer ${jwt_token}`},
            });
            if (response.status===401){
                window.alert("JWT token is expired; please log in again.")
            }
            // Convert the response data to options for the dropdown
            return response.data.map(game => ({
                value: game.app_id,
                label: game.game_name
            }));
        } catch (error) {
            console.error("Error finding game names:", error);
            return [];  // Return empty array in case of error
        }
    }

    return(
        <div className="searchbox">
            <AsyncSelect
                value ={selectedGame}
                loadOptions={getGamesByName}
                onInputChange={(newValue) => {
                setInputValue(newValue);
                setSave(newValue);  // Save the current input value
            }}
                inputValue={inputValue}
                //onChange={setSelectedGame} // Update the selected game when one is chosen
                onChange={(selection)=>{
                    setSelectedGame(selection);}
                }
                placeholder="Start typing to find games"
                onFocus={() => {
                    setInputValue(inputSave); // keeps the input
                    setSave(""); // prevents undesired placeholder value
                }}
                cacheOptions
                defaultOptions={false}  // Prevent loading initial options
            />
        </div>
    )
}