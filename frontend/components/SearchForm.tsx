"use client";

import { useEffect, useState } from "react";
import { getDocuments } from "@/services/documentService";
import { searchKnowledgeBase } from "@/services/searchService";

export default function SearchForm() {
  const [documents, setDocuments] = useState<string[]>([]);
  const [query, setQuery] = useState("");
  const [selectedDocument, setSelectedDocument] = useState("");
  const [answer, setAnswer] = useState("");
  const [isSearching, setIsSearching] = useState(false);

  useEffect(() => {
    async function fetchDocuments() {
      try {
        const response = await getDocuments();
        setDocuments(response.documents);
      } catch (error) {
        console.error(error);
      }
    }

    fetchDocuments();
  }, []);

  const handleSearch = async () => {
    if (!query.trim()) {
      return;
    }

    try {
      setIsSearching(true);
      setAnswer("");

      const response = await searchKnowledgeBase(
        query,
        selectedDocument || undefined
      );

      setAnswer(response.answer);
    } catch (error) {
      console.error(error);
      setAnswer("Search failed.");
    } finally {
      setIsSearching(false);
    }
  };

  return (
    <div className="rounded-lg border p-6 shadow-sm">
      <div className="space-y-4">
        <div>
          <label
            htmlFor="query"
            className="mb-2 block text-sm font-medium"
          >
            Question
          </label>

          <input
            id="query"
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask a question about your documents..."
            className="w-full rounded border p-2"
          />
        </div>

        <div>
          <label
            htmlFor="document"
            className="mb-2 block text-sm font-medium"
          >
            Document
          </label>

          <select
            id="document"
            value={selectedDocument}
            onChange={(e) => setSelectedDocument(e.target.value)}
            className="w-full rounded border p-2"
          >
            <option value="">
              All Documents
            </option>

            {documents.map((document) => (
              <option
                key={document}
                value={document}
              >
                {document}
              </option>
            ))}
          </select>
        </div>

        <button
          onClick={handleSearch}
          disabled={isSearching}
          className="rounded bg-black px-4 py-2 text-white disabled:opacity-50"
        >
          {isSearching ? "Searching..." : "Search"}
        </button>

        {answer && (
          <div className="rounded border p-4">
            <h3 className="mb-2 font-semibold">
              Answer
            </h3>

            <p>{answer}</p>
          </div>
        )}
      </div>
    </div>
  );
}