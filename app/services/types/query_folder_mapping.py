from enum import Enum


class QueryFolderMapping(Enum):
    """
    QueryFolderMapping associates query types with specific folder names for data storage. This mapping is crucial
    for organizing processed data into categorized directories, enhancing data management and retrieval efficiency
    based on the query context.
    """
    ASSETS_LIABILITIES = 'Assets_Liabilities'
    CASH_FLOW = 'Cash_Flow'
    LIQUIDITY = 'Liquidity'
    PROFITABILITY = 'Profitability'

    @staticmethod
    def get_folder_name(query_name: str) -> str:
        mapping = {
            item.name.replace("_", " ").upper(): item.value
            for item in QueryFolderMapping
        }
        return mapping.get(query_name.upper())
