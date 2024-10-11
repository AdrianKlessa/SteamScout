import axios from "axios";
import {useEffect, useState} from "react";

export default function Gamelist({selectedGame, foundGames, includeTag, excludeTag, filterAdultContent}){
    const [recGameInformation, setRecGameInformation] = useState([])
    const backend_port = import.meta.env.VITE_FLASK_PORT
    const backend_similarity_url = `http://127.0.0.1:${backend_port}/get-games-by-similarity`
    useEffect(()=>{
        if (selectedGame?.value){
            console.log(selectedGame);
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
        console.log("HERE!")
        console.log(recGameInformation)
        const listItems = recGameInformation.map(game =>
            <li key={game.app_id}>
                {game.game_name}  | O: {game.overall_score} | R: {game.review_score} | T: {game.tags_similarity} | D: {game.description_similarity}
            </li>
        );

        return (
            <ul>{listItems}</ul>
        );
    }
    else{
        return(
            <div>
            </div>
        )
    }
}