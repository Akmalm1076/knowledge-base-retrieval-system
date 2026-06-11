"use client";

import { useEffect, useState } from "react";
import { getDocuments } from "@/services/documentService";

export default function DocumentsList() {
  const [documents, setDocuments] = useState<string[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    async function fetchDocuments() {
      try {
        const response = await getDocuments();
        setDocuments(response.documents);
      } catch (error) {
        console.error(error);
        setError("Failed to load documents.");
      } finally {
        setLoading(false);
      }
    }

    fetchDocuments();
  }, []);

  if (loading) {
    return (
      <div className="rounded-lg border p-6 shadow-sm">
        <p>Loading documents...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-lg border p-6 shadow-sm">
        <p className="text-red-500">{error}</p>
      </div>
    );
  }

  return (
    <div className="rounded-lg border p-6 shadow-sm">
      <h2 className="mb-4 text-xl font-semibold">
        Uploaded Documents ({documents.length})
      </h2>

      {documents.length === 0 ? (
        <p>No documents found.</p>
      ) : (
        <ul className="space-y-2">
          {documents.map((document) => (
            <li
              key={document}
              className="rounded border p-3"
            >
              {document}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}