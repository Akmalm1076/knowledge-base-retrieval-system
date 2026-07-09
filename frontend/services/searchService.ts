export interface RetrievedContext {
  chunk_text: string;
  document_name: string;
  found_by: {
    semantic: boolean;
    keyword: boolean;
  };
  reranker_score: number;
}

export interface SearchResponse {
  query: string;
  document?: string;
  answer: string;
  context: RetrievedContext[];
}

export async function searchKnowledgeBase(
  query: string,
  document?: string
): Promise<SearchResponse> {

  const response = await fetch(
    "http://localhost:8000/api/v1/search",
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        query,
        document,
      }),
    }
  );

  if (!response.ok) {
    throw new Error("Search failed");
  }

  return response.json();
}