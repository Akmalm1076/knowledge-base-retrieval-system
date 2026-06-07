import UploadForm from "@/components/UploadForm";

export default function UploadPage() {
  return (
    <main className="flex min-h-screen items-center justify-center px-4">
      <div className="w-full max-w-xl">
        <h1 className="mb-6 text-center text-4xl font-bold">
          Upload Document
        </h1>

        <UploadForm />
      </div>
    </main>
  );
}