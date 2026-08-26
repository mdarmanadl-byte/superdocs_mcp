import { useApp } from "../context/AppContext";

function PileHeader() {
  const { pile, documents } = useApp();

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 px-6 py-5">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
        <div className="min-w-0">
          <p className="text-xs font-medium uppercase tracking-wider text-slate-500">
            Document Pile
          </p>

          <h1 className="mt-1 truncate text-2xl font-semibold text-white">
            {pile?.name || "Untitled Project"}
          </h1>

          <div className="mt-2 flex flex-wrap items-center gap-3 text-xs text-slate-500">
            <span>ID: {pile?.id}</span>

            <span className="text-slate-700">•</span>

            <span>{documents?.length || 0} documents</span>
          </div>
        </div>

        <div className="flex shrink-0 items-center gap-2 rounded-full border border-emerald-500/20 bg-emerald-500/10 px-3 py-1.5 text-xs font-medium text-emerald-400">
          <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />
          Active
        </div>
      </div>
    </section>
  );
}

export default PileHeader;
