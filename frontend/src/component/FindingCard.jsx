import { useApp } from "../context/AppContext";

function FindingCard() {
  const { run } = useApp();

  const finding = run?.finding;

  if (!finding?.has_finding) {
    return null;
  }

  return (
    <section className="rounded-2xl border border-amber-500/30 bg-slate-900 p-6">
      <div className="flex gap-4">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-amber-500/10 text-amber-400">
          !
        </div>

        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-3">
            <h2 className="text-lg font-semibold">
              {finding.title || "Document Finding"}
            </h2>

            {finding.severity && (
              <span className="rounded-full bg-amber-500/10 px-3 py-1 text-xs text-amber-400">
                {finding.severity}
              </span>
            )}
          </div>

          {finding.type && (
            <p className="mt-1 text-xs uppercase tracking-wider text-slate-500">
              {finding.type}
            </p>
          )}

          {finding.description && (
            <p className="mt-4 leading-6 text-slate-300">
              {finding.description}
            </p>
          )}
        </div>
      </div>
    </section>
  );
}

export default FindingCard;
