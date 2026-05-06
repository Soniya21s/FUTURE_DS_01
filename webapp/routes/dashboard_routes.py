from flask import Blueprint, render_template, request
import pandas as pd

dashboard_bp = Blueprint("dashboard", __name__)

@dashboard_bp.route("/dashboard", methods=["GET", "POST"])
def dashboard():

    df = pd.read_csv("../data/processed/dashboard_dataset.csv")

   
    # GET FILTER VALUES
    selected_state = request.form.get("state")
    selected_month = request.form.get("month")
    selected_category = request.form.get("category")

    
    # APPLY FILTERS
    if selected_state and selected_state != "All":
        df = df[df["customer_state"] == selected_state]

    if selected_month and selected_month != "All":
        df = df[df["order_month"] == int(selected_month)]

    if selected_category and selected_category != "All":
        df = df[df["product_category_name"] == selected_category]

    
    # KPIs
    
    total_revenue = round(df["payment_value"].sum(), 2)
    total_orders = len(df)
    avg_order = round(df["payment_value"].mean(), 2)

    delayed_pct = round(df["is_delayed"].mean() * 100, 2)
    high_value_pct = round(df["high_value"].mean() * 100, 2)
    avg_delivery = round(df["delivery_time_days"].mean(), 2)

    
    # CHART DATA
    
    revenue_trend = df.groupby("order_month")["payment_value"].sum().to_dict()
    payment_split = df["payment_type"].value_counts().to_dict()
    state_orders = df["customer_state"].value_counts().to_dict()

    # FILTER OPTIONS
    states = sorted(df["customer_state"].unique())
    months = sorted(df["order_month"].unique())
    categories = sorted(df["product_category_name"].unique())

    return render_template(
        "dashboard.html",

        # KPIs
        total_revenue=total_revenue,
        total_orders=total_orders,
        avg_order=avg_order,
        delayed_pct=delayed_pct,
        high_value_pct=high_value_pct,
        avg_delivery=avg_delivery,

        # Charts
        revenue_trend=revenue_trend,
        payment_split=payment_split,
        state_orders=state_orders,

        # Filters
        states=states,
        months=months,
        categories=categories
    )