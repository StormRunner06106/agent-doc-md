# Eshop Natural Language to SQL

A small Streamlit app that turns plain English questions into read-only SQL and runs them against a mock SQLite eshop database.

## Run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

The app works without an API key by using simple built-in prompt rules. If `OPENAI_API_KEY` is set, it uses LangChain with OpenAI to generate SQL from the schema prompt.

To print rows from every table in the terminal:

```bash
python show_db.py
```

You can also point it at another SQLite file or limit the rows per table:

```bash
python show_db.py --db eshop.db --limit 5
```

## Tables

- `users`
- `products`
- `orders`
- `order_items`
