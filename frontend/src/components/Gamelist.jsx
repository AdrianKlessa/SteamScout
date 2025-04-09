import axios from "axios";
import {useEffect, useState} from "react";
import GameResult from "./GameResult.jsx";

export default function Gamelist({selectedGame, foundGames, includeTag, excludeTag, filterAdultContent}){
    const [recGameInformation, setRecGameInformation] = useState([])


    const baseUrl = new URL(document.location.origin);
    baseUrl.port = document.location.port;
    function getCookie(name) {
        function escape(s) { return s.replace(/([.*+?\^$(){}|\[\]\/\\])/g, '\\$1'); }
        var match = document.cookie.match(RegExp('(?:^|;\\s*)' + escape(name) + '=([^;]*)'));
        return match ? match[1] : null;
    }

    useEffect(()=>{
        if (selectedGame?.value){
            const fetchData = async () => {

                let jwt_token = getCookie('jwt_token');
                if (!jwt_token){
                    window.alert("Login is required to use search functionality.")
                }

                const url = new URL("/api/get-games-by-similarity", baseUrl).href;

                const response = await axios.get(url, {
                    params: { app_id: selectedGame?.value,
                        include_tag: includeTag,
                        exclude_tag: excludeTag,
                        adult_content_filter: filterAdultContent

                    },
                    headers: {"Authorization": `Bearer ${jwt_token}`},
                }).catch((reason)=>{
                    if (reason.response.status===401){
                        window.alert("JWT token is expired; please log in again.")
                    }

                })
                setRecGameInformation(response.data);
            }
            fetchData()
                .catch(console.error);

        }

    },[selectedGame, includeTag, excludeTag, filterAdultContent])

    if (selectedGame){
        const listItems = recGameInformation.map(game =>
            <li key={game.app_id} className="game_result_list_element">
                <GameResult game={game}/>
            </li>
        );

        return (
            <> <span className="result_explanation">Games similar to {selectedGame?.label}:</span>
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