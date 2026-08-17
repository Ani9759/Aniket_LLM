from fastapi import FastAPI, HTTPException

from .schemas import ResearchRequest, ResearchResponse
from .tavily_service import search_web
from .groq_service import generate_answer


app = FastAPI(
    title="Company Research AI",
    description="Live company research using Tavily + Groq",
    version="1.0.0"
)


@app.get("/")
def home():

    return {
        "message": "Company Research AI is running"
    }
@app.get("/health")
def health():

    return {
        "status": "healthy"
    }

@app.post(
    "/research",
    response_model=ResearchResponse
)
def research(request: ResearchRequest):

    try:

        # --------------------------------
        # STEP 1: Search the live internet
        # --------------------------------

        search_response = search_web(
            request.query
        )

        results = search_response.get(
            "results",
            []
        )

        if not results:

            raise HTTPException(
                status_code=404,
                detail="No web search results found."
            )


        # --------------------------------
        # STEP 2: Send results to Groq
        # --------------------------------

        answer = generate_answer(
            request.query,
            results
        )


        # --------------------------------
        # STEP 3: Prepare sources
        # --------------------------------

        sources = []

        for result in results:

            sources.append(
                {
                    "title": result.get("title"),
                    "url": result.get("url")
                }
            )


        # --------------------------------
        # STEP 4: Return response
        # --------------------------------

        return ResearchResponse(
            query=request.query,
            answer=answer,
            sources=sources
        )


    except HTTPException:

        raise


    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )