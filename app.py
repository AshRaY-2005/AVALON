from flask import Flask, render_template, request, session, redirect, url_for
import os
from functools import wraps
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from modules.ai_estimator import ai_estimate
from modules.workforce import workforce_estimation
from modules.materials import material_estimation
from modules.timeline import timeline_estimation
from modules.schedule import weekly_schedule
from modules.blueprint import blueprint_generation
from modules.whatif import whatif_simulation
from modules.whatif_ai import whatif_faster_completion, whatif_reduced_budget
from modules.risk_analysis_ai import analyze_comprehensive_risks
from modules.analytics_calculator import calculate_advanced_metrics
from modules.ai_analysis import ai_analysis

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY", "avalon_dev_key")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        # Admin credentials from environment variables
        admin_user = os.getenv("ADMIN_USERNAME", "admin")
        admin_pass = os.getenv("ADMIN_PASSWORD", "avalon2026")
        
        if username == admin_user and password == admin_pass:
            session['user'] = "admin"
            return redirect(url_for('index'))
        else:
            return render_template("login.html", error="Invalid username or password")
            
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        try:
            # Collect form data
            project_data = {
                "location": request.form["location"],
                "area": int(request.form["area"]),
                "floors": int(request.form["floors"]),
                "quality": request.form["quality"],
                "priority": request.form["priority"],
                "soil_type": request.form.get("soil_type", "Clay"),
                "material_grade": request.form.get("material_grade", "Standard"),
                "machinery": request.form.get("machinery", "Partial"),
                "workforce_size": int(request.form.get("workforce_size", 20)),
                "start_date": request.form.get("start_date", "2026-02-06"),
                "site_access": request.form.get("site_access", "Easy"),
                # Added budget with a safe default
                "budget": int(request.form.get("budget", 5000000))
            }

            # 1. Primary AI Estimation
            ai_data = ai_estimate(project_data)

            # --- COST VALIDATION LOGIC ---
            resource_costs = ai_data.get("resource_costs", {})
            material_cost = resource_costs.get("material_cost", 0)
            labor_cost = resource_costs.get("labor_cost", 0)
            overhead = resource_costs.get("overhead", 0)
            contingency = resource_costs.get("contingency", 0)
            
            calculated_total = material_cost + labor_cost + overhead + contingency
            if calculated_total == 0 and ai_data.get("phase_breakdown"):
                phase_total = sum(p.get("cost", 0) for p in ai_data["phase_breakdown"].values())
                if phase_total > 0:
                    calculated_total = phase_total
            
            total_cost = calculated_total if calculated_total > 0 else ai_data.get("total_cost", 0)
            # ------------------------------

            # Build result object
            result = {
                "params": project_data,
                "base_project": project_data, # For backward compatibility in analytics
                "cost": {
                    "material_cost": material_cost,
                    "labor_cost": labor_cost,
                    "labour_cost": labor_cost, # For backward compatibility
                    "overhead": overhead,
                    "contingency": contingency,
                    "total_cost": total_cost,
                    "breakdown_explanation": ai_data.get("breakdown_explanation", {}),
                    "calculation_logic": ai_data.get("calculation_logic", "")
                },
                "calculation_logic": ai_data.get("calculation_logic", ""),
                "total_cost": total_cost, # Root level for convenience
                "duration_days": ai_data.get("timeline", {}).get("total_days", ai_data.get("duration_days", 0)),
                "workforce_size": project_data["workforce_size"],
                "cost_per_sqyd": ai_data.get("cost_per_sqyd", total_cost / (project_data['area'] * project_data['floors'])),
                
                "timeline": {
                    "duration_days": ai_data.get("timeline", {}).get("total_days", ai_data.get("duration_days", 0)),
                    "weather_delays": ai_data.get("timeline", {}).get("weather_delays", 0),
                    "seasonal_notes": ai_data.get("timeline", {}).get("seasonal_notes", ""),
                    "critical_path": ai_data.get("timeline", {}).get("critical_path", [])
                },
                "phase_breakdown": ai_data.get("phase_breakdown", {}),
                "resource_costs": resource_costs,
                "workforce": ai_data["workforce"],
                "ai_insight": ai_data.get("ai_insight", "Analysis complete."),
                "risk": ai_data.get("risk", ""),
                "blueprint": blueprint_generation(
                    project_data["area"],
                    project_data["floors"]
                ),
                # Flatten keys for top-level access in templates and simulations
                "location": project_data["location"],
                "area": project_data["area"],
                "floors": project_data["floors"],
                "quality": project_data["quality"],
                "priority": project_data["priority"],
                "machinery": project_data["machinery"],
                "material_grade": project_data["material_grade"]
            }

            # 2. Comprehensive Risk Analysis
            risk_analysis = analyze_comprehensive_risks(project_data)
            result['risk_analysis'] = risk_analysis
            
            # 3. Pre-calculate Analytics for the dashboard/analytics views
            analytics_data = calculate_advanced_metrics(result)
            result['analytics'] = analytics_data

            # Store in session
            session['last_result'] = result
            session['base_project'] = result # Store full result as base project for what-if

            return render_template("dashboard.html", result=result)

        except Exception as e:
            return render_template("index.html", error=str(e))

    return render_template("index.html")


