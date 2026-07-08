import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Prediction from "./pages/Prediction";
import History from "./pages/History";
import ModelTraining from "./pages/ModelTraining";

function App() {
  const token = localStorage.getItem("token");

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />

        <Route
          path="/dashboard"
          element={token ? <Dashboard /> : <Navigate to="/" />}
        />

        <Route
          path="/prediction"
          element={token ? <Prediction /> : <Navigate to="/" />}
        />

        <Route
          path="/history"
          element={token ? <History /> : <Navigate to="/" />}
        />

        <Route
          path="/model-training"
          element={token ? <ModelTraining /> : <Navigate to="/" />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;