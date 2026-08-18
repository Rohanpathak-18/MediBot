import { motion } from "framer-motion";
import {
  Activity,
  Github,
  ShieldCheck,
} from "lucide-react";

function Navbar() {
  return (
    <header className="navbar">

      <div className="navbar-inner">

        <motion.div
          className="brand"
          initial={{
            opacity: 0,
            x: -20,
          }}
          animate={{
            opacity: 1,
            x: 0,
          }}
          transition={{
            duration: 0.6,
          }}
        >

          <div className="brand-icon">
            <Activity size={20} />
          </div>

          <div>
            <div className="brand-name">
              MediBot
            </div>

            <div className="brand-subtitle">
              AI HEALTH INTELLIGENCE
            </div>
          </div>

        </motion.div>


        <motion.div
          className="navbar-right"
          initial={{
            opacity: 0,
            x: 20,
          }}
          animate={{
            opacity: 1,
            x: 0,
          }}
          transition={{
            duration: 0.6,
            delay: 0.1,
          }}
        >

          <div className="secure-badge">
            <ShieldCheck size={14} />
            RAG POWERED
          </div>

          <div className="nav-line" />

          <Github size={17} />

        </motion.div>

      </div>

    </header>
  );
}

export default Navbar;