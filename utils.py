import plotly.graph_objects as go
from fpdf import FPDF
from datetime import datetime
import random
import plotly.io as pio
import os



def create_chart(prob):

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=prob,
            title={
                "text": "Loan Approval Probability"
            },
            gauge={
                "axis": {
                    "range": [0,100]
                }
            }
        )
    )

    return fig



def save_chart_image(fig):

    path = "loan_chart.png"

    pio.write_image(
        fig,
        path,
        format="png"
    )

    return path




def generate_pdf(
    name,
    age,
    income,
    credit,
    loan,
    years,
    result,
    prob,
    reason,
    chart_path
):

    pdf = FPDF()

    pdf.add_page()


    # Title
    pdf.set_font(
        "Arial",
        "B",
        16
    )

    pdf.cell(
        200,
        10,
        "BANK LOAN REPORT",
        ln=True,
        align="C"
    )


    pdf.ln(5)


    # Normal text
    pdf.set_font(
        "Arial",
        "",
        12
    )


    pdf.cell(
        200,
        10,
        f"Date: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        ln=True
    )


    pdf.ln(3)


    # Applicant details

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        200,
        10,
        "Applicant Details",
        ln=True
    )


    pdf.set_font(
        "Arial",
        "",
        12
    )


    pdf.cell(
        200,
        10,
        f"Name: {name}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Age: {age}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Income: {income}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Credit Score: {credit}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Loan Amount: {loan}",
        ln=True
    )

    pdf.cell(
        200,
        10,
        f"Years Employed: {years}",
        ln=True
    )


    pdf.ln(5)


    # Result

    pdf.set_font(
        "Arial",
        "B",
        12
    )


    pdf.cell(
        200,
        10,
        "Loan Decision",
        ln=True
    )


    pdf.set_font(
        "Arial",
        "",
        12
    )


    pdf.cell(
        200,
        10,
        f"Result: {result}",
        ln=True
    )


    pdf.cell(
        200,
        10,
        f"Probability: {prob:.2f}%",
        ln=True
    )


    pdf.ln(5)


    # AI Explanation

    pdf.set_font(
        "Arial",
        "B",
        12
    )

    pdf.cell(
        200,
        10,
        "AI Explanation:",
        ln=True
    )


    pdf.set_font(
        "Arial",
        "",
        12
    )


    pdf.multi_cell(
        0,
        8,
        reason
    )


    pdf.ln(5)


    # Add graph

    if chart_path and os.path.exists(chart_path):

        pdf.image(
            chart_path,
            x=10,
            y=pdf.get_y(),
            w=180
        )


    filename = (
        f"loan_report_{random.randint(1000,9999)}.pdf"
    )


    pdf.output(filename)


    return filename