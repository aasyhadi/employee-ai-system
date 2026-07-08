import { useEffect, useState } from "react";
import api from "../services/api";
import MainLayout from "../layouts/MainLayout";

export default function History() {
  const [logs, setLogs] = useState([]);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const response = await api.get("/predictions/history");
      setLogs(response.data);
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <MainLayout>
      <h1>Prediction History</h1>

      {logs.length === 0 ? (
        <p>Belum ada data prediksi</p>
      ) : (
        logs.map((item) => (
          <div
            key={item.id}
            style={{
              background: "#fff",
              padding: "20px",
              borderRadius: "12px",
              marginBottom: "15px",
              boxShadow: "0 2px 8px rgba(0,0,0,.1)"
            }}
          >
            <h3>
              Prediction: {item.prediction}
            </h3>

            <p>
              Probability: {item.probability}
            </p>

            <p>
              Recommendation:
              {" "}
              {item.recommendation}
            </p>

            <p>
              Date:
              {" "}
              {new Date(item.created_at).toLocaleString()}
            </p>
          </div>
        ))
      )}
    </MainLayout>
  );
}