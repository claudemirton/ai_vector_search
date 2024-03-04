# ai_vector_search
Python script using a vector database - AstraDB, Open AI text embedding API, HuggingFace model and Langchain for implementing a basic vector search. Script originally developed by @kubowania and with minor updates by me.

Please note that firstly you have to generate an OpenAI API key on [OpenAI API](https://openai.com) and set that key as environment variable on your OS with the following name:
OPENAI_API_KEY

After that, we also have to set up an account on [Astra DB platform](https://accounts.datastax.com/session-service/v1/login) and create the following environment variables as well:
* ASTRA_DB_TOKEN
* ASTRA_DB_END_POINT
* ASTRA_DB_KEYSPACE
* ASTRA_DB_COLLECTION

Video for reference: [Ania Kubow's tutorial](https://www.youtube.com/watch?v=PR7xz5vQKGg)
