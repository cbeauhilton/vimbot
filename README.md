# VIMbot

VIMbot is a FastAPI-based web application
providing an interactive conversational interface
for querying and retrieving information from a medical document knowledge base.
The knowledge base is built using mkdocs, so this code is easily adaptable to any markdown-based knowledge repository.

## Features

- Interactive conversational interface for querying a medical knowledge base.
- Integration with Ragatouille for document indexing and retrieval.
- FastAPI backend for handling HTTP requests and responses.
- Jinja2 templates for rendering HTML pages.
- HTMX for dynamic interactions, along with supplementary JavaScript.
- Tailwind CSS for styling, with additional CSS as needed.
- SQLite databases for storing documents, embeddings, and logs.
- Docker Compose configuration for easy deployment.

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/your-username/vimbot.git
   cd vimbot
   ```

2. Install the required dependencies using Poetry:

   ```sh
   poetry install
   ```

3. Set up the necessary environment variables in a `.env` file:

   ```sh
   FROM_EMAIL=your-email@example.com
   SOURCE_URL=https://your-source-url.com
   POSTMARK_API_KEY=your-postmark-api-key
   OPENAI_API_KEY=sk-gibberish
   ANTHROPIC_API_KEY=sk-mumbo-jumbo
   GROQ_API_KEY=gsk_babba_boo
   ```

4. Run the application using Docker Compose:

   ```sh
   docker-compose up -d
   ```

5. Access the application in your web browser at `http://localhost:8092`.

## Usage

- Enter your query in the input field on the home page and press Enter or click the Submit button.
- The application processes your query, retrieves relevant information from the knowledge base, and displays the response.
- Continue the conversation or start a new one.
- Provide feedback on the response by clicking the appropriate buttons.
- The application includes dropdowns for disclaimers and explanations on how it works—modify these to suit your needs.

## Philosophy

- strike a balance between off-the-shelf tools (e.g. `Ragatouille`) and custom-made solutions (e.g. `htmx` + `FastAPI` >> `streamlit`)
- for most LLM functionality, prefer base libraries or light derivations over large frameworks
- modular API and backend, locality-of-control frontend
- pluggable
- don't take the philosophy too seriously

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgements

- [Ragatouille](https://pypi.org/project/ragatouille/)
  - and [Simon Willison's writeup](https://github.com/simonw/til/blob/main/llms/colbert-ragatouille.md)
- [ColBERT](https://github.com/stanford-futuredata/ColBERT)
- [FastAPI](https://fastapi.tiangolo.com/)
- [HTMX](https://htmx.org/)
- [Tailwind CSS](https://tailwindcss.com/)

## Resources/To-Do

- Implement a separate server for the embeddings, a la <https://github.com/bclavie/RAGatouille/pull/92/files> (will probably speed things up a bit).
- Switch over to structured generation, probably using [Outlines](https://github.com/outlines-dev/outlines/), a la this [HuggingFace cookbook](https://huggingface.co/learn/cookbook/en/structured_generation) (also may speed things up, and get more metadata goodness)
- Consider adding a [semantic cache](https://huggingface.co/learn/cookbook/en/semantic_cache_chroma_vector_database)
- sqlite streaming backups to S3-compatible object storage using [litestream](https://litestream.io/)
