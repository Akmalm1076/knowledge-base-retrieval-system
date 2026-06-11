export async function searchKnowledgeBase(
  query: string,
  document?: string
) {
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