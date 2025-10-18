"""
AI-powered data analysis service using OpenAI API.
"""
from typing import Dict, List, Any, Optional
import pandas as pd
import logging
from openai import OpenAI
from app.core.config import settings

logger = logging.getLogger(__name__)


class AIAnalyzer:
    """Service for AI-powered data analysis and content generation."""
    
    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
    
    def analyze_dataframe(self, df: pd.DataFrame, context: str = "") -> str:
        """
        Analyze a DataFrame and generate insights using AI.
        """
        try:
            # Prepare data summary
            summary = self._prepare_data_summary(df)
            
            # Create prompt
            prompt = f"""
            Analyze the following data and provide key insights:
            
            Context: {context}
            
            Data Summary:
            - Total Rows: {summary['rows']}
            - Total Columns: {summary['columns']}
            - Column Names: {', '.join(summary['column_names'])}
            
            Sample Data:
            {summary['sample_data']}
            
            Statistical Summary:
            {summary['statistics']}
            
            Please provide:
            1. Key findings and trends
            2. Notable patterns or anomalies
            3. Actionable insights
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a data analyst expert. Provide clear, concise insights from data."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            insights = response.choices[0].message.content
            logger.info("AI analysis completed successfully")
            return insights
        
        except Exception as e:
            logger.error(f"Error in AI analysis: {str(e)}")
            return f"Unable to generate AI insights: {str(e)}"
    
    def generate_executive_summary(self, data_sheets: Dict[str, pd.DataFrame]) -> str:
        """
        Generate an executive summary from multiple data sheets.
        """
        try:
            # Prepare overview of all sheets
            overview = []
            for sheet_name, df in data_sheets.items():
                overview.append(f"- {sheet_name}: {len(df)} rows, {len(df.columns)} columns")
            
            prompt = f"""
            Generate an executive summary for a business report based on the following data:
            
            Data Overview:
            {chr(10).join(overview)}
            
            Please provide a concise executive summary (3-5 paragraphs) that includes:
            1. Overview of the data scope
            2. Key performance indicators
            3. Main trends and patterns
            4. Critical findings
            5. Recommendations
            """
            
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a business analyst creating executive summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=self.max_tokens,
                temperature=0.7
            )
            
            summary = response.choices[0].message.content
            logger.info("Executive summary generated successfully")
            return summary
        
        except Exception as e:
            logger.error(f"Error generating executive summary: {str(e)}")
            return f"Unable to generate executive summary: {str(e)}"
    
    def detect_anomalies(self, df: pd.DataFrame, column: str) -> Dict[str, Any]:
        """
        Detect anomalies in a specific column using statistical methods and AI.
        """
        try:
            if column not in df.columns:
                raise ValueError(f"Column {column} not found in DataFrame")
            
            # Calculate basic statistics
            data = df[column].dropna()
            mean = data.mean()
            std = data.std()
            
            # Identify outliers (values beyond 3 standard deviations)
            outliers = df[abs(df[column] - mean) > 3 * std]
            
            result = {
                'column': column,
                'total_values': len(data),
                'mean': float(mean),
                'std': float(std),
                'outliers_count': len(outliers),
                'outlier_indices': outliers.index.tolist()
            }
            
            logger.info(f"Anomaly detection completed for column: {column}")
            return result
        
        except Exception as e:
            logger.error(f"Error in anomaly detection: {str(e)}")
            return {'error': str(e)}
    
    def generate_insights_for_sections(
        self, 
        template_sections: List[Dict[str, Any]],
        data_sheets: Dict[str, pd.DataFrame]
    ) -> Dict[str, str]:
        """
        Generate AI insights for each section in the template.
        """
        insights = {}
        
        for section in template_sections:
            section_name = section.get('name', 'Untitled')
            section_type = section.get('type', 'text_analysis')
            
            if section_type == 'text_analysis' and section.get('ai_processing', False):
                data_source = section.get('data_source', [])
                
                if data_source and len(data_source) > 0:
                    sheet_name = data_source[0].split('.')[0] if '.' in data_source[0] else data_source[0]
                    
                    if sheet_name in data_sheets:
                        df = data_sheets[sheet_name]
                        insights[section_name] = self.analyze_dataframe(df, context=section_name)
                    else:
                        insights[section_name] = f"Data source '{sheet_name}' not found."
                else:
                    # Generate general summary
                    insights[section_name] = self.generate_executive_summary(data_sheets)
        
        logger.info(f"Generated insights for {len(insights)} sections")
        return insights
    
    def _prepare_data_summary(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Prepare a summary of the DataFrame for AI analysis.
        """
        numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
        
        return {
            'rows': len(df),
            'columns': len(df.columns),
            'column_names': df.columns.tolist(),
            'sample_data': df.head(5).to_string(),
            'statistics': df[numeric_cols].describe().to_string() if len(numeric_cols) > 0 else "No numeric columns"
        }

