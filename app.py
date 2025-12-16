import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import numpy as np

# Створюємо тестовий датасет
np.random.seed(42)

years = []
months = []
vehicle_types = []
automobile_sales = []
advertising_expenditure = []
unemployment_rates = []
recession = []

vehicle_type_list = ['Sedan', 'SUV', 'Truck', 'Sports']

for year in range(2015, 2024):
    for month in range(1, 13):
        for veh_type in vehicle_type_list:
            years.append(year)
            months.append(month)
            vehicle_types.append(veh_type)
            
            # Recession years: 2016, 2020
            is_recession = 1 if year in [2016, 2020] else 0
            recession.append(is_recession)
            
            # Продажі нижчі під час рецесії
            if is_recession:
                sales = np.random.randint(200, 500)
                unemp = np.random.uniform(7, 10)
            else:
                sales = np.random.randint(500, 1200)
                unemp = np.random.uniform(4, 6)
            
            automobile_sales.append(sales)
            unemployment_rates.append(unemp)
            advertising_expenditure.append(np.random.randint(5000, 15000))

df = pd.DataFrame({
    'Year': years,
    'Month': months,
    'Vehicle_Type': vehicle_types,
    'Automobile_Sales': automobile_sales,
    'Advertising_Expenditure': advertising_expenditure,
    'unemployment_rate': unemployment_rates,
    'Recession': recession
})

# TASK 2.1: Create Dash application
app = dash.Dash(__name__)
app.title = "Automobile Sales Statistics Dashboard"

