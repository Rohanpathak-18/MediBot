import { useState } from "react";
import {
  Upload,
  FileText,
  X,
  CheckCircle2,
  Loader2,
} from "lucide-react";
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
      setMessage("File must be smaller than 10 MB.");
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
      setFile(null);

      if (onDocumentUploaded) {
        onDocumentUploaded(data);
      }
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
        boxSizing: "border-box",
        marginBottom: "14px",
        padding: "14px",
        borderRadius: "16px",
        background: "#0b0b0d",
        border: "1px solid #202024",
        boxShadow: "0 8px 30px rgba(0, 0, 0, 0.25)",
      }}
    >
      {!uploadedDocument ? (
        <>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: "11px",
              marginBottom: "13px",
            }}
          >
            <div
              style={{
                width: "36px",
                height: "36px",
                borderRadius: "10px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: "#15151a",
                border: "1px solid #292932",
                color: "#a78bfa",
              }}
            >
              <FileText size={18} />
            </div>

            <div>
              <div
                style={{
                  color: "#f5f5f5",
                  fontSize: "13px",
                  fontWeight: 600,
                  letterSpacing: "-0.1px",
                }}
              >
                Chat with your document
              </div>

              <div
                style={{
                  color: "#77777f",
                  fontSize: "11px",
                  marginTop: "3px",
                }}
              >
                PDF, DOCX or TXT · Max 10 MB
              </div>
            </div>
          </div>

          <label
            htmlFor="medibot-document-upload"
            style={{
              minHeight: "105px",
              borderRadius: "13px",
              border: "1px dashed #303038",
              background: "#101014",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              justifyContent: "center",
              cursor: loading ? "not-allowed" : "pointer",
              transition: "all 0.2s ease",
              boxSizing: "border-box",
            }}
          >
            <div
              style={{
                width: "34px",
                height: "34px",
                borderRadius: "9px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                background: "#17151f",
                color: "#a78bfa",
                marginBottom: "8px",
              }}
            >
              <Upload size={17} />
            </div>

            <span
              style={{
                color: "#e8e8eb",
                fontSize: "12px",
                fontWeight: 500,
              }}
            >
              Click to choose a document
            </span>

            <span
              style={{
                color: "#66666f",
                fontSize: "10px",
                marginTop: "4px",
              }}
            >
              Your document will be processed for RAG
            </span>

            <input
              id="medibot-document-upload"
              type="file"
              accept=".pdf,.txt,.docx"
              onChange={handleFileChange}
              disabled={loading}
              style={{ display: "none" }}
            />
          </label>

          {file && (
            <div
              style={{
                marginTop: "9px",
                padding: "9px 10px",
                borderRadius: "10px",
                background: "#111115",
                border: "1px solid #25252c",
                display: "flex",
                alignItems: "center",
                justifyContent: "space-between",
                gap: "10px",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "8px",
                  minWidth: 0,
                }}
              >
                <FileText
                  size={15}
                  color="#a78bfa"
                  style={{ flexShrink: 0 }}
                />

                <span
                  style={{
                    color: "#cfcfd4",
                    fontSize: "11px",
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
                onClick={() => setFile(null)}
                disabled={loading}
                style={{
                  border: "none",
                  background: "transparent",
                  color: "#77777f",
                  cursor: "pointer",
                  padding: "2px",
                  display: "flex",
                }}
              >
                <X size={14} />
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
                height: "38px",
                marginTop: "9px",
                border: "none",
                borderRadius: "10px",
                background:
                  "linear-gradient(135deg, #7c3aed, #8b5cf6)",
                color: "#ffffff",
                fontSize: "12px",
                fontWeight: 600,
                cursor: loading ? "not-allowed" : "pointer",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                gap: "7px",
                opacity: loading ? 0.65 : 1,
              }}
            >
              {loading ? (
                <>
                  <Loader2
                    size={15}
                    className="spin"
                  />
                  Processing...
                </>
              ) : (
                <>
                  <Upload size={15} />
                  Upload & Chat
                </>
              )}
            </button>
          )}

          {message && (
            <div
              style={{
                marginTop: "8px",
                padding: "8px 10px",
                borderRadius: "9px",
                background: "#171013",
                border: "1px solid #302025",
                color: "#fca5a5",
                fontSize: "11px",
              }}
            >
              {message}
            </div>
          )}
        </>
      ) : (
        <>
          <div
            style={{
              display: "flex",
              alignItems: "center",
              justifyContent: "space-between",
              gap: "10px",
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
              <div
                style={{
                  width: "36px",
                  height: "36px",
                  borderRadius: "10px",
                  background: "#0f1a14",
                  border: "1px solid #183323",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  color: "#4ade80",
                  flexShrink: 0,
                }}
              >
                <CheckCircle2 size={18} />
              </div>

              <div style={{ minWidth: 0 }}>
                <div
                  style={{
                    color: "#4ade80",
                    fontSize: "10px",
                    fontWeight: 600,
                    marginBottom: "3px",
                  }}
                >
                  DOCUMENT READY
                </div>

                <div
                  style={{
                    color: "#e4e4e7",
                    fontSize: "12px",
                    fontWeight: 500,
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                    whiteSpace: "nowrap",
                  }}
                >
                  {uploadedDocument.filename}
                </div>

                <div
                  style={{
                    color: "#686870",
                    fontSize: "10px",
                    marginTop: "2px",
                  }}
                >
                  {uploadedDocument.chunks || 0} chunks processed
                </div>
              </div>
            </div>

            <button
              type="button"
              onClick={handleRemove}
              style={{
                height: "29px",
                padding: "0 9px",
                borderRadius: "8px",
                border: "1px solid #29292f",
                background: "#121216",
                color: "#888890",
                fontSize: "10px",
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                gap: "4px",
              }}
            >
              <X size={12} />
              Remove
            </button>
          </div>

          <div
            style={{
              marginTop: "10px",
              padding: "8px 10px",
              borderRadius: "9px",
              background: "#0d1510",
              border: "1px solid #17281c",
              color: "#7dd3a0",
              fontSize: "10px",
            }}
          >
            ✓ MediBot is answering from your uploaded document
          </div>
        </>
      )}
    </div>
  );
}