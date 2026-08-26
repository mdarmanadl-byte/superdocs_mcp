import { useState } from "react";
import { uploadDocuments } from "../api/documentApi";
import { useApp } from "../context/AppContext";

function DocumentUpload() {
  const { pile, setDocuments, setError } = useApp();

  const [files, setFiles] = useState([]);
  const [uploading, setUploading] = useState(false);
  const [message, setMessage] = useState("");

  const handleFileChange = (event) => {
    const selectedFiles = Array.from(event.target.files || []);

    setFiles((previousFiles) => {
      const existing = new Set(
        previousFiles.map(
          (file) => `${file.name}-${file.size}-${file.lastModified}`,
        ),
      );

      const newFiles = selectedFiles.filter(
        (file) =>
          !existing.has(`${file.name}-${file.size}-${file.lastModified}`),
      );

      return [...previousFiles, ...newFiles];
    });

    setMessage("");
    setError("");
    event.target.value = "";
  };
  const removeFile = (fileToRemove) => {
    setFiles((previousFiles) =>
      previousFiles.filter(
        (file) =>
          !(
            file.name === fileToRemove.name &&
            file.size === fileToRemove.size &&
            file.lastModified === fileToRemove.lastModified
          ),
      ),
    );
  };
  const handleUpload = async () => {
    if (!pile?.id || files.length === 0) {
      return;
    }

    try {
      setUploading(true);
      setMessage("");
      setError("");

      const data = await uploadDocuments(pile.id, files);

      console.log("UPLOAD RESPONSE:", data);
      console.log("filename", data.documents[0].filename);

      setDocuments(data.documents || data);

      setMessage(
        `Documents ${data.documents[0].filename} uploaded successfully.`,
      );
      setFiles([]);
    } catch (error) {
      console.error("UPLOAD ERROR:", error);

      setError(error.response?.data?.detail || "Failed to upload documents.");
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6">
      <div className="mb-5">
        <h3 className="text-lg font-semibold">Upload Documents</h3>

        <p className="mt-1 text-sm text-slate-400">
          Add documents to <span className="text-slate-200">{pile?.name}</span>.
        </p>
      </div>

      <label className="flex min-h-40 cursor-pointer flex-col items-center justify-center rounded-xl border border-dashed border-slate-700 bg-slate-950 px-6 text-center transition hover:border-indigo-500 hover:bg-indigo-500/5">
        <div className="text-3xl">📄</div>

        <p className="mt-3 text-sm font-medium">Choose documents</p>

        <p className="mt-1 text-xs text-slate-500">
          PDF and supported document files
        </p>

        <input
          type="file"
          multiple
          onChange={handleFileChange}
          className="hidden"
        />
      </label>

      {files.length > 0 && (
        <div className="mt-5">
          <div className="mb-3 flex items-center justify-between">
            <p className="text-sm font-medium text-slate-300">Selected files</p>

            <span className="text-xs text-slate-500">
              {files.length} {files.length === 1 ? "file" : "files"}
            </span>
          </div>

          <div className="space-y-2">
            {files.map((file) => (
              <div
                key={`${file.name}-${file.size}-${file.lastModified}`}
                className="flex items-center justify-between rounded-xl border border-slate-800 bg-slate-950 px-4 py-3"
              >
                <div className="flex min-w-0 items-center gap-3">
                  <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-indigo-500/10">
                    📄
                  </div>

                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-slate-200">
                      {file.name}
                    </p>

                    <p className="mt-0.5 text-xs text-slate-500">
                      {(file.size / 1024 / 1024).toFixed(2)} MB
                    </p>
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => removeFile(file)}
                  className="ml-4 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg text-slate-500 transition hover:bg-red-500/10 hover:text-red-400"
                  title="Remove file"
                >
                  ×
                </button>
              </div>
            ))}
          </div>
        </div>
      )}

      {message && <p className="mt-4 text-sm text-emerald-400">{message}</p>}

      <button
        onClick={handleUpload}
        disabled={uploading || files.length === 0}
        className="mt-5 rounded-xl bg-indigo-600 px-5 py-3 text-sm font-semibold transition hover:bg-indigo-500 disabled:cursor-not-allowed disabled:opacity-40"
      >
        {uploading ? "Uploading..." : "Upload Documents"}
      </button>
    </div>
  );
}

export default DocumentUpload;
