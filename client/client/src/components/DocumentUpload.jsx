import { useState } from "react";
import { Upload, FileText, X, CheckCircle2, Loader2 } from "lucide-react";
import { uploadDocument } from "../services/api";

export default function DocumentUpload({
  onDocumentUploaded,
  onDocumentRemoved,
}) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [uploadedDocument, setUploadedDocument] = useState(null);

  const handleFileChange = (event) => {
    const selectedFile = event.target.files?.[0];

    if (!selectedFile) return;

    if (selectedFile.size > 10 * 1024 * 1024) {
      setMessage("File size must be less than 10 MB.");
      return;
    }

    setFile(selectedFile);
    setMessage("");
  };

  const handleUpload = async () => {
    if (!file) {
      setMessage("Please select a document first.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const data = await uploadDocument(file);

      if (!data?.document_id) {
        throw new Error(
          "Document ID was not returned by the server."
        );
      }

      setUploadedDocument(data);
      setMessage("");

      if (onDocumentUploaded) {
        onDocumentUploaded(data);
      }

      setFile(null);
    } catch (error) {
      console.error("Document upload error:", error);

      const errorMessage =
        error?.response?.data?.detail ||
        error?.message ||
        "Document upload failed.";

      setMessage(errorMessage);
    } finally {
      setLoading(false);
    }
  };

  const handleRemove = () => {
    setUploadedDocument(null);
    setFile(null);
    setMessage("");

    if (onDocumentRemoved) {
      onDocumentRemoved();
    }
  };

  return (
    <div
      style={{
        width: "100%",
        marginBottom: "18px",
        border: "1px solid rgba(255,255,255,0.08)",
        borderRadius: "18px",
        background:
          "linear-gradient(145deg, rgba(255,255,255,0.045), rgba(255,255,255,0.018))",
        boxShadow:
          "0 10px 35px rgba(0,0,0,0.18)",
        overflow: "hidden",
      }}
    >
      {!uploadedDocument ? (
        <div
          style={{
            padding: "20px",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "12px",
              marginBottom: "16px",
            }}
          >
            <div
              style={{
                width: "42px",
                height: "42px",
                borderRadius: "12px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background:
                  "rgba(99,102,241,0.12)",
                color: "#818cf8",
              }}
            >
              <FileText size={21} />
            </div>

            <div>
              <h3
                style={{
                  margin: 0,
                  fontSize: "15px",
                  fontWeight: 600,
                  color: "inherit",
                }}
              >
                Ask from your own document
              </h3>

              <p
                style={{
                  margin: "4px 0 0",
                  fontSize: "12px",
                  opacity: 0.55,
                }}
              >
                Upload a PDF, TXT or DOCX and chat with it
              </p>
            </div>
          </div>

          <label
            htmlFor="medibot-document-upload"
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              minHeight: "125px",
              padding: "20px",
              borderRadius: "14px",
              border: "1px dashed rgba(129,140,248,0.35)",
              background:
                "rgba(129,140,248,0.035)",
              cursor: loading ? "not-allowed" : "pointer",
              transition: "all 0.2s ease",
            }}
          >
            <div
              style={{
                width: "40px",
                height: "40px",
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background:
                  "rgba(129,140,248,0.12)",
                color: "#818cf8",
                marginBottom: "10px",
              }}
            >
              <Upload size={19} />
            </div>

            <span
              style={{
                fontSize: "13px",
                fontWeight: 600,
                marginBottom: "4px",
              }}
            >
              Choose a document
            </span>

            <span
              style={{
                fontSize: "11px",
                opacity: 0.45,
              }}
            >
              PDF, TXT or DOCX • Max 10 MB
            </span>

            <input
              id="medibot-document-upload"
              type="file"
              accept=".pdf,.txt,.docx"
              onChange={handleFileChange}
              disabled={loading}
              style={{
                display: "none",
              }}
            />
          </label>

          {file && (
            <div
              style={{
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: "12px",
                marginTop: "12px",
                padding: "11px 13px",
                borderRadius: "12px",
                background:
                  "rgba(255,255,255,0.045)",
                border:
                  "1px solid rgba(255,255,255,0.07)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  minWidth: 0,
                }}
              >
                <FileText
                  size={17}
                  style={{
                    color: "#818cf8",
                    flexShrink: 0,
                  }}
                />

                <span
                  style={{
                    fontSize: "12px",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {file.name}
                </span>
              </div>

              <button
                type="button"
                onClick={() => {
                  setFile(null);
                  setMessage("");
                }}
                disabled={loading}
                style={{
                  border: "none",
                  background: "transparent",
                  color: "inherit",
                  opacity: 0.5,
                  cursor: "pointer",
                  padding: "3px",
                }}
              >
                <X size={16} />
              </button>
            </div>
          )}

          {file && (
            <button
              type="button"
              onClick={handleUpload}
              disabled={loading}
              style={{
                width: "100%",
                marginTop: "12px",
                height: "42px",
                border: "none",
                borderRadius: "11px",
                background:
                  "linear-gradient(135deg, #6366f1, #8b5cf6)",
                color: "#fff",
                fontSize: "13px",
                fontWeight: 600,
                cursor: loading
                  ? "not-allowed"
                  : "pointer",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: "8px",
                opacity: loading ? 0.7 : 1,
                boxShadow:
                  "0 6px 20px rgba(99,102,241,0.22)",
              }}
            >
              {loading ? (
                <>
                  <Loader2
                    size={16}
                    className="spin"
                  />
                  Processing document...
                </>
              ) : (
                <>
                  <Upload size={16} />
                  Upload & Process
                </>
              )}
            </button>
          )}

          {message && (
            <div
              style={{
                marginTop: "10px",
                padding: "9px 11px",
                borderRadius: "10px",
                fontSize: "12px",
                color: "#fca5a5",
                background:
                  "rgba(239,68,68,0.08)",
                border:
                  "1px solid rgba(239,68,68,0.12)",
              }}
            >
              {message}
            </div>
          )}
        </div>
      ) : (
        <div
          style={{
            padding: "16px",
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: "12px",
            }}
          >
            <div
              style={{
                display: "flex",
                alignItems: "center",
                gap: "12px",
                minWidth: 0,
              }}
            >
              <div
                style={{
                  width: "42px",
                  height: "42px",
                  borderRadius: "12px",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  background:
                    "rgba(34,197,94,0.1)",
                  color: "#4ade80",
                  flexShrink: 0,
                }}
              >
                <CheckCircle2 size={21} />
              </div>

              <div
                style={{
                  minWidth: 0,
                }}
              >
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: "6px",
                    marginBottom: "4px",
                  }}
                >
                  <span
                    style={{
                      fontSize: "12px",
                      color: "#4ade80",
                      fontWeight: 600,
                    }}
                  >
                    Document ready
                  </span>
                </div>

                <div
                  style={{
                    fontSize: "13px",
                    fontWeight: 600,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {uploadedDocument.filename}
                </div>

                <div
                  style={{
                    fontSize: "11px",
                    opacity: 0.45,
                    marginTop: "3px",
                  }}
                >
                  {uploadedDocument.chunks || 0} chunks processed
                </div>
              </div>
            </div>

            <button
              type="button"
              onClick={handleRemove}
              disabled={loading}
              style={{
                display: "flex",
                alignItems: "center",
                gap: "5px",
                padding: "7px 10px",
                borderRadius: "9px",
                border:
                  "1px solid rgba(255,255,255,0.08)",
                background:
                  "rgba(255,255,255,0.035)",
                color: "inherit",
                opacity: 0.65,
                fontSize: "11px",
                cursor: "pointer",
                flexShrink: 0,
              }}
            >
              <X size={14} />
              Remove
            </button>
          </div>

          <div
            style={{
              marginTop: "13px",
              padding: "10px 12px",
              borderRadius: "10px",
              background:
                "rgba(34,197,94,0.06)",
              border:
                "1px solid rgba(34,197,94,0.1)",
              fontSize: "11px",
              color: "#86efac",
            }}
          >
            ✓ MediBot will now answer questions
            using this document.
          </div>
        </div>
      )}
    </div>
  );
}