# TASK 2.2: Add drop-downs
app.layout = html.Div([
    html.H1("Automobile Sales Statistics Dashboard",
            style={'textAlign': 'center', 'color': '#503D36', 'fontSize': 28, 'marginBottom': 30}),
    
    html.Div([
        # Dropdown 1: Select Statistics
        html.Div([
            html.Label("Select Statistics:", style={'fontSize': 18, 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='dropdown-statistics',
                options=[
                    {'label': 'Yearly Statistics', 'value': 'Yearly Statistics'},
                    {'label': 'Recession Period Statistics', 'value': 'Recession Period Statistics'}
                ],
                value='Yearly Statistics',
                placeholder='Select a report type',
                style={'width': '100%', 'padding': '3px', 'fontSize': 16}
            )
        ], style={'width': '45%', 'display': 'inline-block', 'marginRight': '5%'}),
        
        # Dropdown 2: Select Year
        html.Div([
            html.Label("Select Year:", style={'fontSize': 18, 'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='select-year',
                options=[],
                value=None,
                placeholder='Select a year',
                style={'width': '100%', 'padding': '3px', 'fontSize': 16}
            )
        ], style={'width': '45%', 'display': 'inline-block'})
    ], style={'marginBottom': 30, 'padding': '0 20px'}),
    
    # TASK 2.3: Division for output display
    html.Div(id='output-container', 
             className='chart-grid',
             style={'padding': '20px'})
])

# TASK 2.4: Creating Callbacks
# Callback 1: Оновлює input-container (dropdown року) на основі типу звіту
@app.callback(
    Output(component_id='select-year', component_property='disabled'),
    Output(component_id='select-year', component_property='options'),
    Input(component_id='dropdown-statistics', component_property='value')
)
def update_input_container(selected_statistics):
    """
    Цей колбек оновлює dropdown для вибору року:
    - Якщо обрано Yearly Statistics - активує dropdown і показує список років
    - Якщо обрано Recession Statistics - вимикає dropdown (бо рік не потрібен)
    """
    if selected_statistics == 'Yearly Statistics':
        # Для річної статистики - активуємо dropdown року
        year_list = [{'label': str(i), 'value': i} for i in sorted(df['Year'].unique())]
        return False, year_list
    else:
        # Для Recession - відключаємо dropdown року
        return True, []

# Callback 2: Оновлює графіки на основі вибору
@app.callback(
    Output(component_id='output-container', component_property='children'),
    [Input(component_id='dropdown-statistics', component_property='value'),
     Input(component_id='select-year', component_property='value')]
)
def update_output_container(selected_statistics, input_year):
    """
    Цей колбек малює графіки залежно від вибраного типу звіту та року:
    - Для Recession - показує 4 графіки про рецесію
    - Для Yearly - показує 4 графіки про конкретний рік
    """
    if selected_statistics == 'Recession Period Statistics':
        # TASK 2.5: Create graphs for Recession Report
        recession_data = df[df['Recession'] == 1]
        
        # Графік 1: Середні продажі по типу авто під час рецесії
        avg_sales = recession_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        R_chart1 = dcc.Graph(
            figure=px.bar(
                avg_sales,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title="Average Automobile Sales by Vehicle Type during Recession",
                color='Vehicle_Type',
                labels={'Automobile_Sales': 'Average Sales'}
            )
        )
        
        # Графік 2: Динаміка продажів по роках під час рецесії
        avg_sales_year = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        R_chart2 = dcc.Graph(
            figure=px.line(
                avg_sales_year,
                x='Year',
                y='Automobile_Sales',
                title="Average Automobile Sales during Recession Period",
                markers=True,
                labels={'Automobile_Sales': 'Average Sales'}
            )
        )
        
        # Графік 3: Розподіл рекламних витрат по типу авто
        exp_data = recession_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        R_chart3 = dcc.Graph(
            figure=px.pie(
                exp_data,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title="Advertising Expenditure Share by Vehicle Type during Recession",
                hole=0.3
            )
        )
        
        # Графік 4: Вплив безробіття на продажі по типу авто
        unemp_data = recession_data.groupby('Vehicle_Type')['unemployment_rate'].mean().reset_index()
        R_chart4 = dcc.Graph(
            figure=px.bar(
                unemp_data,
                x='Vehicle_Type',
                y='unemployment_rate',
                title="Average Unemployment Rate by Vehicle Type during Recession",
                color='Vehicle_Type',
                labels={'unemployment_rate': 'Avg Unemployment Rate (%)'}
            )
        )
        
        return [
            html.Div([R_chart1, R_chart2], style={'display': 'flex', 'flexWrap': 'wrap'}),
            html.Div([R_chart3, R_chart4], style={'display': 'flex', 'flexWrap': 'wrap'})
        ]
        
    elif input_year and selected_statistics == 'Yearly Statistics':
        # TASK 2.6: Create graphs for Yearly Report
        yearly_data = df[df['Year'] == input_year]
        
        # Графік 1: Тренд річних продажів (всі роки)
        yearly_trend = df.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                yearly_trend,
                x='Year',
                y='Automobile_Sales',
                title="Yearly Automobile Sales Trend (All Years)",
                markers=True,
                labels={'Automobile_Sales': 'Average Sales'}
            )
        )
        
        # Графік 2: Місячні продажі за обраний рік
        monthly_sales = yearly_data.groupby('Month')['Automobile_Sales'].sum().reset_index()
        Y_chart2 = dcc.Graph(
            figure=px.line(
                monthly_sales,
                x='Month',
                y='Automobile_Sales',
                title=f"Total Monthly Automobile Sales in {input_year}",
                markers=True,
                labels={'Automobile_Sales': 'Total Sales', 'Month': 'Month'}
            )
        )
        
        # Графік 3: Середні продажі по типу авто за рік
        avg_veh = yearly_data.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index()
        Y_chart3 = dcc.Graph(
            figure=px.bar(
                avg_veh,
                x='Vehicle_Type',
                y='Automobile_Sales',
                title=f"Average Vehicles Sold by Type in {input_year}",
                color='Vehicle_Type',
                labels={'Automobile_Sales': 'Average Sales'}
            )
        )
        
        # Графік 4: Рекламні витрати по типу авто
        adv_exp = yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure=px.pie(
                adv_exp,
                values='Advertising_Expenditure',
                names='Vehicle_Type',
                title=f"Advertising Expenditure Share by Vehicle Type in {input_year}",
                hole=0.3
            )
        )
        
        return [
            html.Div([Y_chart1, Y_chart2], style={'display': 'flex', 'flexWrap': 'wrap'}),
            html.Div([Y_chart3, Y_chart4], style={'display': 'flex', 'flexWrap': 'wrap'})
        ]
    
    else:
        return html.Div(
            "Please select a year to view yearly statistics",
            style={'textAlign': 'center', 'padding': '50px', 'fontSize': 20, 'color': '#666'}
        )

if __name__ == '__main__':
    app.run(debug=True, port=8050)