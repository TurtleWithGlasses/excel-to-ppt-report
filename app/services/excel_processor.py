"""
Excel file processing service.
"""
import pandas as pd
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class ExcelProcessor:
    """Service for processing Excel files."""
    
    def __init__(self):
        self.supported_formats = ['.xlsx', '.xls', '.csv']
    
    def validate_file(self, file_path: str) -> bool:
        """
        Validate if the file exists and has a supported format.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        if path.suffix.lower() not in self.supported_formats:
            raise ValueError(f"Unsupported file format: {path.suffix}")
        
        return True
    
    def read_excel_file(self, file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
        """
        Read Excel file and return DataFrame.
        """
        self.validate_file(file_path)
        
        path = Path(file_path)
        try:
            if path.suffix.lower() == '.csv':
                df = pd.read_csv(file_path)
            else:
                df = pd.read_excel(file_path, sheet_name=sheet_name)
            
            logger.info(f"Successfully read file: {file_path}")
            return df
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {str(e)}")
            raise
    
    def read_all_sheets(self, file_path: str) -> Dict[str, pd.DataFrame]:
        """
        Read all sheets from an Excel file.
        """
        self.validate_file(file_path)
        
        path = Path(file_path)
        if path.suffix.lower() == '.csv':
            return {'Sheet1': self.read_excel_file(file_path)}
        
        try:
            excel_file = pd.ExcelFile(file_path)
            sheets = {}
            for sheet_name in excel_file.sheet_names:
                sheets[sheet_name] = pd.read_excel(excel_file, sheet_name=sheet_name)
            
            logger.info(f"Successfully read {len(sheets)} sheets from {file_path}")
            return sheets
        except Exception as e:
            logger.error(f"Error reading sheets from {file_path}: {str(e)}")
            raise
    
    def detect_data_types(self, df: pd.DataFrame) -> Dict[str, str]:
        """
        Detect and return data types for each column.
        """
        type_mapping = {}
        for column in df.columns:
            dtype = str(df[column].dtype)
            if 'int' in dtype:
                type_mapping[column] = 'integer'
            elif 'float' in dtype:
                type_mapping[column] = 'float'
            elif 'datetime' in dtype:
                type_mapping[column] = 'datetime'
            elif 'bool' in dtype:
                type_mapping[column] = 'boolean'
            else:
                type_mapping[column] = 'string'
        
        return type_mapping
    
    def clean_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess DataFrame.
        """
        # Remove completely empty rows and columns
        df = df.dropna(how='all', axis=0)
        df = df.dropna(how='all', axis=1)
        
        # Strip whitespace from string columns
        string_columns = df.select_dtypes(include=['object']).columns
        df[string_columns] = df[string_columns].apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        
        logger.info(f"Data cleaned: {df.shape[0]} rows, {df.shape[1]} columns")
        return df
    
    def get_summary_statistics(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Get summary statistics for the DataFrame.
        """
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        
        summary = {
            'total_rows': len(df),
            'total_columns': len(df.columns),
            'columns': list(df.columns),
            'data_types': self.detect_data_types(df),
            'missing_values': df.isnull().sum().to_dict(),
            'numeric_summary': df[numeric_cols].describe().to_dict() if len(numeric_cols) > 0 else {}
        }
        
        return summary
    
    def extract_data_snapshot(self, file_path: str) -> Dict[str, Any]:
        """
        Extract a comprehensive snapshot of the Excel file data.
        """
        sheets = self.read_all_sheets(file_path)
        
        snapshot = {
            'file_name': Path(file_path).name,
            'total_sheets': len(sheets),
            'sheets': {}
        }
        
        for sheet_name, df in sheets.items():
            df_clean = self.clean_data(df)
            snapshot['sheets'][sheet_name] = self.get_summary_statistics(df_clean)
        
        return snapshot

