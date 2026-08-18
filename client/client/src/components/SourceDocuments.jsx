import { useState } from "react";

import {
  ChevronDown,
  FileText,
  BookOpen,
} from "lucide-react";

function SourceDocuments({
  sources,
}) {

  const [open, setOpen] =
    useState(false);


  if (
    !sources ||
    sources.length === 0
  ) {
    return null;
  }


  return (
    <div className="sources-container">

      <button
        className="sources-toggle"
        onClick={() =>
          setOpen(!open)
        }
      >

        <div className="sources-title">

          <BookOpen size={15} />

          <span>
            {sources.length} knowledge sources
          </span>

        </div>


        <ChevronDown
          size={16}
          className={
            open
              ? "rotate-chevron"
              : ""
          }
        />

      </button>


      {open && (

        <div className="sources-list">

          {sources.map(
            (source, index) => (

              <div
                className="source-card"
                key={index}
              >

                <div className="source-number">
                  {index + 1}
                </div>


                <div className="source-info">

                  <div className="source-file">

                    <FileText size={14} />

                    <span>
                      {source.source ||
                        "Medical Knowledge Base"}
                    </span>

                  </div>


                  <p>
                    {source.content}
                  </p>


                  <span className="source-page">
                    Page{" "}
                    {source.page ?? "N/A"}
                  </span>

                </div>

              </div>

            )
          )}

        </div>

      )}

    </div>
  );
}

export default SourceDocuments;