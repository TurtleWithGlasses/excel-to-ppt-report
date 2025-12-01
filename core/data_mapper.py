"""
DataMapper - Maps Excel/CSV data to component data structures

This module handles data loading, transformation, and mapping between Excel files
and PowerPoint components. Supports variable substitution, column mapping, and
data filtering.
"""

from typing import Dict, Any, List, Optional, Union
import pandas as pd
import os
from datetime import datetime


class DataMapper:
    """
    Maps data from Excel/CSV files to component-ready formats.

    Handles:
    - Excel file loading (xlsx, xls)
    - CSV file loading
    - Column mapping and renaming
    - Data filtering and transformation
    - Variable extraction for text substitution
    - Multi-sheet Excel support
    """

    def __init__(self, data_path: Optional[str] = None):
        """
        Initialize DataMapper.

        Args:
            data_path: Path to Excel/CSV file (optional)
        """
        self.data_path = data_path
        self.data: Optional[pd.DataFrame] = None
        self.metadata: Dict[str, Any] = {}

        if data_path:
            self.load_data(data_path)

    def load_data(self, file_path: str, sheet_name: Union[str, int] = 0) -> pd.DataFrame:
        """
        Load data from Excel or CSV file.

        Args:
            file_path: Path to data file
            sheet_name: Sheet name or index for Excel files (default: 0)

        Returns:
            DataFrame with loaded data

        Raises:
            FileNotFoundError: If file doesn't exist
            ValueError: If file format is unsupported

        Example:
            mapper = DataMapper()
            df = mapper.load_data('data/BSH_November.xlsx')
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Data file not found: {file_path}")

        file_ext = os.path.splitext(file_path)[1].lower()

        try:
            if file_ext in ['.xlsx', '.xls']:
                self.data = pd.read_excel(file_path, sheet_name=sheet_name)
            elif file_ext == '.csv':
                self.data = pd.read_csv(file_path)
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")

            self.data_path = file_path
            self._extract_metadata()

            return self.data

        except Exception as e:
            raise Exception(f"Failed to load data from {file_path}: {str(e)}") from e

    def _extract_metadata(self) -> None:
        """Extract metadata from loaded data for use in text variables."""
        if self.data is None:
            return

        self.metadata = {
            'row_count': len(self.data),
            'column_count': len(self.data.columns),
            'columns': list(self.data.columns),
            'load_date': datetime.now().strftime('%Y-%m-%d'),
            'load_time': datetime.now().strftime('%H:%M:%S')
        }

        # Extract file info if path available
        if self.data_path:
            self.metadata['file_name'] = os.path.basename(self.data_path)
            self.metadata['file_path'] = self.data_path

    def get_data_for_component(
        self,
        component_config: Dict[str, Any],
        variables: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Get data formatted for a specific component.

        Args:
            component_config: Component configuration dictionary
            variables: Additional variables for text substitution

        Returns:
            Data formatted for the component (DataFrame, dict, etc.)

        Example:
            config = {
                'type': 'table',
                'data_source': {
                    'columns': ['Company', 'Total'],
                    'sort_by': 'Total'
                }
            }
            data = mapper.get_data_for_component(config)
        """
        component_type = component_config.get('type')
        data_source = component_config.get('data_source', {})

        if component_type == 'text':
            return self._get_text_data(component_config, variables)
        elif component_type in ['table', 'chart']:
            return self._get_tabular_data(data_source)
        elif component_type == 'summary':
            return self._get_summary_data(data_source)
        elif component_type == 'image':
            return self._get_image_data(data_source)
        else:
            return self.data

    def _get_text_data(
        self,
        component_config: Dict[str, Any],
        additional_vars: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get data for text components (variables for substitution).

        Args:
            component_config: Text component configuration
            additional_vars: Additional variables to include

        Returns:
            Dictionary of variables for text substitution
        """
        variables = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'month': datetime.now().strftime('%B'),
            'year': datetime.now().strftime('%Y'),
            'day': datetime.now().strftime('%d'),
        }

        # Add metadata
        variables.update(self.metadata)

        # Add config variables
        config_vars = component_config.get('variables', {})
        variables.update(config_vars)

        # Add additional variables
        if additional_vars:
            variables.update(additional_vars)

        return variables

    def _get_tabular_data(self, data_source: Dict[str, Any]) -> pd.DataFrame:
        """
        Get data for table/chart components.

        Applies:
        - Column filtering
        - Column mapping/renaming
        - Sorting
        - Top N filtering

        Args:
            data_source: Data source configuration

        Returns:
            Filtered and transformed DataFrame
        """
        if self.data is None or self.data.empty:
            return pd.DataFrame()

        df = self.data.copy()

        # Filter columns
        columns = data_source.get('columns')
        if columns:
            available_cols = [col for col in columns if col in df.columns]
            if available_cols:
                df = df[available_cols]

        # Apply column mapping
        column_mapping = data_source.get('column_mapping', {})
        if column_mapping:
            df = df.rename(columns=column_mapping)

        # Sort data
        sort_by = data_source.get('sort_by')
        if sort_by and sort_by in df.columns:
            ascending = data_source.get('ascending', False)
            df = df.sort_values(by=sort_by, ascending=ascending)

        # Top N filtering
        top_n = data_source.get('top_n')
        if top_n and isinstance(top_n, int) and top_n > 0:
            df = df.head(top_n)

        return df

    def _get_summary_data(self, data_source: Dict[str, Any]) -> pd.DataFrame:
        """
        Get data for summary components.

        Args:
            data_source: Data source configuration

        Returns:
            DataFrame ready for summary analysis
        """
        return self._get_tabular_data(data_source)

    def _get_image_data(self, data_source: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get data for image components.

        Args:
            data_source: Data source configuration

        Returns:
            Dictionary with image path information
        """
        return data_source

    def apply_column_mapping(
        self,
        mapping: Dict[str, str],
        reverse: bool = False
    ) -> pd.DataFrame:
        """
        Apply column name mapping to the entire dataset.

        Args:
            mapping: Dictionary mapping old names to new names
            reverse: If True, reverse the mapping (new to old)

        Returns:
            DataFrame with renamed columns

        Example:
            mapping = {'Kurum': 'Company', 'Toplam': 'Total'}
            df = mapper.apply_column_mapping(mapping)
        """
        if self.data is None:
            raise ValueError("No data loaded")

        if reverse:
            mapping = {v: k for k, v in mapping.items()}

        self.data = self.data.rename(columns=mapping)
        self._extract_metadata()
        return self.data

    def filter_data(
        self,
        column: str,
        values: List[Any],
        exclude: bool = False
    ) -> pd.DataFrame:
        """
        Filter data by column values.

        Args:
            column: Column name to filter on
            values: List of values to include/exclude
            exclude: If True, exclude values instead of including

        Returns:
            Filtered DataFrame

        Example:
            # Include only BSH and Arçelik
            df = mapper.filter_data('Company', ['BSH', 'Arçelik'])

            # Exclude Vestel
            df = mapper.filter_data('Company', ['Vestel'], exclude=True)
        """
        if self.data is None:
            raise ValueError("No data loaded")

        if column not in self.data.columns:
            raise ValueError(f"Column '{column}' not found in data")

        if exclude:
            self.data = self.data[~self.data[column].isin(values)]
        else:
            self.data = self.data[self.data[column].isin(values)]

        return self.data

    def aggregate_data(
        self,
        group_by: Union[str, List[str]],
        aggregations: Dict[str, Union[str, List[str]]]
    ) -> pd.DataFrame:
        """
        Aggregate data by grouping columns.

        Args:
            group_by: Column(s) to group by
            aggregations: Dictionary of column -> aggregation function(s)

        Returns:
            Aggregated DataFrame

        Example:
            # Sum Total by Company
            df = mapper.aggregate_data(
                group_by='Company',
                aggregations={'Total': 'sum', 'Positive': 'sum'}
            )
        """
        if self.data is None:
            raise ValueError("No data loaded")

        grouped = self.data.groupby(group_by)
        self.data = grouped.agg(aggregations).reset_index()

        return self.data

    def get_column_names(self) -> List[str]:
        """
        Get list of column names in the dataset.

        Returns:
            List of column names
        """
        if self.data is None:
            return []
        return list(self.data.columns)

    def get_unique_values(self, column: str) -> List[Any]:
        """
        Get unique values in a column.

        Args:
            column: Column name

        Returns:
            List of unique values

        Example:
            companies = mapper.get_unique_values('Company')
        """
        if self.data is None or column not in self.data.columns:
            return []

        return self.data[column].unique().tolist()

    def get_summary_stats(self, column: str) -> Dict[str, Any]:
        """
        Get summary statistics for a numeric column.

        Args:
            column: Column name

        Returns:
            Dictionary with statistics (mean, median, sum, etc.)

        Example:
            stats = mapper.get_summary_stats('Total')
        """
        if self.data is None or column not in self.data.columns:
            return {}

        if not pd.api.types.is_numeric_dtype(self.data[column]):
            return {'error': 'Column is not numeric'}

        return {
            'sum': float(self.data[column].sum()),
            'mean': float(self.data[column].mean()),
            'median': float(self.data[column].median()),
            'min': float(self.data[column].min()),
            'max': float(self.data[column].max()),
            'std': float(self.data[column].std()),
            'count': int(self.data[column].count())
        }

    def create_variable_dict(
        self,
        custom_vars: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create a complete variable dictionary for text substitution.

        Combines:
        - Date/time variables
        - Metadata
        - Custom variables

        Args:
            custom_vars: Custom variables to include

        Returns:
            Complete variable dictionary

        Example:
            variables = mapper.create_variable_dict({
                'company': 'BSH',
                'report_type': 'Monthly'
            })
        """
        variables = {
            'date': datetime.now().strftime('%Y-%m-%d'),
            'month': datetime.now().strftime('%B'),
            'year': datetime.now().strftime('%Y'),
            'day': datetime.now().strftime('%d'),
            'time': datetime.now().strftime('%H:%M'),
        }

        variables.update(self.metadata)

        if custom_vars:
            variables.update(custom_vars)

        return variables

    def reset(self) -> None:
        """Reset data and metadata to initial state."""
        self.data = None
        self.metadata = {}

    def get_info(self) -> Dict[str, Any]:
        """
        Get information about loaded data.

        Returns:
            Dictionary with data information
        """
        if self.data is None:
            return {'status': 'No data loaded'}

        return {
            'status': 'Data loaded',
            'rows': len(self.data),
            'columns': len(self.data.columns),
            'column_names': list(self.data.columns),
            'data_types': self.data.dtypes.to_dict(),
            'memory_usage': f"{self.data.memory_usage(deep=True).sum() / 1024:.2f} KB",
            'file_path': self.data_path,
            **self.metadata
        }


# Example usage
if __name__ == '__main__':
    print("=" * 60)
    print("DataMapper Test")
    print("=" * 60)

    # Create sample data
    sample_data = pd.DataFrame({
        'Kurum': ['BSH', 'Arçelik', 'Vestel', 'Beko'],
        'Toplam': [1234, 987, 654, 543],
        'Pozitif': [856, 654, 432, 378],
        'Negatif': [234, 187, 123, 98]
    })

    # Save to temp file
    temp_file = 'temp_test_data.xlsx'
    sample_data.to_excel(temp_file, index=False)

    try:
        # Test DataMapper
        print("\n1. Loading data:")
        mapper = DataMapper(temp_file)
        print(f"   ✅ Loaded {len(mapper.data)} rows")

        print("\n2. Getting column names:")
        columns = mapper.get_column_names()
        print(f"   Columns: {', '.join(columns)}")

        print("\n3. Applying column mapping:")
        mapping = {'Kurum': 'Company', 'Toplam': 'Total', 'Pozitif': 'Positive', 'Negatif': 'Negative'}
        mapper.apply_column_mapping(mapping)
        print(f"   ✅ Renamed: {', '.join(mapper.get_column_names())}")

        print("\n4. Getting summary statistics:")
        stats = mapper.get_summary_stats('Total')
        print(f"   Total - Sum: {stats['sum']}, Mean: {stats['mean']:.1f}")

        print("\n5. Creating variable dictionary:")
        variables = mapper.create_variable_dict({'company': 'BSH'})
        print(f"   ✅ Created {len(variables)} variables")

        print("\n6. Getting data for component:")
        config = {
            'type': 'table',
            'data_source': {
                'columns': ['Company', 'Total', 'Positive'],
                'sort_by': 'Total',
                'ascending': False,
                'top_n': 3
            }
        }
        component_data = mapper.get_data_for_component(config)
        print(f"   ✅ Retrieved {len(component_data)} rows for table component")

        print("\n" + "=" * 60)
        print("✅ DataMapper Test Complete!")
        print("=" * 60)

    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.remove(temp_file)