@app.route("/whatif", methods=["GET", "POST"])
@login_required
def whatif():
    """What-If Simulator page"""
    
    # Get base project from session
    base_project = session.get('base_project')
    
    if not base_project:
        return render_template("index.html", result={"error": "No base project found. Please run an analysis first."})
    
    if request.method == "POST":
        duration_change = request.form.get("duration_change", "none")
        budget_change = request.form.get("budget_change", "none")
        quality_focus = request.form.get("quality_focus", "standard")
        custom_goal = request.form.get("custom_scenario", "")
        
        try:
            # Enhanced simulation logic
            new_cost = base_project['total_cost']
            new_duration = base_project['duration_days']
            tradeoffs = []
            risks = []
            
            # 1. Budget impact
            if "increase_10" in budget_change:
                new_cost *= 1.1
                tradeoffs.append("Increased budget allows for premium material sourcing.")
            elif "increase_20" in budget_change:
                new_cost *= 1.2
                tradeoffs.append("Significant budget boost enables high-speed machinery deployment.")
            elif "decrease_10" in budget_change:
                new_cost *= 0.9
                new_duration *= 1.15
                risks.append("Budget cut likely to cause 15% delay due to reduced labor force.")
                tradeoffs.append("Cost savings achieved at the expense of timeline stability.")

            # 2. Duration impact
            if "compress_10" in duration_change:
                new_duration *= 0.9
                new_cost *= 1.05
                tradeoffs.append("10% compression requires additional overtime costs.")
            elif "compress_20" in duration_change:
                new_duration *= 0.8
                new_cost *= 1.2
                risks.append("Extreme compression increases risk of structural curing errors.")
                tradeoffs.append("Double-shift operations implemented for maximum speed.")
            elif "buffer_10" in duration_change:
                new_duration *= 1.1
                tradeoffs.append("Added buffer reduces stress on local supply chains.")

            # 3. Quality focus
            if quality_focus == "premium":
                new_cost *= 1.15
                new_duration *= 1.1
                tradeoffs.append("Premium materials require longer lead times and specialized curing.")
            elif quality_focus == "speed":
                new_cost *= 1.25
                new_duration *= 0.85
                risks.append("High-speed execution may compromise finishing quality.")

            scenario_result = {
                "new_total_cost": new_cost,
                "new_duration_days": int(new_duration),
                "explanation": f"Simulation for goal: '{custom_goal if custom_goal else 'Optimal Delivery'}'. Focus on {quality_focus} with {budget_change} budget adjustment and {duration_change} timeline shift.",
                "tradeoffs": tradeoffs if tradeoffs else ["Standard execution tradeoffs apply."],
                "risks": risks if risks else ["No abnormal risks identified for this scenario."],
                "feasibility": "High" if new_cost >= base_project['total_cost'] else "Moderate",
                "workforce_changes": {
                    "new_size": int(base_project['workforce_size'] * (1.3 if "compress" in duration_change else 1.0)),
                    "original_size": base_project['workforce_size']
                },
                "resource_strain": {
                    "worker_fatigue_score": 8 if "compress" in duration_change else 4,
                    "overall_stress_score": 7 if "speed" in quality_focus else 3
                },
                "recommendations": [
                    "Ensure onsite water storage before Monsoon start.",
                    "Implement daily quality audits during fast-track phases.",
                    "Source aggregates locally to mitigate logistics delay."
                ]
            }
            
            return render_template(
                "whatif.html",
                base_project=base_project,
                scenario=scenario_result,
                scenario_name="Custom AI Simulation"
            )
            
        except Exception as e:
            return render_template("whatif.html", base_project=base_project, error=str(e))
    
    # GET request - show scenario selection
    return render_template("whatif.html", base_project=base_project)


@app.route("/dashboard")
@login_required
def dashboard():
    """Dashboard view for existing project"""
    result = session.get('last_result')
    if not result:
        return render_template("index.html", result={"error": "No project found. Please run an analysis first."})
    return render_template("dashboard.html", result=result)


@app.route("/analytics")
@login_required
def analytics():
    """Visual Analytics Dashboard"""
    result = session.get('last_result')
    if not result:
        return render_template("index.html", error="Please generate an AI analysis first.")
    
    # Generate deep AI insight for the analytics page specifically
    project_data = result.get('params', {})
    analytics_data = result.get('analytics', calculate_advanced_metrics(result))
    
    # Dynamic AI analysis based on the calculated charts
    strategic_insight = ai_analysis(analytics_data, project_data)
    
    return render_template("analytics.html", result=result, analytics=analytics_data, strategic_insight=strategic_insight)


@app.route("/risks")
@login_required
def risks():
    """Risk Analysis Dashboard"""
    result = session.get('last_result')
    if not result:
        return render_template("index.html", error="Please generate an AI analysis first.")
    
    return render_template("risks.html", risk_analysis=result.get('risk_analysis', {}))


if __name__ == "__main__":
    app.run(debug=True)
