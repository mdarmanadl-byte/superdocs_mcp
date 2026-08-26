import { useState } from "react";
import { askDocuments } from "./api/piles";
import PileSetup from "./component/PilesSetup";
import { useApp } from "./context/AppContext";
import PileWorkspace from "./component/PileWorkspace";
function App() {
  const [pileId, setPileId] = useState("");
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const { pile, setPile } = useApp();
  const [run, setRun] = useState(null);
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [finding, setFinding] = useState(null);

  const askQuestion = async () => {
    try {
      if (!pileId.trim() || !query.trim()) return;
      setLoading(true);
      setAnswer("");
      setSources([]);
      setFinding(null);
      setRun(null);

      const data = await askDocuments(pileId, query);
      setRun(data);
      setAnswer(data.answer || "");
      setSources(data.sources || []);
      setFinding(data.finding || null);

      console.log(data);
    } catch (error) {
      console.error("Failed to ask documents:", error);
      setAnswer(
        error.response?.data?.detail || "Unable to process the request.",
      );
    } finally {
      setLoading(false);
    }
  };
  const handleClear = () => {
    localStorage.clear();
    setPileId("");
    setPile(null);
    setQuery("");
    setRun(null);
    setAnswer("");
    setSources([]);
    setFinding(null);
    alert("Cleared!");
  };

  return (
    <div className="min-h-screen bg-slate-950 text-white">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-950/90">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">SuperDocs</h1>
            <p className="text-sm text-slate-400">
              Document Intelligence Agent
            </p>
          </div>

          <div className="rounded-full border border-emerald-500/30 bg-emerald-500/10 px-4 py-2 text-sm text-emerald-400">
            <button
              onClick={handleClear}
              // className="bg-red-600 hover:bg-red-700 text-white font-medium py-2 px-4 rounded transition-colors"
            >
              New Project
            </button>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-6 py-8">
        {!pile ? <PileSetup /> : <PileWorkspace />}
      </main>
    </div>
  );
}

function Stage({ name, active }) {
  return (
    <div
      className={`rounded-xl border p-4 ${
        active
          ? "border-indigo-500/40 bg-indigo-500/10"
          : "border-slate-800 bg-slate-950"
      }`}
    >
      <div className="flex items-center gap-3">
        <div
          className={`h-2.5 w-2.5 rounded-full ${
            active ? "bg-indigo-400 animate-pulse" : "bg-slate-700"
          }`}
        />

        <span className="text-sm text-slate-300">{name}</span>
      </div>
    </div>
  );
}

export default App;
