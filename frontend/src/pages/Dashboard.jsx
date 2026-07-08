import { useEffect, useState } from "react";
import api from "../services/api";
import MainLayout from "../layouts/MainLayout";
import SummaryCard from "../components/SummaryCard";
import RiskChart from "../components/RiskChart";
import PredictionTrendChart from "../components/PredictionTrendChart";
import FeatureImportanceChart from "../components/FeatureImportanceChart";

export default function Dashboard() {
  const [summary, setSummary] = useState(null);
  const [modelSummary, setModelSummary] = useState(null);
  const [trend, setTrend] = useState([]);
  const [recentPredictions, setRecentPredictions] = useState([]);
  const [featureImportance, setFeatureImportance] = useState([]);
  const [topRisk, setTopRisk] = useState([]);

  const exportExcel = async () => {
    try {
      const response = await api.get(
        "/export/predictions/excel",
        {
          responseType: "blob",
        }
      );

      const url = window.URL.createObjectURL(
        new Blob([response.data])
      );

      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        "prediction_history.xlsx"
      );

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert("Gagal export Excel");
    }
  };

  const exportPdf = async () => {
    try {
      const response = await api.get(
        "/export/predictions/pdf",
        {
          responseType: "blob",
        }
      );

      const url = window.URL.createObjectURL(
        new Blob([response.data])
      );

      const link = document.createElement("a");
      link.href = url;
      link.setAttribute(
        "download",
        "employee_ai_report.pdf"
      );

      document.body.appendChild(link);
      link.click();
      link.remove();

      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
      alert("Gagal export PDF");
    }
  };

  useEffect(() => {
    api.get("/dashboard/summary")
      .then((res) => setSummary(res.data))
      .catch((err) => console.error(err));

    api.get("/dashboard/model-summary")
      .then((res) => setModelSummary(res.data))
      .catch((err) => console.error(err));

    api.get("/dashboard/prediction-trend")
      .then((res) => setTrend(res.data))
      .catch((err) => console.error(err));

    api.get("/dashboard/recent-predictions")
      .then((res) => setRecentPredictions(res.data))
      .catch((err) => console.error(err));
    
    api.get("/model/feature-importance")
      .then((res) => setFeatureImportance(res.data))
      .catch((err) => console.error(err));
    
    api.get("/dashboard/top-risk")
      .then((res) => setTopRisk(res.data))
      .catch((err) => console.error(err));

  }, []);

  if (!summary) {
    return (
      <MainLayout>
        <p>Loading dashboard...</p>
      </MainLayout>
    );
  }

  return (
    <MainLayout>
      <div
        style={{
          background: "linear-gradient(135deg,#0F5BC4,#18C1B7)",
          borderRadius: "15px",
          padding: "30px",
          color: "white",
          marginBottom: "30px",
        }}
      >
        <h1>Employee AI Dashboard</h1>
        <p>AI-powered Employee Attrition Prediction & Analytics</p>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(220px,1fr))",
          gap: "20px",
        }}
      >
        <SummaryCard title="Total Prediction" value={summary.total_predictions} />
        <SummaryCard title="High Risk" value={summary.high_risk} />
        <SummaryCard title="Low Risk" value={summary.low_risk} />
        <SummaryCard title="Average Probability" value={summary.average_probability} />
        <SummaryCard title="Average Probability" value={summary.average_probability} />

        {modelSummary && (
          <>
            <SummaryCard
              title="Latest Accuracy"
              value={`${(modelSummary.latest_accuracy * 100).toFixed(2)}%`}
            />

            <SummaryCard
              title="Best Accuracy"
              value={`${(modelSummary.best_accuracy * 100).toFixed(2)}%`}
            />

            <SummaryCard
              title="Model Versions"
              value={modelSummary.total_versions}
            />

            <SummaryCard
              title="Latest Version"
              value={modelSummary.latest_version}
            />

            <SummaryCard
              title="Employee Health Score"
              value={`${summary.health_score}%`}
            />
          </>
        )}
      </div>

      <p style={{ marginTop: "12px", color: "#64748b" }}>
        Status:
        {" "}
        {summary.health_score >= 90
          ? "Excellent"
          : summary.health_score >= 75
          ? "Good"
          : "Need Attention"}
      </p>

      <div
        style={{
          display: "flex",
          gap: "10px",
          marginTop: "25px",
        }}
      >
        <button
          onClick={exportExcel}
          style={{
            padding: "12px 18px",
            background: "#0F5BC4",
            color: "white",
            border: "none",
            borderRadius: "10px",
            cursor: "pointer",
            fontWeight: "600",
          }}
        >
          Export Excel
        </button>

        <button
          onClick={exportPdf}
          style={{
            padding: "12px 18px",
            background: "#DC2626",
            color: "white",
            border: "none",
            borderRadius: "10px",
            cursor: "pointer",
            fontWeight: "600",
          }}
        >
          Export PDF
        </button>
      </div>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(auto-fit,minmax(420px,1fr))",
          gap: "20px",
          marginTop: "30px",
        }}
      >
        <div
          style={{
            background: "#fff",
            padding: "20px",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,.08)",
          }}
        >
          <h2>Risk Distribution</h2>

          <RiskChart
            highRisk={summary.high_risk}
            lowRisk={summary.low_risk}
          />
        </div>

        <div
          style={{
            background: "#fff",
            padding: "20px",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,.08)",
          }}
        >
          <h2>Prediction Trend</h2>

          <PredictionTrendChart data={trend} />
        </div>
      </div>

      <div
        style={{
          background: "#fff",
          marginTop: "30px",
          padding: "20px",
          borderRadius: "12px",
          boxShadow: "0 2px 8px rgba(0,0,0,.08)",
          overflowX: "auto",
        }}
      >
        <h2>Recent Predictions</h2>

        <table
          cellPadding="12"
          style={{
            width: "100%",
            borderCollapse: "collapse",
          }}
        >
          <thead>
            <tr
              style={{
                background: "#f1f5f9",
                textAlign: "left",
              }}
            >
              <th>Age</th>
              <th>Income</th>
              <th>Years</th>
              <th>Overtime</th>
              <th>Prediction</th>
              <th>Probability</th>
              <th>Date</th>
              <th>Top Reasons</th>
            </tr>
          </thead>

          <tbody>
            {recentPredictions.length === 0 ? (
              <tr>
                <td colSpan="7">
                  Belum ada data prediksi.
                </td>
              </tr>
            ) : (
              recentPredictions.map((item) => (
                <tr
                  key={item.id}
                  style={{
                    borderBottom: "1px solid #e5e7eb",
                  }}
                >
                  <td>{item.age}</td>
                  <td>{item.monthly_income}</td>
                  <td>{item.years_at_company}</td>
                  <td>{item.overtime}</td>
                  <td>{item.prediction}</td>
                  <td>{item.probability}</td>
                  <td>{new Date(item.created_at).toLocaleString()}</td>
                  <td>
                    {item.top_reasons && item.top_reasons.length > 0 ? (
                      <ul>
                        {item.top_reasons.map((reason, index) => (
                          <li key={index}>
                            {reason.feature}: {reason.impact}
                          </li>
                        ))}
                      </ul>
                    ) : (
                      "-"
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>

        <div
          style={{
            background: "#fff",
            padding: "20px",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,.08)",
          }}
        >
          <h2>Feature Importance</h2>

          <FeatureImportanceChart data={featureImportance} />
        </div>

        <div
          style={{
            background: "#fff",
            marginTop: "30px",
            padding: "20px",
            borderRadius: "12px",
            boxShadow: "0 2px 8px rgba(0,0,0,.08)",
          }}
        >
          <h2>Top Risk Employees</h2>

          <table
            style={{
              width: "100%",
              borderCollapse: "collapse",
            }}
          >
            <thead>
              <tr>
                <th>Age</th>
                <th>Income</th>
                <th>Years</th>
                <th>Probability</th>
              </tr>
            </thead>

            <tbody>
              {topRisk.map((item) => (
                <tr key={item.id}>
                  <td>{item.age}</td>
                  <td>{item.monthly_income}</td>
                  <td>{item.years_at_company}</td>
                  <td>
                    {(item.probability * 100).toFixed(2)}%
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </MainLayout>
  );
}