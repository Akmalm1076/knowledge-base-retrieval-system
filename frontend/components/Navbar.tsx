import Link from "next/link";

export default function Navbar() {
  return (
    <nav className="flex items-center justify-between px-6 py-4 border-b">
      <Link href="/" className="text-xl font-bold">
        KB Retrieval
      </Link>

      <div className="flex gap-6">
        <Link href="/documents">Documents</Link>
        <Link href="/upload">Upload</Link>
        <Link href="/search">Search</Link>
      </div>
    </nav>
  );
}