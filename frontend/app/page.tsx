export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-6 text-center">
      <h1 className="text-5xl font-bold mb-4">
        Knowledge Base Retrieval System
      </h1>

      <p className="max-w-2xl text-lg text-gray-600 dark:text-gray-300">
        Upload documents, perform semantic search, and generate AI-powered
        answers using Retrieval-Augmented Generation (RAG).
      </p>
    </main>
  );
}