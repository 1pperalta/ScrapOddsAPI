import express from "express";
import cors from "cors";
import path from "path";
import { fileURLToPath } from "url";
import dotenv from "dotenv";
import { createOddsRoutes } from "./routes/odds.js";
import { createAgentRoutes } from "./routes/agent.js";
import { createAnalysisRoutes } from "./routes/analysis.js";  // NEW LINE

// Forzar la carga del .env desde la raíz del proyecto
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const envPath = path.resolve(__dirname, "../../../.env");
dotenv.config({ path: envPath });

const app = express();
const PORT = process.env.PORT || 5000;

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use("/api/odds", createOddsRoutes());
app.use("/api/agent", createAgentRoutes());
app.use("/api/analysis", createAnalysisRoutes());  // NEW LINE

// Health check
app.get("/api/health", (req, res) => {
  res.json({
    status: "OK",
    timestamp: new Date().toISOString(),
    version: "1.0.0",
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error("Server error:", err);
  res.status(500).json({
    error: "Internal server error",
    message:
      process.env.NODE_ENV === "development"
        ? err.message
        : "Something went wrong",
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: "Not found",
    path: req.path,
  });
});

app.listen(PORT, () => {
  console.log(`🚀 Server running on port ${PORT}`);
  console.log(`📊 Odds API: http://localhost:${PORT}/api/odds`);
  console.log(`🤖 Agent API: http://localhost:${PORT}/api/agent`);
  console.log(`🔍 Analysis API: http://localhost:${PORT}/api/analysis`);  // NEW LINE (optional but nice)
});