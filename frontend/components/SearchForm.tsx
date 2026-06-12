"use client";

import { useEffect, useState } from "react";
import { getDocuments } from "@/services/documentService";
import { searchKnowledgeBase } from "@/services/searchService";

export default function SearchForm() {
  const [documents, setDocuments] = useState<string[]>([]);
  const [query, setQuery] = useState("");
  const [selectedDocument, setSelectedDocument] = useState("");

  const [answer, setAnswer] = useState("");
  const [contextChunks, setContextChunks] = useState<string[]>([]);

  const [error, setError] = useState("");
  const [validationError, setValidationError] = useState("");

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
      setValidationError(
        "Please enter a question before searching."
      );
      return;
    }

    try {
      setValidationError("");
      setError("");

      setAnswer("");
      setContextChunks([]);

      setIsSearching(true);

      const response = await searchKnowledgeBase(
        query,
        selectedDocument || undefined
      );

      setAnswer(response.answer);
      setContextChunks(response.context || []);
    } catch (error) {
      console.error(error);

      setAnswer("");
      setContextChunks([]);

      setError(
        "Search failed. Please try again."
      );
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
            disabled={isSearching}
            value={query}
            onChange={(e) => {
              setQuery(e.target.value);

              if (validationError) {
                setValidationError("");
              }
            }}
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
            disabled={isSearching}
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

        {validationError && (
          <div className="rounded border border-yellow-300 bg-yellow-50 p-3">
            <p>{validationError}</p>
          </div>
        )}

        {error && (
          <div className="rounded border border-red-300 bg-red-50 p-4">
            <h3 className="mb-2 font-semibold">
              Error
            </h3>

            <p>{error}</p>
          </div>
        )}

        {answer && (
          <div className="rounded border border-green-300 bg-green-50 p-4">
            <h3 className="mb-2 font-semibold">
              Answer
            </h3>

            <p>{answer}</p>
          </div>
        )}

        {contextChunks.length > 0 && (
          <div className="space-y-3">
            <h3 className="text-lg font-semibold">
              Retrieved Context
            </h3>

            {contextChunks.map((chunk, index) => (
              <div
                key={index}
                className="rounded border p-4"
              >
                <h4 className="mb-2 font-medium">
                  Chunk {index + 1}
                </h4>

                <p className="whitespace-pre-wrap text-sm">
                  {chunk}
                </p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}