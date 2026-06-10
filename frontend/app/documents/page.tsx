import DocumentsList from "@/components/DocumentsList";

export default function DocumentsPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-3xl">
        <h1 className="mb-6 text-center text-4xl font-bold">
          Documents
        </h1>

        <DocumentsList />
      </div>
    </main>
  );
}