import { useApp } from "../context/AppContext";

function AnswerCard() {
  const { run } = useApp();

  if (!run?.answer) {
    return null;
  }

  const isWaitingReview = run.status === "waiting_review";

  return (
    <section className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-5 flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-medium uppercase tracking-wider text-indigo-400">
            Generated Answer
          </p>

          <h2 className="mt-1 text-xl font-semibold text-white">Answer</h2>
        </div>

        <span
          className={`shrink-0 rounded-full px-3 py-1 text-xs font-medium ${
            isWaitingReview
              ? "bg-amber-500/10 text-amber-400"
              : "bg-emerald-500/10 text-emerald-400"
          }`}
        >
          {isWaitingReview ? "Waiting for review" : run.status || "Completed"}
        </span>
      </div>

      <div className="rounded-xl border border-slate-800 bg-slate-950 px-5 py-6">
        <p className="whitespace-pre-wrap text-[15px] leading-7 text-slate-300">
          {run.answer}
        </p>
      </div>
    </section>
  );
}

export default AnswerCard;
