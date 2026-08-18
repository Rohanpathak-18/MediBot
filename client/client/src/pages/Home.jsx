import Navbar from "../components/Navbar";
import Background from "../components/Background";
import ChatBox from "../components/ChatBox";

function Home() {
  return (
    <div className="app">
      <Background />

      <Navbar />

      <main className="main-container">
        <section className="hero-section">

          <div className="status-pill">
            <span className="status-dot" />
            AI MEDICAL ASSISTANT
          </div>

          <h1 className="hero-title">
            Your health.
            <br />

            <span className="gradient-text">
              Explained clearly.
            </span>
          </h1>

          <p className="hero-description">
            Ask medical questions and get intelligent,
            context-aware answers powered by
            Retrieval-Augmented Generation.
          </p>

        </section>

        <ChatBox />

        <div className="bottom-disclaimer">
          <span>✦</span>
          MediBot provides informational content only.
          Always consult a qualified healthcare professional
          for medical advice.
        </div>

      </main>
    </div>
  );
}

export default Home;