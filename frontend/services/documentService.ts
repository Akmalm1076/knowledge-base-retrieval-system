export async function getDocuments() {
  const response = await fetch(
    "http://localhost:8000/api/v1/documents"
  );

  if (!response.ok) {
    throw new Error("Failed to fetch documents");
  }

  return response.json();
}