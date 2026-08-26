import { useState } from "react";
import { reviewRun } from "../api/runs";
import { useApp } from "../context/AppContext";

function HumanReview() {
  const { run, setRun, setError } = useApp();

  const [reviewing, setReviewing] = useState(false);

  if (run?.status !== "waiting_review") {
    return null;
  }

  const handleReview = async (approved) => {
    console.log("APPROVE/REJECT CLICKED:", approved);

    if (!run?.id) {
      console.error("Run ID is missing.");
      setError("Run ID is missing.");
      return;
    }

    try {
      setReviewing(true);
      setError("");

      const data = await reviewRun(run.id, approved);

      console.log("REVIEW RESPONSE:", data);

      setRun(data);
    } catch (error) {
      console.error("REVIEW ERROR:", error);

      setError(error.response?.data?.detail || "Failed to submit review.");
    } finally {
      setReviewing(false);
    }
  };

  return (
    <section className="rounded-2xl border border-amber-500/30 bg-slate-900 p-6">
      <div className="flex gap-4">
        <div className="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-amber-500/10 text-amber-400">
          !
        </div>

        <div className="flex-1">
          <div>
            <p className="text-xs font-medium uppercase tracking-wider text-amber-400">
              Human in the loop
            </p>

            <h2 className="mt-1 text-lg font-semibold">Review Required</h2>

            <p className="mt-2 text-sm leading-6 text-slate-400">
              The agent has paused and is waiting for your decision before
              completing this run.
            </p>
          </div>

          {run.finding?.has_finding && (
            <div className="mt-5 rounded-xl border border-slate-800 bg-slate-950 p-4">
              <p className="text-sm font-medium text-slate-200">
                {run.finding.title}
              </p>

              {run.finding.description && (
                <p className="mt-2 text-sm leading-6 text-slate-400">
                  {run.finding.description}
                </p>
              )}
            </div>
          )}

          <div className="mt-5 flex gap-3">
            <button
              type="button"
              onClick={() => handleReview(false)}
              disabled={reviewing}
              className="rounded-xl border border-slate-700 px-5 py-2.5 text-sm font-medium text-slate-300 transition hover:bg-slate-800 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Reject
            </button>

            <button
              type="button"
              onClick={() => handleReview(true)}
              disabled={reviewing}
              className="rounded-xl bg-emerald-600 px-5 py-2.5 text-sm font-semibold transition hover:bg-emerald-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {reviewing ? "Submitting..." : "Approve"}
            </button>
          </div>
        </div>
      </div>
    </section>
  );
}

export default HumanReview;
