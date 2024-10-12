import Searchbox from "./SearchBox.jsx";
import Gamelist from "./Gamelist.jsx";
import Button from "./Button.jsx";
import {useState} from "react";

export default function GameSearch() {
    const [gameList, setGameList] = useState([]);
    const [selectedGame, setSelectedGame] = useState(null);
    const [includeTag, setIncludeTag] = useState("");
    const [excludeTag, setExcludeTag] = useState("");
    const [filterAdultContent, setFilterAdultContent] = useState(false);

    function handleTyping(){

    }

    function handleSelect(){

    }

    return (
        <div>
            {selectedGame &&
                <h3>{selectedGame?.label} (AppID: {selectedGame?.value})</h3>
            }
            <Searchbox gameList={gameList} selectedGame={selectedGame} setSelectedGame={setSelectedGame}
                       setGameList={setGameList}></Searchbox>
            <label className="search_label">
                <input
                    type="checkbox"
                    checked={filterAdultContent}
                    onChange={e => setFilterAdultContent(e.target.checked)}
                    className="search_input_checkbox"
                />
                Filter Adult Content?
            </label>
            <label className="search_label">
                <input
                    type="text"
                    value={includeTag}
                    onChange={e => setIncludeTag(e.target.value)}
                    className="search_input_text"
                />
                Includes tag
            </label>
            <label className="search_label">
                <input
                    type="text"
                    checked={excludeTag}
                    onChange={e => setExcludeTag(e.target.value)}
                    className="search_input_text"
                />
                Excludes tag
            </label>


            <Gamelist selectedGame={selectedGame} foundGames={gameList} includeTag={includeTag} excludeTag={excludeTag} filterAdultContent={filterAdultContent}></Gamelist>
        </div>
    )
}