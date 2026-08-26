import { useApp } from "../context/AppContext";

function Sources() {
  const { run } = useApp();

  const sources = run?.sources || [];

  if (!run) {
    return null;
  }

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-5">
        <p className="text-xs font-medium uppercase tracking-wider text-indigo-400">
          Grounding
        </p>

        <div className="mt-1 flex items-center justify-between">
          <h2 className="text-xl font-semibold text-white">Sources</h2>

          <span className="text-xs text-slate-500">{sources.length}</span>
        </div>
      </div>

      {sources.length === 0 ? (
        <div className="rounded-xl border border-slate-800 bg-slate-950 p-5 text-sm text-slate-500">
          No sources available.
        </div>
      ) : (
        <div className="max-h-[430px] space-y-3 overflow-y-auto pr-1">
          {sources.map((source, index) => (
            <div
              key={`${source.document_id || index}-${source.chunk || index}`}
              className="rounded-xl border border-slate-800 bg-slate-950 p-4 transition hover:border-slate-700"
            >
              <div className="flex items-start gap-3">
                <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-indigo-500/10">
                  <span className="text-sm">📄</span>
                </div>

                <div className="min-w-0">
                  <p
                    className="break-words text-sm font-medium text-slate-200"
                    title={source.filename}
                  >
                    {source.filename || "Document"}
                  </p>

                  <p className="mt-1 text-xs text-slate-500">
                    Page {source.page ?? "—"} · Chunk {source.chunk ?? "—"}
                  </p>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </section>
  );
}

export default Sources;
