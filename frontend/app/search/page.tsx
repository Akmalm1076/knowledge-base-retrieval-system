import SearchForm from "@/components/SearchForm";

export default function SearchPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-4xl">
        <h1 className="mb-6 text-center text-4xl font-bold">
          Search Knowledge Base
        </h1>

        <SearchForm />
      </div>
    </main>
  );
}