import { useApp } from "../context/AppContext";

const stages = [
  {
    key: "mcp_search",
    label: "MCP Search",
  },
  {
    key: "analyze",
    label: "Analyze",
  },
  {
    key: "generate",
    label: "Generate",
  },
  {
    key: "finding",
    label: "Finding",
  },
  {
    key: "human_review",
    label: "Human Review",
  },
];

function getStageIndex(stage) {
  return stages.findIndex((item) => item.key === stage);
}

function RunStatus() {
  const { run, loading } = useApp();

  if (!run && !loading) {
    return null;
  }

  const currentIndex = getStageIndex(run?.current_stage);

  const waitingReview = run?.status === "waiting_review";

  const completed = run?.status === "completed";

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-6 flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-indigo-400">
            Agent Run
          </p>

          <h2 className="mt-1 text-xl font-semibold">Processing Pipeline</h2>
        </div>

        <div
          className={`w-fit rounded-full px-3 py-1.5 text-xs font-medium ${
            waitingReview
              ? "bg-amber-500/10 text-amber-400"
              : completed
                ? "bg-emerald-500/10 text-emerald-400"
                : "bg-indigo-500/10 text-indigo-400"
          }`}
        >
          {waitingReview
            ? "Waiting for review"
            : completed
              ? "Completed"
              : loading
                ? "Processing"
                : run?.status || "Unknown"}
        </div>
      </div>

      <div className="grid gap-2 md:grid-cols-5">
        {stages.map((stage, index) => {
          const isCompleted = currentIndex >= 0 && index < currentIndex;

          const isCurrent = currentIndex === index;

          const isReview = stage.key === "human_review";

          return (
            <div
              key={stage.key}
              className={`relative rounded-xl border p-4 ${
                isCurrent && waitingReview
                  ? "border-amber-500/30 bg-amber-500/5"
                  : isCurrent
                    ? "border-indigo-500/30 bg-indigo-500/5"
                    : isCompleted
                      ? "border-emerald-500/20 bg-emerald-500/5"
                      : "border-slate-800 bg-slate-950"
              }`}
            >
              <div className="flex items-center gap-3">
                <div
                  className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full text-xs font-semibold ${
                    isCurrent && waitingReview
                      ? "bg-amber-500/10 text-amber-400"
                      : isCompleted
                        ? "bg-emerald-500/10 text-emerald-400"
                        : isCurrent
                          ? "bg-indigo-500/10 text-indigo-400"
                          : "bg-slate-800 text-slate-500"
                  }`}
                >
                  {isCompleted ? "✓" : index + 1}
                </div>

                <div className="min-w-0">
                  <p className="text-sm font-medium text-slate-200">
                    {stage.label}
                  </p>

                  {isCurrent && (
                    <p className="mt-0.5 text-[11px] text-slate-500">
                      {isReview && waitingReview
                        ? "Action required"
                        : loading
                          ? "Running..."
                          : "Current stage"}
                    </p>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>
    </section>
  );
}

export default RunStatus;
