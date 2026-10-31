import { useState } from "react";
import axios from "axios";
import {
  LayoutDashboard, ScanSearch, Leaf, ShieldCheck,
  ChefHat, CalendarDays, Menu, X, Upload, Loader2,
  Sparkles, Activity, Utensils, HeartPulse
} from "lucide-react";
import "./App.css";

const API = "http://127.0.0.1:8000";

const modules = [
  { id: "dashboard", name: "Dashboard", icon: LayoutDashboard },
  { id: "food", name: "Food Recognition", icon: ScanSearch },
  { id: "freshness", name: "Freshness Detection", icon: Leaf },
  { id: "hygiene", name: "Hygiene Monitor", icon: ShieldCheck },
  { id: "kitchen", name: "Smart Kitchen", icon: ChefHat },
  { id: "planner", name: "Meal Planner", icon: CalendarDays },
];

function App() {
  const [page, setPage] = useState("dashboard");
  const [mobileMenu, setMobileMenu] = useState(false);
  const [file, setFile] = useState(null);
  const [foodName, setFoodName] = useState("");
  const [recipeInput, setRecipeInput] = useState("");
  const [context, setContext] = useState("");
  const [profile, setProfile] = useState({
    age: 21,
    diet_type: "Vegetarian",
    goal: "Muscle gain",
    activity_level: "Moderately active",
    daily_calorie_target: 2200,
    allergies: [],
    food_preferences: ["Indian food"],
    meals_per_day: 4,
  });
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  const currentModule = modules.find((m) => m.id === page);

  function navigate(id) {
    setPage(id);
    setFile(null);
    setResult(null);
    setError("");
    setMobileMenu(false);
  }

  async function runRequest(url, formData, method = "post") {
    setLoading(true);
    setResult(null);
    setError("");

    try {
      const response = await axios({
        method,
        url: `${API}${url}`,
        data: formData,
        headers: method === "post" && !(formData instanceof FormData)
          ? { "Content-Type": "application/json" }
          : undefined,
      });
      setResult(response.data.data ?? response.data);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        "Unable to connect to the backend. Make sure FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  }

  function submitImage(endpoint, extra = {}) {
    if (!file) {
      setError("Please select an image first.");
      return;
    }

    const data = new FormData();
    data.append("file", file);

    Object.entries(extra).forEach(([key, value]) => {
      data.append(key, value);
    });

    runRequest(endpoint, data);
  }

  function submitRecipe() {
    if (!recipeInput.trim()) {
      setError("Enter ingredients or a dish name.");
      return;
    }
    runRequest("/api/kitchen/recipe", { text_input: recipeInput });
  }

  function submitMealPlan() {
    runRequest("/api/meal-planner/generate", profile);
  }

  return (
    <div className="app-shell">
      <aside className={`sidebar ${mobileMenu ? "sidebar-open" : ""}`}>
        <div className="brand">
          <div className="brand-icon"><Utensils size={23} /></div>
          <div>
            <h2>Food Verse <span>AI</span></h2>
            <small>Intelligent Food Platform</small>
          </div>
          <button className="mobile-close" onClick={() => setMobileMenu(false)}>
            <X />
          </button>
        </div>

        <div className="nav-label">WORKSPACE</div>
        <nav>
          {modules.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                className={`nav-item ${page === item.id ? "active" : ""}`}
                onClick={() => navigate(item.id)}
              >
                <Icon size={19} />
                <span>{item.name}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-bottom">
          <div className="status-dot" />
          <span>Food Verse AI Platform</span>
          <small>v1.0.0</small>
        </div>
      </aside>

      {mobileMenu && (
        <div className="menu-overlay" onClick={() => setMobileMenu(false)} />
      )}

      <main className="main-content">
        <header className="topbar">
          <button className="menu-toggle" onClick={() => setMobileMenu(true)}>
            <Menu />
          </button>
          <div>
            <div className="breadcrumb">WORKSPACE / {currentModule?.name.toUpperCase()}</div>
            <h3>{currentModule?.name}</h3>
          </div>
          <div className="topbar-right">
            <span className="online-dot" /> AI Services
          </div>
        </header>

        <section className="page-content">
          {page === "dashboard" && (
            <Dashboard navigate={navigate} />
          )}

          {page === "food" && (
            <ModulePage
              icon={ScanSearch}
              title="Food Recognition & Nutrition"
              description="Identify food items and estimate their nutritional composition using AI."
              button="Analyze Food"
              loading={loading}
              onSubmit={() => submitImage("/api/food-recognition/analyze")}
              file={file}
              setFile={setFile}
              result={result}
              error={error}
            />
          )}

          {page === "freshness" && (
            <ModulePage
              icon={Leaf}
              title="Food Freshness Detection"
              description="Analyze visible food characteristics and receive a preliminary freshness assessment."
              button="Check Freshness"
              loading={loading}
              onSubmit={() => submitImage("/api/freshness/analyze", { food_name: foodName || "Unknown food" })}
              file={file}
              setFile={setFile}
              result={result}
              error={error}
              extra={
                <div className="field">
                  <label>Food name</label>
                  <input value={foodName} onChange={(e) => setFoodName(e.target.value)} placeholder="e.g. Tomato, Apple, Milk" />
                </div>
              }
            />
          )}

          {page === "hygiene" && (
            <ModulePage
              icon={ShieldCheck}
              title="Restaurant Hygiene Monitor"
              description="Use image analysis to identify visible hygiene concerns and receive recommendations."
              button="Analyze Hygiene"
              loading={loading}
              onSubmit={() => submitImage("/api/hygiene/analyze", { context })}
              file={file}
              setFile={setFile}
              result={result}
              error={error}
              extra={
                <div className="field">
                  <label>Inspection context (optional)</label>
                  <input value={context} onChange={(e) => setContext(e.target.value)} placeholder="e.g. Restaurant kitchen" />
                </div>
              }
            />
          )}

          {page === "kitchen" && (
            <div className="module-layout">
              <div className="module-intro">
                <div className="module-icon"><ChefHat /></div>
                <div>
                  <h1>Smart Kitchen Assistant</h1>
                  <p>Generate recipes and cooking guidance from ingredients or a dish name.</p>
                </div>
              </div>
              <div className="panel">
                <div className="field">
                  <label>Ingredients or dish name</label>
                  <textarea
                    rows="5"
                    value={recipeInput}
                    onChange={(e) => setRecipeInput(e.target.value)}
                    placeholder="Example: Paneer, tomato, onion, cream..."
                  />
                </div>
                <button className="primary-btn" onClick={submitRecipe} disabled={loading}>
                  {loading ? <Loader2 className="spin" /> : <Sparkles size={18} />}
                  Generate Recipe
                </button>
                <Feedback loading={loading} error={error} result={result} />
              </div>
            </div>
          )}

          {page === "planner" && (
            <div className="module-layout">
              <div className="module-intro">
                <div className="module-icon"><CalendarDays /></div>
                <div>
                  <h1>Personalized Meal Planner</h1>
                  <p>Create a meal plan based on your dietary preferences and fitness goals.</p>
                </div>
              </div>
              <div className="panel">
                <div className="form-grid">
                  <div className="field">
                    <label>Age</label>
                    <input type="number" value={profile.age} onChange={(e) => setProfile({ ...profile, age: Number(e.target.value) })} />
                  </div>
                  <div className="field">
                    <label>Daily calorie target</label>
                    <input type="number" value={profile.daily_calorie_target} onChange={(e) => setProfile({ ...profile, daily_calorie_target: Number(e.target.value) })} />
                  </div>
                  <div className="field">
                    <label>Diet type</label>
                    <select value={profile.diet_type} onChange={(e) => setProfile({ ...profile, diet_type: e.target.value })}>
                      <option>Vegetarian</option><option>Vegan</option><option>Non-vegetarian</option><option>Eggetarian</option>
                    </select>
                  </div>
                  <div className="field">
                    <label>Fitness goal</label>
                    <select value={profile.goal} onChange={(e) => setProfile({ ...profile, goal: e.target.value })}>
                      <option>Muscle gain</option><option>Weight loss</option><option>Weight maintenance</option><option>General health</option>
                    </select>
                  </div>
                  <div className="field">
                    <label>Activity level</label>
                    <select value={profile.activity_level} onChange={(e) => setProfile({ ...profile, activity_level: e.target.value })}>
                      <option>Sedentary</option><option>Lightly active</option><option>Moderately active</option><option>Very active</option>
                    </select>
                  </div>
                  <div className="field">
                    <label>Meals per day</label>
                    <select value={profile.meals_per_day} onChange={(e) => setProfile({ ...profile, meals_per_day: Number(e.target.value) })}>
                      {[2, 3, 4, 5, 6].map((n) => <option key={n} value={n}>{n}</option>)}
                    </select>
                  </div>
                </div>
                <button className="primary-btn" onClick={submitMealPlan} disabled={loading}>
                  {loading ? <Loader2 className="spin" /> : <Sparkles size={18} />}
                  Generate My Meal Plan
                </button>
                <Feedback loading={loading} error={error} result={result} />
              </div>
            </div>
          )}
        </section>
      </main>
    </div>
  );
}

function Dashboard({ navigate }) {
  const cards = [
    { id: "food", icon: ScanSearch, title: "Food Recognition", desc: "Identify food and estimate nutrition.", color: "green" },
    { id: "freshness", icon: Leaf, title: "Freshness Detection", desc: "Assess visible freshness indicators.", color: "lime" },
    { id: "hygiene", icon: ShieldCheck, title: "Hygiene Monitor", desc: "Detect visible hygiene concerns.", color: "blue" },
    { id: "kitchen", icon: ChefHat, title: "Smart Kitchen", desc: "Generate recipes and cooking guidance.", color: "orange" },
    { id: "planner", icon: CalendarDays, title: "Meal Planner", desc: "Create personalized meal plans.", color: "purple" },
  ];

  return (
    <>
      <div className="welcome-banner">
        <div>
          <div className="eyebrow"><Sparkles size={14} /> AI-POWERED FOOD INTELLIGENCE</div>
          <h1>Smarter food decisions<br />start <span>right here.</span></h1>
          <p>One platform for food recognition, nutrition insights, freshness analysis and personalized meal planning.</p>
          <button className="banner-btn" onClick={() => navigate("food")}>Explore Food Analysis <span>→</span></button>
        </div>
        <div className="banner-art"><div className="art-circle"><Utensils size={75} /></div><div className="art-leaf">✳</div></div>
      </div>

      <div className="section-heading">
        <div><h2>Explore Modules</h2><p>Choose an AI tool to get started</p></div>
        <span className="module-count">05 MODULES</span>
      </div>

      <div className="module-grid">
        {cards.map((card) => {
          const Icon = card.icon;
          return (
            <button className="module-card" key={card.id} onClick={() => navigate(card.id)}>
              <div className={`card-icon ${card.color}`}><Icon size={23} /></div>
              <h3>{card.title}</h3>
              <p>{card.desc}</p>
              <span className="card-link">Open module <span>→</span></span>
            </button>
          );
        })}
      </div>

      <div className="info-strip">
        <HeartPulse size={22} />
        <div><strong>AI-generated estimates</strong><p>Nutrition, freshness and hygiene outputs are preliminary estimates, not medical advice or certified food-safety inspections.</p></div>
      </div>
    </>
  );
}

function ModulePage({ icon: Icon, title, description, button, loading, onSubmit, file, setFile, result, error, extra }) {
  return (
    <div className="module-layout">
      <div className="module-intro">
        <div className="module-icon"><Icon /></div>
        <div><h1>{title}</h1><p>{description}</p></div>
      </div>
      <div className="panel">
        {extra}
        <label className="upload-area">
          <input type="file" accept="image/png,image/jpeg,image/webp" onChange={(e) => setFile(e.target.files[0])} />
          <div className="upload-icon"><Upload /></div>
          <strong>{file ? file.name : "Click to upload an image"}</strong>
          <span>PNG, JPG or WEBP · Maximum 10 MB</span>
        </label>
        {file && <img className="preview-image" src={URL.createObjectURL(file)} alt="Selected preview" />}
        <button className="primary-btn" onClick={onSubmit} disabled={loading}>
          {loading ? <Loader2 className="spin" /> : <Sparkles size={18} />}
          {loading ? "Analyzing..." : button}
        </button>
        <Feedback loading={loading} error={error} result={result} />
      </div>
    </div>
  );
}

function Feedback({ loading, error, result }) {
  if (loading) return <div className="loading-state"><Loader2 className="spin" /> AI is processing your request...</div>;
  if (error) return <div className="error-state">{error}</div>;
  if (!result) return null;

  return (
    <div className="result-panel">
      <div className="result-heading"><Activity size={20} /><h3>Analysis Results</h3></div>
      <pre>{JSON.stringify(result, null, 2)}</pre>
    </div>
  );
}

export default App;