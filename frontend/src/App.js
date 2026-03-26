import React, { useState } from "react";
import axios from "axios";
import { motion } from "framer-motion";
import "./App.css";
import {
  RadialBarChart,
  RadialBar,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
} from "recharts";

function App() {
  const [form, setForm] = useState({
    attendance: 70,
    assignment: 70,
    quiz: 70,
    midsem: 70,
  });

  const [result, setResult] = useState("");
  const [explanation, setExplanation] = useState([]);
  const [suggestions, setSuggestions] = useState([]);

  // Handle slider change
  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]: Number(e.target.value),
    });
  };

  // API call
  const handleSubmit = async () => {
    try {
      const res1 = await axios.post("http://127.0.0.1:8000/predict", form);
      setResult(res1.data.status);

      const res2 = await axios.post("http://127.0.0.1:8000/explain", form);
      setExplanation(res2.data.explanation);

      const res3 = await axios.post("http://127.0.0.1:8000/suggest", form);
      setSuggestions(res3.data.suggestions);
    } catch (err) {
      console.error(err);
      alert("API error");
    }
  };

  // Risk score for meter
  const getRiskScore = () => {
    if (!result) return 0;
    return result.includes("HIGH") ? 80 : 20;
  };

  // Chart data
  const chartData = [
    { name: "Attendance", value: form.attendance },
    { name: "Assignment", value: form.assignment },
    { name: "Quiz", value: form.quiz },
    { name: "Midsem", value: form.midsem },
  ];

  return (
    <div className="container">
      <h1>🎓 EduPredict-X+</h1>

      {/* INPUT CARD */}
      <motion.div
        className="card"
        initial={{ scale: 0.8 }}
        animate={{ scale: 1 }}
      >
        {["attendance", "assignment", "quiz", "midsem"].map((field) => (
          <div className="slider" key={field}>
            <label>
              {field.toUpperCase()} ({form[field]})
            </label>
            <input
              type="range"
              min="0"
              max="100"
              name={field}
              value={form[field]}
              onChange={handleChange}
            />
          </div>
        ))}

        <button onClick={handleSubmit}>Predict</button>
      </motion.div>

      {/* PERFORMANCE CHART */}
      <motion.div className="card" initial={{ y: 50 }} animate={{ y: 0 }}>
        <h3>📊 Student Performance</h3>
        <BarChart width={300} height={200} data={chartData}>
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" fill="#6c63ff" />
        </BarChart>
      </motion.div>

      {/* RESULT */}
      {result && (
        <motion.div
          className={`result ${result.includes("HIGH") ? "high-risk" : "safe"}`}
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
        >
          {result}
        </motion.div>
      )}

      {/* RISK METER */}
      {result && (
        <motion.div
          className="card"
          initial={{ scale: 0.8 }}
          animate={{ scale: 1 }}
        >
          <h3>📊 Risk Meter</h3>
          <RadialBarChart
            width={250}
            height={250}
            cx="50%"
            cy="50%"
            innerRadius="70%"
            outerRadius="100%"
            barSize={15}
            data={[{ name: "Risk", value: getRiskScore() }]}
          >
            <RadialBar
              minAngle={15}
              background
              clockWise
              dataKey="value"
              fill={result.includes("HIGH") ? "#ff4d4d" : "#00ff9c"}
            />
            <Legend />
          </RadialBarChart>
        </motion.div>
      )}

      {/* EXPLANATION */}
      {explanation.length > 0 && (
        <motion.div className="card box" initial={{ y: 50 }} animate={{ y: 0 }}>
          <h3>🧠 Explanation</h3>
          <ul>
            {explanation.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </motion.div>
      )}

      {/* SUGGESTIONS */}
      {suggestions.length > 0 && (
        <motion.div className="card box" initial={{ y: 50 }} animate={{ y: 0 }}>
          <h3>🎯 Suggestions</h3>
          <ul>
            {suggestions.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        </motion.div>
      )}
    </div>
  );
}

export default App;
