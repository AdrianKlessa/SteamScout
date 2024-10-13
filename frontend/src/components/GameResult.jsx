export default function GameResult({game}){

    const store_link = `https://store.steampowered.com/app/${game.app_id}/`
    const overall_score = Math.trunc(game.overall_score*100)
    const review_score = Math.trunc(game.review_score*100)
    const description_score = Math.trunc(game.description_similarity*100)
    const tags_score = Math.trunc(game.tags_similarity*100)

    const tags = game.tags.split(',')
    let tags_element;
    if (!tags.includes("nan")){
        tags_element = tags.map((tag) =>
            <li key={tag} className="game_result_tag">{tag}</li>
        )
    }else{
        tags_element = <li key="nan">No tags found</li>
    }

    return (
        <div className="game_result">
            <div className="game_result_main">
                <span className="game_result_title">{game.game_name}</span>
                <a href={store_link}>Store page</a>
                <div className="game_scores">
                    <ul>
                        <li>Overall score: {overall_score}</li>
                        <li>Tags similarity: {review_score}</li>
                        <li>Description similarity: {description_score}</li>
                        <li>Review score score: {tags_score}</li>
                    </ul>
                </div>
            </div>
            <div className="game_result_tags">
                <span>Tags:</span>
                <ul>
                    {tags_element}
                </ul>
            </div>
        </div>
    )
}