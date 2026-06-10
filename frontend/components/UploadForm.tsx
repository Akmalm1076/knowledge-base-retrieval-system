"use client";

import { useRef, useState } from "react";
import { uploadDocument } from "@/services/uploadService";

export default function UploadForm() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [message, setMessage] = useState("");
  const [isUploading, setIsUploading] = useState(false);
  const [messageType, setMessageType] = useState<
    "success" | "error" | ""
  >("");
  const fileInputRef = useRef<HTMLInputElement>(null);
  const handleFileChange = (
  event: React.ChangeEvent<HTMLInputElement>
) => {
  const file = event.target.files?.[0] || null;

  setMessage("");
  setMessageType("");

  if (!file) {
    setSelectedFile(null);
    return;
  }

  if (file.type !== "application/pdf") {
    setSelectedFile(null);
    setMessage("Only PDF files are allowed.");
    setMessageType("error");
    return;
  }

  setSelectedFile(file);
};  


  const handleUpload = async () => {
    if (!selectedFile) {
      setMessage("Please select a PDF file.");
      setMessageType("error");
      return;
    }

    try {
      setIsUploading(true);
      setMessage("");

      const response = await uploadDocument(selectedFile);

      setMessage(response.message);
      setMessageType("success");
      setSelectedFile(null);

      if (fileInputRef.current) {
        fileInputRef.current.value = "";
      }
    } catch (error) {
      setMessage("Upload failed.");
      setMessageType("error");
      console.error(error);
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="rounded-lg border p-6 shadow-sm">
      <div className="space-y-4">
        <input
          ref={fileInputRef}
          type="file"
          accept=".pdf"
          onChange={handleFileChange}
          disabled={isUploading}
          className="block w-full disabled:opacity-50"
        />

        {selectedFile && (
          <p className="text-sm font-medium">
            Selected File: {selectedFile.name}
          </p>
        )}

        <button
          onClick={handleUpload}
          disabled={isUploading}
          className="rounded bg-black px-4 py-2 text-white disabled:opacity-50"
        >
          {isUploading ? "Uploading..." : "Upload"}
        </button>

        {message && (
          <p
            className={`text-sm ${
              messageType === "success"
                ? "text-green-500"
                : "text-red-500"
            }`}
          >
            {message}
          </p>
        )}
      </div>
    </div>
  );
}