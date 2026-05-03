from flask import Blueprint, render_template, request
from services.model_service import predict_high_value, predict_delay

prediction_bp = Blueprint("prediction", __name__)


@prediction_bp.route("/prediction", methods=["GET", "POST"])
def prediction():

    result = None
    prob = 0
    result_class = ""
    result_label = ""
    insight = ""

    if request.method == "POST":

        model_type = request.form.get("model_type")

        try:
            # Collect input
            input_data = {
                "payment_sequential": int(request.form.get("payment_sequential", 1)),
                "payment_installments": int(request.form.get("payment_installments", 1)),
                "payment_value": float(request.form.get("payment_value", 100)),

                "product_weight_g": float(request.form.get("product_weight_g", 500)),
                "product_height_cm": float(request.form.get("product_height_cm", 10)),
                "product_volume_cm3": float(request.form.get("product_volume_cm3", 3000)),

                "approval_time_hours": float(request.form.get("approval_time_hours", 1)),

                "total_cost": float(request.form.get("total_cost", 150)),
                "product_density": float(request.form.get("product_density", 0.1)),

                "order_month": int(request.form.get("order_month", 6)),
                "is_weekend": int(request.form.get("is_weekend", 0)),

                "price_bucket": int(request.form.get("price_bucket", 2)),
                "high_shipping": int(request.form.get("high_shipping", 0)),
                "is_expensive": int(request.form.get("is_expensive", 0)),
                "is_large_product": int(request.form.get("is_large_product", 0)),
                "high_installments": int(request.form.get("high_installments", 0)),
                "top_category": int(request.form.get("top_category", 1)),

                "payment_type": request.form.get("payment_type", "credit_card"),
                "customer_state": request.form.get("customer_state", "SP"),
                "product_category_name": request.form.get("product_category_name", "toys")
            }

            # CALL MODEL
            if model_type == "high_value":
                pred, probability = predict_high_value(input_data)
            else:
                pred, probability = predict_delay(input_data)

            # CONVERT TO %
            prob = round(probability * 100, 2)

            # RESULT LOGIC
            if prob > 70:
                result_class = "high"
                result_label = "🔴 High Risk / High Value"
                insight = "Strong signal detected. Prioritize this case immediately."

            elif prob > 40:
                result_class = "medium"
                result_label = "🟡 Medium Risk"
                insight = "Moderate likelihood. Monitor closely."

            else:
                result_class = "low"
                result_label = "🟢 Low Risk"
                insight = "Low probability. No urgent action needed."

            result = True

            print("RAW MODEL OUTPUT:", probability)

        except Exception as e:
            result_label = f"Error: {str(e)}"
            result = True

    return render_template(
        "prediction.html",
        result=result,
        probability=prob,
        result_class=result_class,
        result_label=result_label,
        insight=insight
    )