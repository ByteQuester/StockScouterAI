# main.py

from app.services.queries.query_managers.data_loader import DataLoader
from app.services.queries.query_managers.view_manager import ViewManager

def create_views():
    query_manager = ViewManager()
    views = [
        'profitability_views.sql',
        'cash_flow_views.sql',
        'liquidity_views.sql',
        'assets_liabilities_views.sql'
    ]
    for view in views:
        query_manager.execute_sql_file(f'app/services/queries/sql_views/{view}')

def load_data():
    data_loader = DataLoader()
    data_loader.load_data_to_db()

if __name__ == "__main__":
    load_data()
    create_views()
