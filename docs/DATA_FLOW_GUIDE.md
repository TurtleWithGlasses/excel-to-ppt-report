# Data Flow & Processing Guide
## Complete Data Pipeline Documentation

---

## 1. Overview

This guide explains how data flows through the system, from Excel upload to PPT generation.

---

## 2. Complete Data Flow Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                    1. DATA INGESTION                         │
│                                                               │
│  User Upload → Validation → Storage → Database Entry         │
│     Excel         Format      File        Metadata           │
│                   Check       System      Record             │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                    2. DATA PROCESSING                         │
│                                                               │
│  Read Excel → Parse Sheets → Data Cleaning → Normalization  │
│    pandas       openpyxl       Handle NaN      Type conv.    │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                    3. DATA ANALYSIS                           │
│                                                               │
│  Statistical → Trend → Anomaly → AI Insights                │
│   Analysis    Detection Detection  Generation                │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                    4. TEMPLATE MATCHING                       │
│                                                               │
│  Load Template → Map Data → Apply Rules → Validate          │
│    Config         to Sections  Processing    Mappings        │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                    5. CONTENT GENERATION                      │
│                                                               │
│  Generate Text → Create Charts → Format Tables → Build PPT  │
│    AI-powered     matplotlib      pandas styling   python-pptx │
└────────────────────────┬─────────────────────────────────────┘
                         │
┌────────────────────────▼─────────────────────────────────────┐
│                    6. OUTPUT DELIVERY                         │
│                                                               │
│  Save File → Update DB → Notify User → Provide Download     │
│   storage     status       webhook/email    API endpoint      │
└──────────────────────────────────────────────────────────────┘
```

---

## 3. Detailed Processing Steps

### 3.1 Data Ingestion

```python
class DataIngestionPipeline:
    """Handle Excel file upload and initial processing"""

    def __init__(self, storage_path: str):
        self.storage_path = storage_path
        self.allowed_extensions = ['.xlsx', '.xls', '.csv']
        self.max_file_size = 50 * 1024 * 1024  # 50MB

    async def ingest_file(
        self,
        file: UploadFile,
        client_id: str,
        user_id: str
    ) -> dict:
        """
        Complete ingestion workflow

        Returns:
            dict with upload_id, file_path, metadata
        """

        # Step 1: Validate file
        validation = await self._validate_file(file)
        if not validation['valid']:
            raise ValueError(f"Invalid file: {validation['error']}")

        # Step 2: Generate secure filename
        filename = self._generate_secure_filename(file.filename)

        # Step 3: Save to storage
        file_path = await self._save_file(file, filename)

        # Step 4: Create database entry
        upload_record = await self._create_upload_record(
            filename=filename,
            file_path=file_path,
            client_id=client_id,
            user_id=user_id,
            file_size=validation['size']
        )

        # Step 5: Initial data preview
        preview = await self._generate_preview(file_path)

        return {
            "upload_id": upload_record['id'],
            "file_path": file_path,
            "preview": preview,
            "metadata": upload_record
        }

    async def _validate_file(self, file: UploadFile) -> dict:
        """Validate uploaded file"""

        # Check extension
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in self.allowed_extensions:
            return {
                'valid': False,
                'error': f'Unsupported file type. Allowed: {self.allowed_extensions}'
            }

        # Check file size
        file.file.seek(0, 2)  # Seek to end
        file_size = file.file.tell()
        file.file.seek(0)  # Reset

        if file_size > self.max_file_size:
            return {
                'valid': False,
                'error': f'File too large. Max: {self.max_file_size} bytes'
            }

        # Check if file is readable
        try:
            if file_ext in ['.xlsx', '.xls']:
                pd.read_excel(file.file, nrows=1)
            else:
                pd.read_csv(file.file, nrows=1)

            file.file.seek(0)  # Reset

            return {'valid': True, 'size': file_size}

        except Exception as e:
            return {
                'valid': False,
                'error': f'Cannot read file: {str(e)}'
            }

    def _generate_secure_filename(self, original_filename: str) -> str:
        """Generate secure, unique filename"""

        # Extract extension
        _, ext = os.path.splitext(original_filename)

        # Generate unique ID
        unique_id = uuid.uuid4().hex

        # Sanitize original name
        safe_name = re.sub(r'[^a-zA-Z0-9_-]', '_', original_filename)
        safe_name = safe_name[:50]  # Limit length

        # Combine
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        return f"{safe_name}_{timestamp}_{unique_id}{ext}"

    async def _save_file(self, file: UploadFile, filename: str) -> str:
        """Save file to storage"""

        file_path = os.path.join(self.storage_path, filename)

        # Save file
        with open(file_path, 'wb') as f:
            content = await file.read()
            f.write(content)

        return file_path

    async def _generate_preview(self, file_path: str) -> dict:
        """Generate quick preview of file contents"""

        # Read first few rows
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path, nrows=5)
        else:
            df = pd.read_excel(file_path, nrows=5)

        return {
            "columns": df.columns.tolist(),
            "sample_data": df.to_dict('records'),
            "row_count_preview": len(df)
        }
