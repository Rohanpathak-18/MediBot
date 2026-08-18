import {
  useEffect,
  useRef,
  useState,
} from "react";

import { motion } from "framer-motion";

import {
  ArrowUp,
  Trash2,
  RotateCcw,
  ShieldCheck,
} from "lucide-react";

import { sendMessage } from "../services/api";

import ChatMessage from "./ChatMessage";
import LoadingMessage from "./LoadingMessage";
import WelcomeScreen from "./WelcomeScreen";


function ChatBox() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const messagesEndRef = useRef(null);
  const textareaRef = useRef(null);


  /* =========================
     AUTO SCROLL
  ========================= */

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);


  /* =========================
     SEND QUESTION
  ========================= */

  const submitQuestion = async (question) => {
    const trimmed = question.trim();

    if (!trimmed || loading) {
      return;
    }

    // Add user's message immediately
    const userMessage = {
      role: "user",
      content: trimmed,
    };

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setInput("");
    setLoading(true);


    try {
      const response = await sendMessage(trimmed);

      const botMessage = {
        role: "assistant",
        content:
          response?.answer ||
          "I couldn't generate a response.",
        sources:
          response?.sources || [],
      };

      setMessages((previous) => [
        ...previous,
        botMessage,
      ]);

    } catch (error) {
      console.error(
        "MediBot API error:",
        error
      );

      const errorMessage = {
        role: "assistant",
        content:
          "I couldn't connect to the MediBot server. Please make sure the FastAPI backend is running.",
        sources: [],
      };

      setMessages((previous) => [
        ...previous,
        errorMessage,
      ]);

    } finally {
      setLoading(false);

      // Focus input again
      setTimeout(() => {
        textareaRef.current?.focus();
      }, 100);
    }
  };


  /* =========================
     FORM SUBMIT
  ========================= */

  const handleSubmit = async (event) => {
    event.preventDefault();

    await submitQuestion(input);
  };


  /* =========================
     SUGGESTION CLICK
  ========================= */

  const handleSuggestion = async (question) => {
    if (loading) {
      return;
    }

    // Directly send the suggestion
    await submitQuestion(question);
  };


  /* =========================
     CLEAR CHAT
  ========================= */

  const clearChat = () => {
    if (loading) {
      return;
    }

    setMessages([]);
    setInput("");

    setTimeout(() => {
      textareaRef.current?.focus();
    }, 100);
  };


  /* =========================
     ENTER KEY
  ========================= */

  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();

      handleSubmit(event);
    }
  };


  return (
    <motion.section
      className="chat-shell"
      initial={{
        opacity: 0,
        y: 25,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      transition={{
        duration: 0.7,
        delay: 0.25,
      }}
    >

      {/* =========================
          CHAT TOP BAR
      ========================= */}

      <div className="chat-topbar">

        <div className="chat-status">

          <div className="online-indicator" />

          <span>
            MEDIBOT ONLINE
          </span>

        </div>


        {messages.length > 0 && (
          <button
            type="button"
            className="clear-button"
            onClick={clearChat}
            disabled={loading}
          >

            <Trash2 size={14} />

            <span>
              Clear
            </span>

          </button>
        )}

      </div>


      {/* =========================
          CHAT CONTENT
      ========================= */}

      <div className="messages-area">

        {/* 
          IMPORTANT:

          WelcomeScreen is shown ONLY when
          there are NO messages.

          Once the user asks a question,
          messages.length becomes greater than 0
          and WelcomeScreen completely disappears.
        */}

        {messages.length === 0 ? (

          <WelcomeScreen
            onSuggestion={handleSuggestion}
          />

        ) : (

          <div className="messages-list">

            {messages.map((message, index) => (
              <ChatMessage
                key={`${message.role}-${index}`}
                message={message}
                index={index}
              />
            ))}


            {loading && (
              <LoadingMessage />
            )}


            <div
              ref={messagesEndRef}
            />

          </div>

        )}

      </div>


      {/* =========================
          INPUT
      ========================= */}

      <div className="input-area">

        <form
          className="input-form"
          onSubmit={handleSubmit}
        >

          <div className="input-wrapper">

            <textarea
              ref={textareaRef}
              value={input}
              onChange={(event) =>
                setInput(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder="Ask MediBot anything about your health..."
              rows={1}
              disabled={loading}
            />


            <motion.button
              type="submit"
              className="send-button"
              disabled={
                loading ||
                !input.trim()
              }
              whileHover={{
                scale:
                  input.trim() && !loading
                    ? 1.05
                    : 1,
              }}
              whileTap={{
                scale:
                  input.trim() && !loading
                    ? 0.95
                    : 1,
              }}
            >

              {loading ? (

                <RotateCcw
                  size={18}
                  className="spin"
                />

              ) : (

                <ArrowUp size={19} />

              )}

            </motion.button>

          </div>

        </form>


        {/* =========================
            INPUT FOOTER
        ========================= */}

        <div className="input-footer">

          <div className="privacy-note">

            <ShieldCheck size={13} />

            <span>
              Responses are based on
              MediBot's medical knowledge base.
            </span>

          </div>


          <span className="keyboard-hint">
            ENTER TO SEND
          </span>

        </div>

      </div>

    </motion.section>
  );
}


export default ChatBox;