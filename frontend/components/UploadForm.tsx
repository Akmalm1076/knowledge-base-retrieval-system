"use client";

import { useState } from "react";
import { uploadDocument } from "@/services/uploadService";

export default function UploadForm() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");

  const handleFileChange = (
    event: React.ChangeEvent<HTMLInputElement>
  ) => {
    const file = event.target.files?.[0] || null;
    setSelectedFile(file);

    setMessage("");
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage("Please select a PDF file.");
      return;
    }

    try {
      const response = await uploadDocument(selectedFile);
      setMessage(response.message);
    } catch (error) {
      setMessage("Upload failed.");
      console.error(error);
    }
  };

  return (
    <div className="rounded-lg border p-6 shadow-sm">
      <div className="space-y-4">
        <input
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          className="block w-full"
        />

        {selectedFile && (
          <p className="text-sm text-gray-600">
            Selected File: {selectedFile.name}
          </p>
        )}

        <button
          onClick={handleUpload}
          className="rounded bg-black px-4 py-2 text-white"
        >
          Upload
        </button>

        {message && (
          <p className="text-sm">
            {message}
          </p>
        )}
      </div>
    </div>
  );
}