import { motion } from "framer-motion";

function Background() {
  return (
    <div className="background-wrapper">

      <div className="grid-background" />

      <motion.div
        className="glow glow-one"
        animate={{
          x: [0, 100, -40, 0],
          y: [0, -50, 80, 0],
        }}
        transition={{
          duration: 18,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      <motion.div
        className="glow glow-two"
        animate={{
          x: [0, -80, 50, 0],
          y: [0, 70, -40, 0],
        }}
        transition={{
          duration: 22,
          repeat: Infinity,
          ease: "easeInOut",
        }}
      />

      <div className="noise" />

    </div>
  );
}

export default Background;