import { motion } from "framer-motion";
import {
  Bot,
  User,
  FileText,
  ChevronDown,
} from "lucide-react";
import { useState } from "react";


function ChatMessage({ message, index }) {
  const [showSources, setShowSources] = useState(false);

  const isUser = message?.role === "user";

  const content =
    message?.content ||
    message?.answer ||
    "No response was generated.";


  return (
    <motion.div
      className={`message-row ${
        isUser ? "user-row" : ""
      }`}
      initial={{
        opacity: 0,
        y: 12,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      transition={{
        duration: 0.35,
        delay: Math.min(index * 0.03, 0.15),
      }}
    >

      {/* =========================
          AVATAR
      ========================= */}

      <div
        className={`avatar ${
          isUser
            ? "user-avatar"
            : "bot-avatar"
        }`}
      >
        {isUser ? (
          <User size={17} />
        ) : (
          <Bot size={17} />
        )}
      </div>


      {/* =========================
          MESSAGE CONTENT
      ========================= */}

      <div className="message-content">

        <div className="message-label">
          {isUser ? "YOU" : "MEDIBOT"}
        </div>


        <div
          className={`message-bubble ${
            isUser
              ? "user-bubble"
              : "bot-bubble"
          }`}
        >
          <p>{content}</p>
        </div>


        {/* =========================
            SOURCES
        ========================= */}

        {!isUser &&
          Array.isArray(message?.sources) &&
          message.sources.length > 0 && (

            <div className="sources-container">

              <button
                type="button"
                className="sources-toggle"
                onClick={() =>
                  setShowSources(
                    (previous) => !previous
                  )
                }
              >

                <span className="sources-title">

                  <FileText size={13} />

                  <span>
                    {message.sources.length}{" "}
                    {message.sources.length === 1
                      ? "Source"
                      : "Sources"}
                  </span>

                </span>


                <ChevronDown
                  size={14}
                  className={
                    showSources
                      ? "rotate-chevron"
                      : ""
                  }
                />

              </button>


              {showSources && (

                <div className="sources-list">

                  {message.sources.map(
                    (source, sourceIndex) => {

                      /*
                       * The backend may return
                       * different field names.
                       * We safely handle the common ones.
                       */

                      const fileName =
                        source?.file_name ||
                        source?.filename ||
                        source?.source ||
                        source?.metadata?.source ||
                        "Medical Knowledge Base";

                      const text =
                        source?.content ||
                        source?.text ||
                        source?.page_content ||
                        source?.metadata?.text ||
                        "";

                      const page =
                        source?.page ||
                        source?.page_number ||
                        source?.metadata?.page;


                      return (
                        <div
                          className="source-card"
                          key={sourceIndex}
                        >

                          <div className="source-number">
                            {sourceIndex + 1}
                          </div>


                          <div className="source-info">

                            <div className="source-file">

                              <FileText
                                size={12}
                              />

                              <span>
                                {fileName}
                              </span>

                            </div>


                            {text && (
                              <p>
                                {text}
                              </p>
                            )}


                            {page !== undefined &&
                              page !== null && (

                                <span className="source-page">
                                  Page {page}
                                </span>

                              )}

                          </div>

                        </div>
                      );
                    }
                  )}

                </div>

              )}

            </div>

          )}

      </div>

    </motion.div>
  );
}


export default ChatMessage;