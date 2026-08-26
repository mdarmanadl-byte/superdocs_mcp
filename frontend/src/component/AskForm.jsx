import { useState } from "react";
import { askDocuments } from "../api/askApi";
import { useApp } from "../context/AppContext";

function AskForm() {
  const { pile, setRun, setLoading, setError } = useApp();

  const [query, setQuery] = useState("");

  const handleAsk = async (event) => {
    event.preventDefault();

    if (!pile?.id || !query.trim()) return;

    try {
      setLoading(true);
      setError("");

      const data = await askDocuments(pile.id, query.trim());

      console.log("ASK RESPONSE:", data);

      setRun({
        ...data,
        id: data.run_id,
      });
    } catch (error) {
      console.error("ASK ERROR:", error);

      setError(
        error.response?.data?.detail || "Failed to process your question.",
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-5">
        <h3 className="text-lg font-semibold">Ask your documents</h3>

        <p className="mt-1 text-sm text-slate-400">
          Ask a question using the documents in this pile.
        </p>
      </div>

      <form onSubmit={handleAsk}>
        <textarea
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          rows={4}
          placeholder="What does the document say about..."
          className="w-full resize-none rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm text-slate-200 outline-none placeholder:text-slate-600 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
        />

        <div className="mt-4 flex justify-end">
          <button
            type="submit"
            disabled={!query.trim()}
            className="rounded-xl bg-indigo-600 px-6 py-3 text-sm font-semibold transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Ask Question
          </button>
        </div>
      </form>
    </div>
  );
}

export default AskForm;
