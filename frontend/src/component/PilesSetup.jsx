import { useState } from "react";
import { createPile } from "../api/piles";
import { useApp } from "../context/AppContext";

function PileSetup() {
  const [name, setName] = useState("");

  const { setPile, setLoading, setError, error, pilename, setPileName } =
    useApp();

  const handleCreatePile = async (e) => {
    e.preventDefault();

    if (!name.trim()) return;

    try {
      setLoading(true);
      setError("");

      const data = await createPile(name.trim());

      console.log("CREATE PILE RESPONSE:", data);
      setPileName(name.trim());
      localStorage.setItem("pilename", name.trim());
      localStorage.setItem("pile", data);
      setPile(data);
    } catch (error) {
      console.error("CREATE PILE ERROR:", error);

      setError(error.response?.data?.detail || "Failed to create project.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-xl">
      <div className="mx-auto max-w-xl text-center">
        <div className="mx-auto mb-5 flex h-14 w-14 items-center justify-center rounded-2xl bg-indigo-500/10 text-2xl">
          📚
        </div>

        <h2 className="text-2xl font-semibold">Create a document pile</h2>

        <p className="mt-2 text-sm text-slate-400">
          Give your project a name to get started.
        </p>

        <form onSubmit={handleCreatePile} className="mt-8">
          <input
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="e.g. SuperDocs Research"
            className="w-full rounded-xl border border-slate-700 bg-slate-950 px-4 py-3 text-sm outline-none transition placeholder:text-slate-600 focus:border-indigo-500 focus:ring-2 focus:ring-indigo-500/20"
          />

          {error && (
            <p className="mt-3 text-left text-sm text-red-400">{error}</p>
          )}

          <button
            type="submit"
            disabled={!name.trim()}
            className="mt-4 w-full rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-40"
          >
            Create Project
          </button>
        </form>
      </div>
    </section>
  );
}

export default PileSetup;
