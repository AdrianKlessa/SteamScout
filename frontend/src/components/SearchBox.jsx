//import Async, { useAsync } from 'react-select/async';
import AsyncSelect from 'react-select/async';
import {useState} from "react";
import axios from "axios";

export default function Searchbox({gameList, selectedGame, setSelectedGame, setGameList}){

    const [inputValue, setInputValue] = useState("");
    const [inputSave, setSave] = useState("");
    // Fetch the games based on the input value
    async function getGamesByName(inputValue) {
        if (!inputValue) return [];  // Return empty array if no input

        try {
            const response = await axios.get('http://127.0.0.1:5000/get-games-by-name', {
                params: { game_name: inputValue }
            });

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