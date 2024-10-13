export default function Resources() {
    return (<div>
        The current iteration of SteamScout is a web application with completely separate frontend and backend.
        Previously, <a href="https://github.com/gradio-app/gradio" className="inline_link">Gradio</a> was used to
        quickly create (a prototype for?) the frontend but a few months later I decided to work on a proper, modern web
        application.
        <h2>Backend technologies:</h2>
        <ul>
            <li><a href="https://flask.palletsprojects.com/en/3.0.x/" className="inline_link">Flask</a> for easy
                creation of a Python backend
            </li>
            <li><a href="https://radimrehurek.com/gensim/index.html" className="inline_link">Gensim</a> for easy-to-use
                Python implementation of Doc2Vec
            </li>
            <li><a href="https://github.com/jina-ai/vectordb/" className="inline_link">Vectordb</a> for storing
                vectorized game tags & descriptions with <a
                    href="https://en.wikipedia.org/wiki/Hierarchical_navigable_small_world"
                    className="inline_link">HNSW</a> search support
            </li>
            <li><a href="https://www.sqlite.org/" className="inline_link">SQLite</a> for storing
                general game data (names, ids, tags in their text form etc.)
            </li>
            <li><a href="https://gunicorn.org/" className="inline_link">Gunicorn</a> for serving the Flask app outside a
                development environment
            </li>
        </ul>
        <h2>Frontend technologies:</h2>
        <ul>
            <li><a href="https://vite.dev/" className="inline_link">Vite</a> for fast frontend build time & hot reload
            </li>
            <li><a href="https://react.dev/" className="inline_link">React</a> for modular component
                creation
            </li>
            <ul>
                <li><a href="https://reactrouter.com/en/main" className="inline_link">React Router</a> for... routing to tabs such as this one</li>
            </ul>
            <li><a href="https://nginx.org/en/" className="inline_link">Nginx</a> for serving the website
            </li>
            <li><a href="https://axios-http.com/" className="inline_link">Axios</a> for API requests
            </li>
        </ul>
        <h2>Others:</h2>
        <ul>
            <li><a href="https://www.docker.com/" className="inline_link">Docker</a> for easily reproducible and
                scalable application building and deployment
            </li>
            <ul>
                <li><a href="https://docs.docker.com/compose/" className="inline_link">Docker compose</a> for building &
                    running the frontend and backend as one application
                </li>
            </ul>
            <li><a href="https://github.com/features/actions" className="inline_link">Github actions</a> for automatic unit testing when pushing to the Github repository
            </li>
        </ul>
    </div>)
}