```

### 3.2 Data Processing & Cleaning

```python
class DataProcessor:
    """Process and clean Excel data"""

    def __init__(self):
        self.numeric_columns = []
        self.categorical_columns = []
        self.date_columns = []

    def process_excel(self, file_path: str) -> dict:
        """
        Process Excel file and return structured data

        Returns:
            dict with processed DataFrames for each sheet
        """

        # Step 1: Load all sheets
        excel_file = pd.ExcelFile(file_path)
        sheets = {}

        for sheet_name in excel_file.sheet_names:
            df = excel_file.parse(sheet_name)

            # Step 2: Clean data
            df_cleaned = self._clean_dataframe(df)

            # Step 3: Detect column types
            column_types = self._detect_column_types(df_cleaned)

            # Step 4: Normalize data
            df_normalized = self._normalize_dataframe(df_cleaned, column_types)

            sheets[sheet_name] = {
                "data": df_normalized,
                "column_types": column_types,
                "metadata": self._generate_sheet_metadata(df_normalized)
            }

        return sheets

    def _clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Clean DataFrame"""

        df_clean = df.copy()

        # Remove completely empty rows/columns
        df_clean = df_clean.dropna(how='all', axis=0)
        df_clean = df_clean.dropna(how='all', axis=1)

        # Strip whitespace from column names
        df_clean.columns = df_clean.columns.str.strip()

        # Strip whitespace from string columns
        string_columns = df_clean.select_dtypes(include=['object']).columns
        for col in string_columns:
            df_clean[col] = df_clean[col].str.strip() if isinstance(df_clean[col].iloc[0], str) else df_clean[col]

        # Remove duplicate rows
        df_clean = df_clean.drop_duplicates()

        return df_clean

    def _detect_column_types(self, df: pd.DataFrame) -> dict:
        """Detect semantic column types"""

        column_types = {}

        for col in df.columns:
            col_type = self._detect_single_column_type(df[col])
            column_types[col] = col_type

        return column_types

    def _detect_single_column_type(self, series: pd.Series) -> str:
        """Detect type of a single column"""

        # Check if numeric
        if pd.api.types.is_numeric_dtype(series):
            # Check if it's a percentage
            if series.between(0, 1).all() or series.between(0, 100).all():
                return "percentage"
            # Check if it's currency
            elif series.min() >= 0 and series.max() > 1000:
                return "currency"
            else:
                return "numeric"

        # Check if datetime
        elif pd.api.types.is_datetime64_any_dtype(series):
            return "datetime"

        # Check if it looks like a date string
        elif self._is_date_string(series):
            return "date_string"

        # Check if categorical
        elif len(series.unique()) / len(series) < 0.5:
            return "categorical"

        else:
            return "text"

    def _is_date_string(self, series: pd.Series) -> bool:
        """Check if column contains date strings"""

        # Sample first non-null value
        sample = series.dropna().iloc[0] if len(series.dropna()) > 0 else None

        if sample is None or not isinstance(sample, str):
            return False

        # Try to parse as date
        try:
            pd.to_datetime(series.dropna().head(10))
            return True
        except:
            return False

    def _normalize_dataframe(self, df: pd.DataFrame, column_types: dict) -> pd.DataFrame:
        """Normalize data based on detected types"""

        df_norm = df.copy()

        for col, col_type in column_types.items():
            if col_type == "date_string":
                # Convert to datetime
                df_norm[col] = pd.to_datetime(df_norm[col], errors='coerce')

            elif col_type == "percentage":
                # Normalize to 0-1 range if needed
                if df_norm[col].max() > 1:
                    df_norm[col] = df_norm[col] / 100

            elif col_type == "currency":
                # Remove currency symbols if present
                if df_norm[col].dtype == 'object':
                    df_norm[col] = df_norm[col].str.replace('[$,]', '', regex=True).astype(float)

        return df_norm

    def _generate_sheet_metadata(self, df: pd.DataFrame) -> dict:
        """Generate metadata about the sheet"""

        return {
            "row_count": len(df),
            "column_count": len(df.columns),
            "columns": df.columns.tolist(),
            "memory_usage": df.memory_usage(deep=True).sum(),
            "null_counts": df.isnull().sum().to_dict()
        }
```

### 3.3 Data-to-Template Mapping

```python
class DataTemplateMapper:
    """Map processed data to template sections"""

    def __init__(self, template_config: dict):
        self.template = template_config
        self.mappings = {}

    def map_data_to_template(self, processed_data: dict) -> dict:
        """
        Map processed Excel data to template sections

        Args:
            processed_data: Output from DataProcessor

        Returns:
            dict with section_id -> data mappings
        """

        section_mappings = {}

        for section in self.template['sections']:
            section_id = section['id']
            section_type = section['type']

            # Get data source configuration
            data_sources = section.get('data_sources', [])

            if section_type == 'text_analysis':
                # AI-generated content - collect all relevant data
                section_data = self._collect_text_analysis_data(
                    processed_data,
                    data_sources
                )

            elif section_type == 'data_table':
                # Table display - extract specific sheet/range
                section_data = self._extract_table_data(
                    processed_data,
                    data_sources,
                    section.get('filters', [])
                )

            elif section_type == 'visualization':
                # Chart data - prepare for visualization
                section_data = self._prepare_chart_data(
                    processed_data,
                    data_sources,
                    section.get('chart_type')
                )

            section_mappings[section_id] = {
                "type": section_type,
                "data": section_data,
                "config": section
            }

        return section_mappings

    def _collect_text_analysis_data(
        self,
        processed_data: dict,
        data_sources: list
    ) -> dict:
        """Collect data for AI text analysis"""

        collected_data = {}

        for source in data_sources:
            sheet_name = source.get('sheet')
            range_spec = source.get('range', 'all')

            if sheet_name in processed_data:
                sheet_data = processed_data[sheet_name]
                df = sheet_data['data']

                # Apply range if specified
                if range_spec != 'all':
                    df = self._apply_range(df, range_spec)

                collected_data[sheet_name] = {
                    "dataframe": df,
                    "summary": df.describe().to_dict(),
                    "column_types": sheet_data['column_types']
                }

        return collected_data

    def _extract_table_data(
        self,
        processed_data: dict,
        data_sources: list,
        filters: list
    ) -> pd.DataFrame:
        """Extract and filter data for table display"""

        # Get primary data source
        primary_source = data_sources[0]
        sheet_name = primary_source.get('sheet')

        df = processed_data[sheet_name]['data'].copy()

        # Apply filters
        for filter_rule in filters:
            df = self._apply_filter(df, filter_rule)

        return df

    def _prepare_chart_data(
        self,
        processed_data: dict,
        data_sources: list,
        chart_type: str
    ) -> dict:
        """Prepare data for chart generation"""

        source = data_sources[0]
        sheet_name = source.get('sheet')
        df = processed_data[sheet_name]['data']

        # Extract relevant columns
        x_column = source.get('x_axis')
        y_columns = source.get('y_axis', [])

        chart_data = {
            "chart_type": chart_type,
            "x_values": df[x_column].tolist() if x_column else None,
            "y_series": {}
        }

        for y_col in y_columns:
            chart_data["y_series"][y_col] = df[y_col].tolist()

        return chart_data

    def _apply_filter(self, df: pd.DataFrame, filter_rule: dict) -> pd.DataFrame:
        """Apply filter rule to DataFrame"""

        column = filter_rule['column']
        operator = filter_rule['operator']
        value = filter_rule['value']

        if operator == 'equals':
            return df[df[column] == value]
        elif operator == 'not_equals':
            return df[df[column] != value]
        elif operator == 'greater_than':
            return df[df[column] > value]
        elif operator == 'less_than':
            return df[df[column] < value]
        elif operator == 'contains':
            return df[df[column].str.contains(value, na=False)]

        return df
```

---

## 4. Monthly/Quarterly/Annual Reports

### 4.1 Historical Data Aggregation

```python
class HistoricalDataAggregator:
    """Aggregate data across time periods"""

    def __init__(self, db_session):
        self.db = db_session

    def generate_periodic_report(
        self,
        client_id: str,
        period_type: str,  # 'monthly', 'quarterly', 'annual'
        end_date: datetime,
        num_periods: int = 12
    ) -> dict:
        """
        Generate report aggregating multiple periods

        Args:
            client_id: Client identifier
            period_type: Type of period
            end_date: End date for the report
            num_periods: Number of periods to include

        Returns:
            Aggregated data ready for reporting
        """

        # Step 1: Calculate date ranges
        periods = self._calculate_periods(period_type, end_date, num_periods)

        # Step 2: Fetch data for each period
        period_data = []
        for period in periods:
            data = self._fetch_period_data(
                client_id,
                period['start'],
                period['end']
            )
            period_data.append({
                "period": period,
                "data": data
            })

        # Step 3: Aggregate across periods
        aggregated = self._aggregate_data(period_data, period_type)

        # Step 4: Calculate trends
        trends = self._calculate_trends(aggregated)

        # Step 5: Generate comparisons
        comparisons = self._generate_comparisons(aggregated)

        return {
            "periods": periods,
            "raw_data": period_data,
            "aggregated": aggregated,
            "trends": trends,
            "comparisons": comparisons
        }

    def _calculate_periods(
        self,
        period_type: str,
        end_date: datetime,
        num_periods: int
    ) -> list:
        """Calculate period date ranges"""

        periods = []

        for i in range(num_periods):
            if period_type == 'monthly':
                period_end = end_date - relativedelta(months=i)
                period_start = period_end.replace(day=1)

            elif period_type == 'quarterly':
                quarter_offset = i * 3
                period_end = end_date - relativedelta(months=quarter_offset)
                # Start of quarter
                quarter_start_month = ((period_end.month - 1) // 3) * 3 + 1
                period_start = period_end.replace(month=quarter_start_month, day=1)

            elif period_type == 'annual':
                period_end = end_date - relativedelta(years=i)
                period_start = period_end.replace(month=1, day=1)

            periods.append({
                "start": period_start,
                "end": period_end,
                "label": self._format_period_label(period_start, period_type)
            })

        return list(reversed(periods))  # Chronological order

    def _format_period_label(self, date: datetime, period_type: str) -> str:
        """Format period label"""

        if period_type == 'monthly':
            return date.strftime('%B %Y')
        elif period_type == 'quarterly':
            quarter = (date.month - 1) // 3 + 1
            return f"Q{quarter} {date.year}"
        elif period_type == 'annual':
            return str(date.year)

    def _fetch_period_data(
        self,
        client_id: str,
        start_date: datetime,
        end_date: datetime
    ) -> dict:
        """Fetch all data uploads for a period"""

        # Query database for uploads in date range
        result = self.db.execute(
            """
            SELECT * FROM data_uploads
            WHERE client_id = :client_id
              AND upload_date BETWEEN :start_date AND :end_date
            ORDER BY upload_date
            """,
            {
                "client_id": client_id,
                "start_date": start_date,
                "end_date": end_date
            }
        )

        uploads = result.fetchall()

        # Aggregate data from all uploads
        combined_data = self._combine_uploads(uploads)

        return combined_data

    def _aggregate_data(self, period_data: list, period_type: str) -> dict:
        """Aggregate metrics across periods"""

        # Extract key metrics from each period
        metrics = {}

        for period_entry in period_data:
            period_label = period_entry['period']['label']
            data = period_entry['data']

            # Calculate aggregates for this period
            period_metrics = self._calculate_period_metrics(data)

            metrics[period_label] = period_metrics

        return metrics

    def _calculate_trends(self, aggregated_data: dict) -> dict:
        """Calculate trends across periods"""

        trends = {}

        # For each metric, calculate trend
        all_periods = list(aggregated_data.keys())

        if len(all_periods) < 2:
            return trends

        # Get list of all metrics
        first_period_metrics = aggregated_data[all_periods[0]]

        for metric_name in first_period_metrics.keys():
            values = [
                aggregated_data[period].get(metric_name, 0)
                for period in all_periods
            ]

            # Calculate trend direction and strength
            trend_info = self._calculate_trend_info(values)

            trends[metric_name] = trend_info

        return trends

    def _generate_comparisons(self, aggregated_data: dict) -> dict:
        """Generate period-over-period comparisons"""

        comparisons = {}
        periods = list(aggregated_data.keys())

        if len(periods) < 2:
            return comparisons

        current_period = periods[-1]
        previous_period = periods[-2]

        current_data = aggregated_data[current_period]
        previous_data = aggregated_data[previous_period]

        for metric in current_data.keys():
            current_value = current_data[metric]
            previous_value = previous_data.get(metric, 0)

            if previous_value > 0:
                change_pct = ((current_value - previous_value) / previous_value) * 100
            else:
                change_pct = 0

            comparisons[metric] = {
                "current": current_value,
                "previous": previous_value,
                "change": current_value - previous_value,
                "change_percent": change_pct,
                "direction": "up" if change_pct > 0 else "down"
            }

        return comparisons
```

---

## 5. Data Storage Strategy

### 5.1 Storage Architecture

```
┌─────────────────────────────────────────────────┐
│              File Storage Layer                  │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐      │
│  │  Uploads │  │ Templates │  │ Reports  │      │
│  │  Bucket  │  │  Bucket   │  │  Bucket  │      │
│  └──────────┘  └──────────┘  └──────────┘      │
│        (S3 / MinIO / Local FS)                  │
└─────────────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────┐
│           Database Storage Layer                │
│  ┌─────────────────────────────────────────┐   │
│  │  Metadata, References, Relationships    │   │
│  │  (PostgreSQL)                            │   │
│  └─────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

### 5.2 Data Retention Policy

```python
class DataRetentionManager:
    """Manage data lifecycle and retention"""

    def __init__(self):
        self.retention_policies = {
            "uploads": 90,  # days
            "reports": 365,
            "archive": -1  # indefinite
        }

    async def apply_retention_policy(self):
        """Apply retention policies"""

        # Archive old data
        await self._archive_old_data()

        # Delete expired data
        await self._delete_expired_data()

    async def _archive_old_data(self):
        """Move old data to archive storage"""

        cutoff_date = datetime.now() - timedelta(days=30)

        # Archive old uploads
        old_uploads = self.db.query(DataUpload).filter(
            DataUpload.upload_date < cutoff_date
        ).all()

        for upload in old_uploads:
            # Compress and move to archive
            await self._archive_file(upload.file_path)

            # Update database
            upload.archived = True
            upload.archive_date = datetime.now()

        self.db.commit()
```

---

**This guide covers the complete data flow from ingestion to output. Update as processing logic evolves.**
