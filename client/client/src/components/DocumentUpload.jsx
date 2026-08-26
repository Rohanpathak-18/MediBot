import { useState } from "react";

import { uploadDocument } from "../services/api";


export default function DocumentUpload({
  onDocumentUploaded,
  onDocumentRemoved,
}) {

  const [file, setFile] = useState(null);

  const [loading, setLoading] =
    useState(false);

  const [message, setMessage] =
    useState("");

  const [uploadedDocument, setUploadedDocument] =
    useState(null);


  // =========================
  // FILE SELECT
  // =========================

  const handleFileChange = (event) => {

    const selectedFile =
      event.target.files?.[0];

    if (!selectedFile) {
      return;
    }

    setFile(selectedFile);

    setMessage("");
  };


  // =========================
  // UPLOAD DOCUMENT
  // =========================

  const handleUpload = async () => {

    if (!file) {

      setMessage(
        "Please select a document first."
      );

      return;
    }


    // 10 MB limit
    if (file.size > 10 * 1024 * 1024) {

      setMessage(
        "File size must be less than 10 MB."
      );

      return;
    }


    setLoading(true);

    setMessage("");


    try {

      const data =
        await uploadDocument(file);


      if (!data?.document_id) {

        throw new Error(
          "Document ID was not returned by the server."
        );
      }


      setUploadedDocument(data);

      setMessage(
        `✅ ${data.filename} uploaded successfully`
      );


      // Send document information to ChatBox
      if (onDocumentUploaded) {

        onDocumentUploaded(data);
      }


      setFile(null);


    } catch (error) {

      console.error(
        "Document upload error:",
        error
      );


      const errorMessage =
        error?.response?.data?.detail ||
        error?.message ||
        "Document upload failed.";

      setMessage(
        `❌ ${errorMessage}`
      );


    } finally {

      setLoading(false);
    }
  };


  // =========================
  // REMOVE DOCUMENT
  // =========================

  const handleRemove = () => {

    setUploadedDocument(null);

    setFile(null);

    setMessage("");


    if (onDocumentRemoved) {

      onDocumentRemoved();
    }
  };


  return (

    <div className="document-upload">

      <h3>
        📄 Ask from your own document
      </h3>


      <p>
        Upload a PDF, TXT or DOCX file and
        ask MediBot questions about it.
      </p>


      {!uploadedDocument ? (

        <>

          <input
            type="file"
            accept=".pdf,.txt,.docx"
            onChange={handleFileChange}
            disabled={loading}
          />


          {file && (

            <p>
              Selected:{" "}
              <strong>
                {file.name}
              </strong>
            </p>

          )}


          <button
            type="button"
            onClick={handleUpload}
            disabled={
              loading ||
              !file
            }
          >

            {loading
              ? "Processing..."
              : "Upload Document"
            }

          </button>

        </>

      ) : (

        <div>

          <p>
            ✅{" "}
            <strong>
              {uploadedDocument.filename}
            </strong>
          </p>


          <p>
            {uploadedDocument.chunks} chunks
            processed successfully.
          </p>


          <button
            type="button"
            onClick={handleRemove}
            disabled={loading}
          >
            Remove Document
          </button>

        </div>

      )}


      {message && (

        <p>
          {message}
        </p>

      )}

    </div>
  );
}