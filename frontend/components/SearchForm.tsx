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
    <div className="rounded-xl border p-8 shadow-sm">
      <div className="mb-8">
        <h2 className="text-2xl font-bold">
          🔍 Search Knowledge Base
        </h2>

        <p className="mt-2 text-sm opacity-70">
          Ask questions about your uploaded documents and get AI-generated answers.
        </p>
      </div>

      <div className="space-y-6">
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
            className="w-full rounded-lg border px-4 py-3"
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
            className="w-full rounded-lg border px-4 py-3"
          >

            <option
                value=""
                className="bg-black text-white"
              >
                All Documents
              </option>

              {documents.map((document) => (
                <option
                  key={document}
                  value={document}
                  className="bg-black text-white"
                >
                  {document}
                </option>
              ))}
           
          </select>
        </div>

        <button
          onClick={handleSearch}
          disabled={isSearching}
          className="rounded-lg bg-black px-6 py-3 font-medium text-white transition-opacity disabled:opacity-50"
        >
          {isSearching ? "Searching..." : "Search"}
        </button>

        {validationError && (
          <div className="rounded-lg border-l-4 border-yellow-500 p-4">
            <p>{validationError}</p>
          </div>
        )}

        {error && (
          <div className="rounded-lg border-l-4 border-red-500 p-4">
            <h3 className="mb-2 font-semibold">
              ❌ Error
            </h3>

            <p>{error}</p>
          </div>
        )}

        {answer && (
          <div className="rounded-xl border-l-4 border-green-500 p-5 shadow-sm">
            <h3 className="mb-3 text-lg font-semibold">
              📄 Answer
            </h3>

            <p className="leading-7">
              {answer}
            </p>
          </div>
        )}

        {contextChunks.length > 0 && (
          <div className="space-y-4">
            <div>
              <h3 className="text-xl font-semibold">
                📚 Retrieved Context
              </h3>

              <p className="mt-1 text-sm opacity-70">
                {contextChunks.length} chunk(s) retrieved from the knowledge base
              </p>
            </div>

            {contextChunks.map((chunk, index) => (
              <div
                key={index}
                className="rounded-xl border p-5 shadow-sm"
              >
                <h4 className="mb-3 font-semibold">
                  Chunk {index + 1}
                </h4>

                <p className="whitespace-pre-wrap text-sm leading-6">
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