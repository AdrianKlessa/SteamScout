export default function About() {
    return (<div>
        <h2>What is SteamScout?</h2>
        SteamScout is a recommendation system that you can use to find similar games to the ones you love.
        You can think about it as a similarity search engine.
        Simply type into the search box the name of one of your favourite games, select it from the dropdown and you'll get results with other Steam games similar to the one you typed in.
        <h2>What data is used to search for great games?</h2>
        By utilizing techniques such as Doc2Vec and Approximate Nearest Neighbor Search, the results take into account:
        <ul>
            <li>The game tags</li>
            <li>The game descriptions (the text that you see on their Steam page)</li>
            <li>User ratings</li>
        </ul>
        Those interested in more technical aspects of the implementation can check out the documentation section of the Github repository. Alternatively, see the "Resources used" tab to find a list of technologies used in the project.
    </div>)
}