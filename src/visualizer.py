"""
Visualization Module
Creates charts and graphs for the dashboard
"""

import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import config

class Visualizer:
    """Handles all visualization needs"""
    
    def __init__(self):
        """Initialize visualizer"""
        self.colors = config.COLORS
    
    def create_risk_gauge(self, probability, risk_level):
        """
        Create a gauge chart for risk visualization
        
        Args:
            probability: float (0-1)
            risk_level: str ('Low', 'Moderate', 'High')
        
        Returns:
            plotly figure
        """
        # Determine color based on risk level
        if risk_level == 'Low':
            color = self.colors['low_risk']
        elif risk_level == 'Moderate':
            color = self.colors['moderate_risk']
        else:
            color = self.colors['high_risk']
        
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=probability * 100,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': f"Risk Level: {risk_level}", 'font': {'size': 24}},
            number={'suffix': "%", 'font': {'size': 40}},
            gauge={
                'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "darkgray"},
                'bar': {'color': color},
                'bgcolor': "white",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 30], 'color': '#e8f5e9'},
                    {'range': [30, 70], 'color': '#fff8e1'},
                    {'range': [70, 100], 'color': '#ffebee'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig.update_layout(
            height=300,
            margin=dict(l=20, r=20, t=60, b=20),
            font={'family': "Arial, sans-serif"}
        )
        
        return fig
    
    def create_risk_bar_chart(self, predictions_df):
        """
        Create bar chart showing risk distribution
        
        Args:
            predictions_df: DataFrame with prediction data
        
        Returns:
            plotly figure
        """
        risk_counts = predictions_df['risk_level'].value_counts()
        
        colors_map = {
            'Low': self.colors['low_risk'],
            'Moderate': self.colors['moderate_risk'],
            'High': self.colors['high_risk']
        }
        
        fig = go.Figure(data=[
            go.Bar(
                x=risk_counts.index,
                y=risk_counts.values,
                marker_color=[colors_map.get(level, '#999') for level in risk_counts.index],
                text=risk_counts.values,
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Risk Level Distribution",
            xaxis_title="Risk Level",
            yaxis_title="Count",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_disease_distribution_pie(self, predictions_df):
        """
        Create pie chart for disease type distribution
        
        Args:
            predictions_df: DataFrame with prediction data
        
        Returns:
            plotly figure
        """
        disease_counts = predictions_df['disease_type'].value_counts()
        
        # Map disease types to display names
        disease_names = {
            'diabetes': '💉 Diabetes',
            'heart': '❤️ Heart Disease',
            'kidney': '🫘 Kidney Disease',
            'liver': '🫀 Liver Disease',
            'breast_cancer': '🎀 Breast Cancer'
        }
        
        labels = [disease_names.get(d, d) for d in disease_counts.index]
        
        fig = go.Figure(data=[go.Pie(
            labels=labels,
            values=disease_counts.values,
            hole=.3,
            textinfo='label+percent',
            textposition='auto'
        )])
        
        fig.update_layout(
            title="Tests by Disease Type",
            height=400
        )
        
        return fig
    
    def create_timeline_chart(self, predictions_df):
        """
        Create timeline chart showing prediction history
        
        Args:
            predictions_df: DataFrame with prediction data
        
        Returns:
            plotly figure
        """
        # Convert date column to datetime
        predictions_df['prediction_date'] = pd.to_datetime(predictions_df['prediction_date'])
        
        # Group by date and count
        daily_counts = predictions_df.groupby(
            predictions_df['prediction_date'].dt.date
        ).size().reset_index(name='count')
        
        fig = go.Figure(data=go.Scatter(
            x=daily_counts['prediction_date'],
            y=daily_counts['count'],
            mode='lines+markers',
            line=dict(color=self.colors['primary'], width=2),
            marker=dict(size=8)
        ))
        
        fig.update_layout(
            title="Prediction History",
            xaxis_title="Date",
            yaxis_title="Number of Predictions",
            height=400
        )
        
        return fig
    
    def create_probability_distribution(self, predictions_df):
        """
        Create histogram of risk probabilities
        
        Args:
            predictions_df: DataFrame with prediction data
        
        Returns:
            plotly figure
        """
        fig = go.Figure(data=[go.Histogram(
            x=predictions_df['risk_probability'],
            nbinsx=20,
            marker_color=self.colors['info'],
            opacity=0.7
        )])
        
        fig.update_layout(
            title="Risk Probability Distribution",
            xaxis_title="Risk Probability",
            yaxis_title="Frequency",
            height=400
        )
        
        return fig
    
    def create_comparison_chart(self, disease_risks):
        """
        Create comparison chart for multiple diseases
        
        Args:
            disease_risks: dict {disease_name: probability}
        
        Returns:
            plotly figure
        """
        diseases = list(disease_risks.keys())
        probabilities = [disease_risks[d] * 100 for d in diseases]
        
        # Determine colors based on probability
        colors = []
        for prob in probabilities:
            if prob < 30:
                colors.append(self.colors['low_risk'])
            elif prob < 70:
                colors.append(self.colors['moderate_risk'])
            else:
                colors.append(self.colors['high_risk'])
        
        fig = go.Figure(data=[
            go.Bar(
                x=diseases,
                y=probabilities,
                marker_color=colors,
                text=[f"{p:.1f}%" for p in probabilities],
                textposition='auto',
            )
        ])
        
        fig.update_layout(
            title="Disease Risk Comparison",
            xaxis_title="Disease",
            yaxis_title="Risk Probability (%)",
            height=400,
            showlegend=False
        )
        
        return fig
    
    def create_feature_importance_chart(self, feature_names, importances):
        """
        Create feature importance chart
        
        Args:
            feature_names: list of feature names
            importances: list of importance values
        
        Returns:
            plotly figure
        """
        # Sort by importance
        sorted_idx = sorted(range(len(importances)), 
                          key=lambda i: importances[i], 
                          reverse=True)
        
        sorted_features = [feature_names[i] for i in sorted_idx[:10]]  # Top 10
        sorted_importances = [importances[i] for i in sorted_idx[:10]]
        
        fig = go.Figure(data=[
            go.Bar(
                y=sorted_features,
                x=sorted_importances,
                orientation='h',
                marker_color=self.colors['primary']
            )
        ])
        
        fig.update_layout(
            title="Top 10 Important Features",
            xaxis_title="Importance",
            yaxis_title="Feature",
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig


def create_risk_indicator(probability, risk_level):
    """
    Create HTML/CSS risk indicator
    
    Args:
        probability: float (0-1)
        risk_level: str
    
    Returns:
        HTML string
    """
    color_map = {
        'Low': config.COLORS['low_risk'],
        'Moderate': config.COLORS['moderate_risk'],
        'High': config.COLORS['high_risk']
    }
    
    color = color_map.get(risk_level, '#999')
    
    html = f"""
    <div style="
        background: linear-gradient(135deg, {color}22 0%, {color}44 100%);
        border-left: 5px solid {color};
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    ">
        <h2 style="color: {color}; margin: 0 0 10px 0;">
            Risk Level: {risk_level}
        </h2>
        <h1 style="color: {color}; margin: 0; font-size: 48px;">
            {probability * 100:.1f}%
        </h1>
    </div>
    """
    
    return html
