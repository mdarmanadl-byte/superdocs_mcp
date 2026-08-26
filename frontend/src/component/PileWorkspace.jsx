import PileHeader from "./PileHeader";
import DocumentUpload from "./DocumentUpload";
import AskForm from "./AskForm";
import RunStatus from "./RunStatus";
import AnswerCard from "./AnswerCard";
import Sources from "./Source";
import FindingCard from "./FindingCard";
import HumanReview from "./HumanReview";

function PileWorkspace() {
  return (
    <div className="space-y-6">
      {/* Project */}
      <PileHeader />

      {/* Documents + Ask */}
      <section className="grid gap-6 lg:grid-cols-2">
        <DocumentUpload />
        <AskForm />
      </section>

      {/* Agent Run */}
      <RunStatus />

      {/* Answer + Sources */}
      <section className="grid gap-6 lg:grid-cols-[minmax(0,1fr)_320px]">
        <AnswerCard />
        <Sources />
      </section>

      {/* Finding */}
      <FindingCard />

      {/* Human Review */}
      <HumanReview />
    </div>
  );
}

export default PileWorkspace;
