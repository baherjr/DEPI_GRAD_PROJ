import streamlit as st
import joblib
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(
    page_title="MSRP Forecasting Dashboard",
    layout="wide"
)

# Custom CSS to improve the appearance
st.markdown("""
    <style>
    .stButton>button {
        width: 100%;
        padding: 1rem;
    }
    .reportview-container {
        background: #f0f2f6;
    }
    .warning {
        padding: 1rem;
        background-color: #fff3cd;
        border: 1px solid #ffeeba;
        border-radius: 0.25rem;
        color: #856404;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)


def load_model():
    """Load the ARIMA model with error handling."""
    try:
        return joblib.load('arima_model.pkl')
    except FileNotFoundError:
        st.error("⚠️ Model file not found. Please ensure 'arima_model.pkl' exists in the current directory.")
        return None
    except Exception as e:
        st.error(f"⚠️ Error loading model: {str(e)}")
        return None


def generate_dates(start_date, steps, frequency='M'):
    """
    Generate future dates for forecasting.

    Args:
        start_date: Starting date for forecast
        steps: Number of periods to forecast
        frequency: 'M' for monthly, 'D' for daily
    """
    if frequency == 'M':
        return pd.date_range(start=start_date, periods=steps + 1, freq='M')[1:]
    return pd.date_range(start=start_date, periods=steps + 1, freq='D')[1:]


def create_forecast_plot(dates, forecast, confidence_intervals=None):
    """Create an interactive plot using Plotly."""
    fig = go.Figure()

    # Add the main forecast line
    fig.add_trace(go.Scatter(
        x=dates,
        y=forecast,
        mode='lines+markers',
        name='Forecast',
        line=dict(color='blue')
    ))

    # Add confidence intervals if available
    if confidence_intervals is not None:
        fig.add_trace(go.Scatter(
            x=dates + dates[::-1],
            y=np.concatenate([confidence_intervals[:, 0], confidence_intervals[:, 1][::-1]]),
            fill='toself',
            fillcolor='rgba(0,100,255,0.2)',
            line=dict(color='rgba(255,255,255,0)'),
            name='95% Confidence Interval'
        ))

    fig.update_layout(
        title='MSRP Forecast',
        xaxis_title='Date',
        yaxis_title='MSRP ($)',
        hovermode='x unified',
        template='plotly_white'
    )

    return fig


def main():
    # Title and description
    st.title("🚗 MSRP Forecasting Dashboard")
    st.markdown("""
    This dashboard provides forecasts for Manufacturer Suggested Retail Prices (MSRP) 
    using an ARIMA model trained on data up to 2017.
    """)

    # Warning about data limitations
    st.markdown("""
    <div class="warning">
        <strong>⚠️ Important Note:</strong><br>
        This model was trained on data up to 2017. Forecasts are limited to 30 periods 
        beyond the training data to maintain prediction accuracy. The forecasts are generated
        on a monthly basis to match the temporal granularity of the training data.
    </div>
    """, unsafe_allow_html=True)

    # Create two columns for layout
    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Forecast Parameters")

        # Input parameters with maximum 30 periods
        steps = st.number_input(
            "Number of months to forecast",
            min_value=1,
            max_value=30,
            value=12,
            help="Enter the number of months to forecast (maximum 30 months from Dec 2017)"
        )

        # Set the default start date to 2017
        default_start = datetime(2017, 12, 31).date()
        start_date = st.date_input(
            "Start date for forecast",
            default_start,
            min_value=default_start,
            max_value=default_start + timedelta(days=30),
            help="Select the starting date for your forecast (forecasts will be monthly from this date)"
        )

        # Confidence interval toggle
        show_confidence = st.checkbox(
            "Show confidence intervals",
            value=True,
            help="Display the 95% confidence interval for the forecast"
        )

    # Load the model
    model = load_model()

    if model is not None and st.button("Generate Forecast", key="forecast_button"):
        try:
            with st.spinner('Generating forecast...'):
                # Generate forecast with monthly frequency
                forecast = model.forecast(steps=steps)
                dates = generate_dates(start_date, steps, frequency='M')

                # Generate confidence intervals
                if show_confidence:
                    conf_int = model.get_forecast(steps=steps).conf_int()
                else:
                    conf_int = None

                # Create and display the plot
                with col2:
                    st.plotly_chart(
                        create_forecast_plot(dates, forecast, conf_int),
                        use_container_width=True
                    )

                # Display forecast data in a table
                st.subheader("Detailed Forecast Data")
                forecast_df = pd.DataFrame({
                    'Date': dates,
                    'Forecasted MSRP': forecast.round(2)
                })

                if show_confidence and conf_int is not None:
                    forecast_df['Lower Bound'] = conf_int.iloc[:, 0].round(2)
                    forecast_df['Upper Bound'] = conf_int.iloc[:, 1].round(2)

                # Format dates as strings in YYYY-MM format for monthly data
                forecast_df['Date'] = forecast_df['Date'].dt.strftime('%Y-%m')

                st.dataframe(forecast_df, use_container_width=True)

                # Add download button for the forecast data
                csv = forecast_df.to_csv(index=False)
                st.download_button(
                    label="Download Forecast Data",
                    data=csv,
                    file_name=f"msrp_forecast_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )

        except Exception as e:
            st.error(f"An error occurred while generating the forecast: {str(e)}")


if __name__ == "__main__":
    main()