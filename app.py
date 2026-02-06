from flask import Flask, render_template, request, session

from modules.ai_estimator import ai_estimate
from modules.workforce import workforce_estimation
from modules.materials import material_estimation
from modules.timeline import timeline_estimation
from modules.schedule import weekly_schedule
from modules.blueprint import blueprint_generation
from modules.whatif import whatif_simulation
from modules.whatif_ai import whatif_faster_completion, whatif_reduced_budget
from modules.risk_analysis_ai import analyze_comprehensive_risks
from modules.ai_analysis import ai_analysis

app = Flask(__name__)
app.secret_key = "avalon_construction_planning_2026"  # For session management

@app.route("/", methods=["GET", "POST"])
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
                # New fields for enhanced analysis
                "soil_type": request.form.get("soil_type", "Clay"),
                "material_grade": request.form.get("material_grade", "Standard"),
                "machinery": request.form.get("machinery", "Partial"),
                "workforce_size": int(request.form.get("workforce_size", 20)),
                "start_date": request.form.get("start_date", "2026-02-06"),
                "site_access": request.form.get("site_access", "Easy"),
                "budget": int(request.form.get("budget", 5000000))
            }

            # Call Groq AI estimator
            ai_data = ai_estimate(project_data)

            # Build result object for dashboard
            result = {

                "params": project_data,

                "cost": {
                    "material_cost": ai_data.get("resource_costs", {}).get("material_cost", ai_data.get("material_cost", 0)),
                    "labour_cost": ai_data.get("resource_costs", {}).get("labor_cost", ai_data.get("labour_cost", 0)),
                    "overhead": ai_data.get("resource_costs", {}).get("overhead", ai_data.get("overhead", 0)),
                    "contingency": ai_data.get("resource_costs", {}).get("contingency", ai_data.get("contingency", 0)),
                    "total_cost": ai_data.get("total_cost", 0),
                    "breakdown_explanation": ai_data.get("breakdown_explanation", {})
                },

                "timeline": {
                    "duration_days": ai_data.get("timeline", {}).get("total_days", ai_data.get("duration_days", 0)),
                    "weather_delays": ai_data.get("timeline", {}).get("weather_delays", 0),
                    "seasonal_notes": ai_data.get("timeline", {}).get("seasonal_notes", ""),
                    "critical_path": ai_data.get("timeline", {}).get("critical_path", [])
                },

                "phase_breakdown": ai_data.get("phase_breakdown", {}),
                "resource_costs": ai_data.get("resource_costs", {}),

                "workforce": ai_data["workforce"],

                "blueprint": blueprint_generation(
                    project_data["area"],
                    project_data["floors"]
                ),

                "ai": {
                    "insight": ai_data["ai_insight"],
                    "risk": ai_data["risk"]
                }
            }

            # Store project data in session for What-If analysis
            session['base_project'] = {
                **project_data,
                'total_cost': ai_data.get('total_cost', 0),
                'duration_days': ai_data.get('timeline', {}).get('total_days', ai_data.get('duration_days', 0))
            }

            # Run comprehensive risk analysis
            risk_analysis = analyze_comprehensive_risks({
                **project_data,
                'total_cost': ai_data.get('total_cost', 0),
                'duration_days': ai_data.get('timeline', {}).get('total_days', ai_data.get('duration_days', 0))
            })

            # Add risk analysis to result
            result['risk_analysis'] = risk_analysis

            return render_template("dashboard.html", result=result)

        except Exception as e:
            return render_template(
                "index.html",
                result={"error": str(e)}
            )

    return render_template("index.html")


@app.route("/whatif", methods=["GET", "POST"])
def whatif():
    """What-If Simulator page"""
    
    # Get base project from session
    base_project = session.get('base_project')
    
    if not base_project:
        return render_template("index.html", result={"error": "No base project found. Please run an analysis first."})
    
    if request.method == "POST":
        scenario_type = request.form.get("scenario")
        
        try:
            if scenario_type == "faster":
                # Faster completion scenario (20% time reduction)
                scenario_result = whatif_faster_completion(base_project, time_reduction_percent=20)
                scenario_name = "Faster Completion (20% Time Reduction)"
                
            elif scenario_type == "budget_cut":
                # Reduced budget scenario (10% budget cut)
                scenario_result = whatif_reduced_budget(base_project, budget_reduction_percent=10)
                scenario_name = "Reduced Budget (10% Cost Reduction)"
                
            else:
                return render_template("whatif.html", base_project=base_project, error="Invalid scenario type")
            
            return render_template(
                "whatif.html",
                base_project=base_project,
                scenario=scenario_result,
                scenario_name=scenario_name,
                scenario_type=scenario_type
            )
            
        except Exception as e:
            return render_template("whatif.html", base_project=base_project, error=str(e))
    
    # GET request - show scenario selection
    return render_template("whatif.html", base_project=base_project)


@app.route("/risks")
def risks():
    """Risk Analysis Dashboard"""
    
    # Get base project from session
    base_project = session.get('base_project')
    
    if not base_project:
        return render_template("risks.html", risk_analysis=None)
    
    # Run comprehensive risk analysis
    risk_analysis = analyze_comprehensive_risks(base_project)
    
    return render_template("risks.html", risk_analysis=risk_analysis)




if __name__ == "__main__":
    app.run(debug=True)
