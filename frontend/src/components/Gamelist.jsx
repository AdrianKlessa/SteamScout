import axios from "axios";
import {useEffect, useState} from "react";
import GameResult from "./GameResult.jsx";

export default function Gamelist({selectedGame, foundGames, includeTag, excludeTag, filterAdultContent}){
    const [recGameInformation, setRecGameInformation] = useState([])

    const backend_similarity_url = "http://127.0.0.1:5174/get-games-by-similarity"
    useEffect(()=>{
        if (selectedGame?.value){
            const fetchData = async () => {
                const response = await axios.get(backend_similarity_url, {
                    params: { app_id: selectedGame?.value,
                        include_tag: includeTag,
                        exclude_tag: excludeTag,
                        adult_content_filter: filterAdultContent

                    }
                })
                setRecGameInformation(response.data);
            }
            fetchData()
                .catch(console.error);

        }

    },[selectedGame, includeTag, excludeTag, filterAdultContent])

    if (recGameInformation){
        const listItems = recGameInformation.map(game =>
            <li key={game.app_id} className="game_result_list_element">
                <GameResult game={game}/>
            </li>
        );

        return (
            <> <span className="result_explanation">Games similar to {selectedGame.label}:</span>
            <ul>{listItems}</ul>
            </>
        );
    }
    else{
        return(
            <div>
            </div>
        )
    }
}