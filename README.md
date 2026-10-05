# Weighted Decision Matrix

### A clearer way to make the choices that shape your life.

Choosing a job, a college, a course, or a new place to live can mean weighing very different priorities. A traditional pros-and-cons list gives every point equal space, even when some things matter much more to you than others.

The **Weighted Decision Matrix** turns that choice into a transparent, adjustable comparison. Describe your decision in everyday language and AI suggests options, evaluation criteria, priorities, and scores. You stay in control: change the assumptions, adjust the weights, and see how your priorities affect the result.

> A structured decision-support technique used in fields such as engineering, economics, operations research, and strategic planning—made approachable for everyday decisions.

## When it can help

- Compare job offers by compensation, growth, flexibility, and commute.
- Evaluate colleges or courses by cost, quality, location, and opportunity.
- Weigh a move against the value of community, affordability, and career prospects.
- Bring structure to any choice where several competing factors matter.

## How the matrix works

Each criterion receives an importance **weight** from 1 to 10. Each option receives a **score** from 1 to 10 for that criterion. The matrix multiplies each score by its weight and adds the results:

```text
Weighted total for an option = sum(criterion weight × option score)
```

The totals are normalized to a percentage of the highest possible score, making options easier to compare. A higher result indicates a closer fit with the weights and scores currently in the matrix—not a guaranteed “right” answer. The result is only as useful as its assumptions, so review and adjust the AI suggestions to reflect your own circumstances.

## Use it in three steps

1. **Describe the decision.** Name the alternatives and anything you already know about your priorities.
2. **Review the suggested matrix.** AI creates a starting point with options, criteria, weights, and scores.
3. **Make it yours.** Rename options or criteria, adjust weights and scores, add or remove rows, and compare the updated rankings.

## Built with

| Layer | Technology |
| --- | --- |
| Interface | HTML, JavaScript, Tailwind CSS |
| API | Python, FastAPI |
| AI generation | Cohere API |
| Hosting | Render |

The Cohere API key belongs on the server, never in browser JavaScript or a public repository.

## Run locally

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Set your Cohere API key in the terminal before starting the app:

```bash
export COHERE_API_KEY="your_cohere_api_key"
uvicorn index:app --reload
```

Keep the key private and do not commit it to Git.

Open [http://127.0.0.1:8000](http://127.0.0.1:8000) to use the app, or visit [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the API.

## Deploy on Render

In the Render service settings, use this **Start Command**:

```bash
uvicorn index:app --host 0.0.0.0 --port $PORT
```

In **Environment**, add `COHERE_API_KEY` with your Cohere API key as its value, then save and deploy. Keep the key in Render's environment settings; do not add it to the frontend or commit it to Git.

## API

`POST /ai`

Request:

```json
{
  "user_input": "Should I accept a higher-paying job with a longer commute or choose a more flexible role?"
}
```

The response includes a generated matrix in `data`:

```json
{
  "success": true,
  "data": {
    "title": "Choosing between job offers",
    "options": ["Higher-paying role", "Flexible role"],
    "criteria": []
  }
}
```

## Project files

```text
.
├── controllers/
│   └── ai_controller.py
├── routes/
│   └── ai_routes.py
├── index.html
├── index.py
├── prototype_algorithm.py
├── requirements.txt
└── vercel.json
```

## A note on decisions

This tool is designed to clarify trade-offs, not make important decisions for you. AI-generated scores are suggestions, not objective facts. Use your own knowledge, check the assumptions, and consider advice from people you trust before making high-stakes choices.

---

**Anjana Sundar**
