import { useState } from "react";
import api from "../services/api";

export default function Prediction() {
  const [form, setForm] = useState({
    age: 35,
    monthly_income: 12000,
    years_at_company: 5,
    job_satisfaction: 4,
    overtime: "Yes",
  });

  const [result, setResult] = useState(null);

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: e.target.value,
    });
  };

  const submit = async (e) => {
    e.preventDefault();

    const payload = {
      age: Number(form.age),
      monthly_income: Number(form.monthly_income),
      years_at_company: Number(form.years_at_company),
      job_satisfaction: Number(form.job_satisfaction),
      overtime: form.overtime,
    };

    const response = await api.post("/predictions/", payload);
    setResult(response.data);
  };

  return (
    <div style={{ padding: "30px" }}>
      <h1>Employee Attrition Prediction</h1>

      <form onSubmit={submit}>
        <input name="age" value={form.age} onChange={handleChange} placeholder="Age" />
        <br /><br />

        <input name="monthly_income" value={form.monthly_income} onChange={handleChange} placeholder="Monthly Income" />
        <br /><br />

        <input name="years_at_company" value={form.years_at_company} onChange={handleChange} placeholder="Years at Company" />
        <br /><br />

        <input name="job_satisfaction" value={form.job_satisfaction} onChange={handleChange} placeholder="Job Satisfaction 1-4" />
        <br /><br />

        <select name="overtime" value={form.overtime} onChange={handleChange}>
          <option value="Yes">Yes</option>
          <option value="No">No</option>
        </select>

        <br /><br />

        <button type="submit">Predict</button>
      </form>

      
      {result && (
        <div>
          <h3>Prediction Result</h3>

          <p>
            <strong>Prediction:</strong> {result.prediction}
          </p>

          <p>
            <strong>Probability:</strong>{" "}
            {(result.probability * 100).toFixed(2)}%
          </p>

          <p>
            <strong>Recommendation:</strong> {result.recommendation}
          </p>

          {result.top_reasons && result.top_reasons.length > 0 && (
            <div>
              <h4>Top Reasons</h4>

              <ul>
                {result.top_reasons.map((item, index) => (
                  <li key={index}>
                    {item.feature}: {item.impact}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}
    </div>
  );
}