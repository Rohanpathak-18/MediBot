import { motion } from "framer-motion";
import {
  BrainCircuit,
  FileSearch,
  MessageCircle,
  Sparkles,
} from "lucide-react";

function WelcomeScreen({ onSuggestion }) {

  const suggestions = [
    {
      icon: FileSearch,
      text: "What are common symptoms of diabetes?",
    },
    {
      icon: BrainCircuit,
      text: "What causes high blood pressure?",
    },
    {
      icon: MessageCircle,
      text: "Explain anemia in simple words.",
    },
  ];

  return (
    <div className="welcome-screen">

      <motion.div
        className="bot-orb"
        initial={{
          scale: 0.7,
          opacity: 0,
        }}
        animate={{
          scale: 1,
          opacity: 1,
        }}
        transition={{
          duration: 0.7,
          ease: "easeOut",
        }}
      >

        <div className="orb-ring ring-one" />
        <div className="orb-ring ring-two" />

        <div className="orb-core">
          <Sparkles size={28} />
        </div>

      </motion.div>


      <motion.h2
        className="welcome-title"
        initial={{
          opacity: 0,
          y: 15,
        }}
        animate={{
          opacity: 1,
          y: 0,
        }}
        transition={{
          delay: 0.15,
          duration: 0.6,
        }}
      >
        How can I help you?
      </motion.h2>


      <motion.p
        className="welcome-description"
        initial={{
          opacity: 0,
          y: 15,
        }}
        animate={{
          opacity: 1,
          y: 0,
        }}
        transition={{
          delay: 0.25,
          duration: 0.6,
        }}
      >
        Ask a medical question. MediBot searches its
        medical knowledge base and generates an answer
        from relevant information.
      </motion.p>


      <div className="suggestions">

        {suggestions.map(
          (suggestion, index) => {

            const Icon = suggestion.icon;

            return (
              <motion.button
                key={suggestion.text}
                className="suggestion-card"
                onClick={() =>
                  onSuggestion(suggestion.text)
                }
                initial={{
                  opacity: 0,
                  y: 15,
                }}
                animate={{
                  opacity: 1,
                  y: 0,
                }}
                transition={{
                  delay:
                    0.35 + index * 0.1,
                  duration: 0.5,
                }}
                whileHover={{
                  y: -3,
                }}
                whileTap={{
                  scale: 0.98,
                }}
              >

                <Icon size={17} />

                <span>
                  {suggestion.text}
                </span>

              </motion.button>
            );
          }
        )}

      </div>

    </div>
  );
}

export default WelcomeScreen;