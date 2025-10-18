# AI Integration Guide
## Detailed Implementation Strategy

---

## 1. Overview

This guide explains how to integrate and train AI models for automated report generation.

---

## 2. AI System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User Input Layer                       │
│  (Excel Data + Template + Historical Context)           │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              AI Processing Pipeline                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐    │
│  │   Data      │→ │  Context    │→ │  Content    │    │
│  │  Analysis   │  │  Builder    │  │ Generation  │    │
│  └─────────────┘  └─────────────┘  └─────────────┘    │
└────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────┐
│              Output Generation                           │
│  (AI-generated insights + Recommendations)              │
└─────────────────────────────────────────────────────────┘
```

---

## 3. AI Components

### 3.1 Data Analysis Module

**Purpose**: Analyze Excel data to extract patterns, trends, and anomalies.

**Implementation**:

```python
class AIDataAnalyzer:
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)
        self.analysis_cache = {}

    async def analyze_dataset(self, df: pd.DataFrame, context: dict) -> dict:
        """
        Analyze a pandas DataFrame and extract insights.

        Args:
            df: Input DataFrame
            context: Additional context (client info, report type, etc.)

        Returns:
            Dictionary containing analysis results
        """
        # Step 1: Generate statistical summary
        stats = self._generate_statistics(df)

        # Step 2: Identify trends
        trends = self._identify_trends(df)

        # Step 3: Detect anomalies
        anomalies = self._detect_anomalies(df)

        # Step 4: Create AI prompt
        prompt = self._build_analysis_prompt(stats, trends, anomalies, context)

        # Step 5: Get AI insights
        insights = await self._get_ai_insights(prompt)

        return {
            "statistics": stats,
            "trends": trends,
            "anomalies": anomalies,
            "ai_insights": insights,
            "recommendations": self._generate_recommendations(insights)
        }

    def _generate_statistics(self, df: pd.DataFrame) -> dict:
        """Generate comprehensive statistics"""
        return {
            "summary": df.describe().to_dict(),
            "missing_values": df.isnull().sum().to_dict(),
            "data_types": df.dtypes.astype(str).to_dict(),
            "row_count": len(df),
            "column_count": len(df.columns),
            "numeric_columns": df.select_dtypes(include=['number']).columns.tolist(),
            "categorical_columns": df.select_dtypes(include=['object']).columns.tolist()
        }

    def _identify_trends(self, df: pd.DataFrame) -> list:
        """Identify trends in time-series or sequential data"""
        trends = []

        # Look for date columns
        date_columns = df.select_dtypes(include=['datetime64']).columns

        for date_col in date_columns:
            # For each numeric column, analyze trend over time
            numeric_cols = df.select_dtypes(include=['number']).columns

            for num_col in numeric_cols:
                # Simple trend detection using linear regression
                from sklearn.linear_model import LinearRegression

                df_sorted = df.sort_values(date_col)
                X = np.arange(len(df_sorted)).reshape(-1, 1)
                y = df_sorted[num_col].values

                # Remove NaN values
                valid_idx = ~np.isnan(y)
                if valid_idx.sum() > 1:
                    model = LinearRegression()
                    model.fit(X[valid_idx], y[valid_idx])

                    slope = model.coef_[0]
                    trend_direction = "increasing" if slope > 0 else "decreasing"

                    trends.append({
                        "metric": num_col,
                        "time_column": date_col,
                        "direction": trend_direction,
                        "slope": float(slope),
                        "strength": abs(slope)
                    })

        return sorted(trends, key=lambda x: x["strength"], reverse=True)

    def _detect_anomalies(self, df: pd.DataFrame) -> list:
        """Detect anomalies using statistical methods"""
        anomalies = []

        for col in df.select_dtypes(include=['number']).columns:
            values = df[col].dropna()

            if len(values) > 0:
                # Use IQR method for anomaly detection
                Q1 = values.quantile(0.25)
                Q3 = values.quantile(0.75)
                IQR = Q3 - Q1

                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR

                outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)]

                if len(outliers) > 0:
                    anomalies.append({
                        "column": col,
                        "count": len(outliers),
                        "percentage": (len(outliers) / len(df)) * 100,
                        "values": outliers[col].tolist()[:10]  # Limit to 10 examples
                    })

        return anomalies

    def _build_analysis_prompt(self, stats: dict, trends: list,
                                anomalies: list, context: dict) -> str:
        """Build comprehensive prompt for AI analysis"""

        prompt = f"""You are a data analyst reviewing {context.get('report_type', 'business')} data
for {context.get('client_name', 'a client')}.

**Dataset Overview:**
- Rows: {stats['row_count']}
- Columns: {stats['column_count']}
- Numeric metrics: {', '.join(stats['numeric_columns'])}

**Key Statistics:**
{json.dumps(stats['summary'], indent=2)}

**Identified Trends:**
{json.dumps(trends[:5], indent=2)}

**Anomalies Detected:**
{json.dumps(anomalies[:3], indent=2)}

**Task:**
1. Provide 3-5 key insights about this data
2. Highlight the most important trends
3. Explain any significant anomalies
4. Suggest 2-3 actionable recommendations

**Format your response as JSON:**
{{
    "key_insights": ["insight1", "insight2", ...],
    "trend_summary": "brief summary",
    "anomaly_explanation": "explanation if any",
    "recommendations": ["rec1", "rec2", ...]
}}
"""
        return prompt

    async def _get_ai_insights(self, prompt: str) -> dict:
        """Call OpenAI API to generate insights"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an expert data analyst."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )

            content = response.choices[0].message.content

            # Try to parse as JSON
            try:
                return json.loads(content)
            except json.JSONDecodeError:
                # If not JSON, return as text
                return {"raw_analysis": content}

        except Exception as e:
            return {"error": str(e)}

    def _generate_recommendations(self, insights: dict) -> list:
        """Generate actionable recommendations"""
        recommendations = insights.get("recommendations", [])

        # Add default recommendations based on common patterns
        if not recommendations:
            recommendations = [
                "Continue monitoring key metrics for trend changes",
                "Investigate any identified anomalies for root causes",
                "Set up alerts for metrics approaching critical thresholds"
            ]

        return recommendations
```

### 3.2 Content Generation Module

**Purpose**: Generate executive summaries, descriptions, and narrative content.

```python
class AIContentGenerator:
    def __init__(self, openai_api_key: str):
        self.client = OpenAI(api_key=openai_api_key)

    async def generate_executive_summary(
        self,
        data_insights: dict,
        template_config: dict,
        client_context: dict
    ) -> str:
        """
        Generate executive summary for the report.

        Args:
            data_insights: Results from AIDataAnalyzer
            template_config: Template configuration
            client_context: Client-specific preferences

        Returns:
            Generated executive summary text
        """

        # Build context-aware prompt
        prompt = self._build_summary_prompt(
            data_insights,
            template_config,
            client_context
        )

        # Get AI-generated content
        summary = await self._generate_content(
            prompt,
            max_tokens=500,
            temperature=0.7
        )

        return summary

    def _build_summary_prompt(self, insights: dict,
                              template: dict, context: dict) -> str:
        """Build prompt for executive summary"""

        tone = context.get("tone", "professional")
        length = context.get("summary_length", "medium")  # brief/medium/detailed

        length_guidelines = {
            "brief": "2-3 sentences",
            "medium": "1 paragraph (4-6 sentences)",
            "detailed": "2-3 paragraphs"
        }

        prompt = f"""Generate an executive summary for a {template.get('report_type', 'business')} report.

**Tone**: {tone}
**Length**: {length_guidelines.get(length, 'medium')}

**Data Insights:**
{json.dumps(insights.get('key_insights', []), indent=2)}

**Trends:**
{json.dumps(insights.get('trends', [])[:3], indent=2)}

**Requirements:**
- Start with the most important finding
- Use business language, avoid technical jargon
- Include specific numbers when relevant
- End with forward-looking statement

Write the executive summary now:
"""
        return prompt

    async def _generate_content(self, prompt: str,
                                 max_tokens: int = 500,
                                 temperature: float = 0.7) -> str:
        """Generate content using OpenAI"""

        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional business writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens
        )

        return response.choices[0].message.content.strip()

    async def generate_chart_description(
        self,
        chart_data: dict,
        chart_type: str
    ) -> str:
        """Generate description for a chart"""

        prompt = f"""Describe this {chart_type} chart in 1-2 sentences:

**Data:**
{json.dumps(chart_data, indent=2)}

Focus on the main trend or comparison shown in the chart.
"""

        return await self._generate_content(prompt, max_tokens=150)
```

---

## 4. Training the AI System

### 4.1 Knowledge Base Creation

```python
class AIKnowledgeBase:
    """Store and manage AI training examples"""

    def __init__(self, db_session):
        self.db = db_session

    def add_training_example(
        self,
        client_id: str,
        excel_data: dict,
        ppt_content: dict,
        metadata: dict
    ):
        """
        Store a training example (Excel + PPT pair)

        Args:
            client_id: Client identifier
            excel_data: Structured Excel data
            ppt_content: Text content from PPT slides
            metadata: Additional context
        """

        training_example = {
            "client_id": client_id,
            "input_data": excel_data,
            "expected_output": ppt_content,
            "metadata": metadata,
            "created_at": datetime.now()
        }

        # Store in database
        self.db.execute(
            """
            INSERT INTO ai_training_examples
            (client_id, input_data, expected_output, metadata, created_at)
            VALUES (:client_id, :input_data, :expected_output, :metadata, :created_at)
            """,
            training_example
        )
        self.db.commit()

    def get_client_examples(self, client_id: str, limit: int = 10) -> list:
        """Retrieve training examples for a specific client"""

        result = self.db.execute(
            """
            SELECT * FROM ai_training_examples
            WHERE client_id = :client_id
            ORDER BY created_at DESC
            LIMIT :limit
            """,
            {"client_id": client_id, "limit": limit}
        )

        return result.fetchall()

    def build_few_shot_examples(self, client_id: str, n: int = 3) -> str:
        """Build few-shot learning examples for prompts"""

        examples = self.get_client_examples(client_id, n)

        few_shot_text = ""
        for i, example in enumerate(examples, 1):
            few_shot_text += f"""
Example {i}:
Input Data: {json.dumps(example['input_data'], indent=2)}
Generated Content: {example['expected_output']}

"""

        return few_shot_text
```

### 4.2 Training Database Schema

```sql
-- AI Training Examples Table
CREATE TABLE ai_training_examples (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES clients(id),
    input_data JSONB NOT NULL,  -- Excel data structure
    expected_output JSONB NOT NULL,  -- PPT content
    metadata JSONB,  -- Additional context
    quality_score FLOAT,  -- User rating (1-5)
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- AI Feedback Table
CREATE TABLE ai_feedback (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    report_id UUID REFERENCES reports(id),
    ai_generated_content TEXT NOT NULL,
    user_edited_content TEXT,
    feedback_type VARCHAR(50),  -- 'correction', 'improvement', 'approval'
    rating INTEGER,  -- 1-5 stars
    comments TEXT,
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Client AI Preferences
CREATE TABLE client_ai_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    client_id UUID REFERENCES clients(id),
    tone VARCHAR(50) DEFAULT 'professional',  -- casual, professional, technical
    summary_length VARCHAR(50) DEFAULT 'medium',  -- brief, medium, detailed
    custom_prompts JSONB,  -- Custom prompt templates
    terminology JSONB,  -- Industry-specific terms
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(client_id)
);
```

---

## 5. Feedback Loop System

### 5.1 Learning from User Edits

```python
class AIFeedbackSystem:
    """Capture and learn from user feedback"""

    def __init__(self, db_session):
        self.db = db_session

    async def capture_edit_feedback(
        self,
        report_id: str,
        original_content: str,
        edited_content: str,
        user_id: str
    ):
        """Capture when user edits AI-generated content"""

        # Calculate edit distance to measure significance
        edit_distance = self._calculate_edit_distance(
            original_content,
            edited_content
        )

        # Store feedback
        feedback = {
            "report_id": report_id,
            "ai_generated_content": original_content,
            "user_edited_content": edited_content,
            "feedback_type": "correction" if edit_distance > 0.3 else "improvement",
            "created_by": user_id,
            "edit_similarity": 1 - edit_distance
        }

        self.db.execute(
            """
            INSERT INTO ai_feedback
            (report_id, ai_generated_content, user_edited_content,
             feedback_type, created_by)
            VALUES (:report_id, :ai_generated_content, :user_edited_content,
                    :feedback_type, :created_by)
            """,
            feedback
        )
        self.db.commit()

        # Trigger learning process
        await self._update_ai_model(feedback)

    def _calculate_edit_distance(self, text1: str, text2: str) -> float:
        """Calculate normalized edit distance"""
        from difflib import SequenceMatcher

        return 1 - SequenceMatcher(None, text1, text2).ratio()

    async def _update_ai_model(self, feedback: dict):
        """Update AI prompts based on feedback"""

        # Extract patterns from edits
        patterns = self._extract_edit_patterns(feedback)

        # Update client-specific preferences
        # This could involve updating prompt templates,
        # adjusting tone, or modifying terminology

        pass

    def _extract_edit_patterns(self, feedback: dict) -> list:
        """Extract common patterns from user edits"""
        # Analyze what users consistently change
        # Return list of patterns

        return []
```

---

## 6. Implementation Workflow

### Step-by-Step Integration

```python
# Example: Complete AI workflow for report generation

async def generate_report_with_ai(
    excel_file: str,
    template_id: str,
    client_id: str
) -> str:
    """
    Complete workflow for AI-powered report generation
    """

    # Step 1: Load and process Excel data
    excel_processor = ExcelProcessor()
    df = excel_processor.load_file(excel_file)

    # Step 2: Analyze data with AI
    ai_analyzer = AIDataAnalyzer(openai_api_key=settings.OPENAI_API_KEY)

    context = {
        "client_name": get_client_name(client_id),
        "report_type": get_template_type(template_id)
    }

    analysis = await ai_analyzer.analyze_dataset(df, context)

    # Step 3: Generate content
    content_generator = AIContentGenerator(openai_api_key=settings.OPENAI_API_KEY)

    template_config = get_template_config(template_id)
    client_context = get_client_preferences(client_id)

    executive_summary = await content_generator.generate_executive_summary(
        analysis,
        template_config,
        client_context
    )

    # Step 4: Create PPT
    ppt_generator = PPTGenerator()
    ppt_file = ppt_generator.create_presentation(
        data=df,
        analysis=analysis,
        summary=executive_summary,
        template=template_config
    )

    return ppt_file
```

---

## 7. Best Practices

### 7.1 Prompt Engineering

- **Be Specific**: Clearly define expected output format
- **Provide Context**: Include relevant background information
- **Use Examples**: Few-shot learning improves accuracy
- **Set Constraints**: Specify length, tone, and style
- **Iterate**: Test and refine prompts based on results

### 7.2 Cost Optimization

```python
class AIOptimizer:
    """Optimize AI usage for cost efficiency"""

    def __init__(self):
        self.cache = {}  # Simple cache for repeated requests

    async def cached_ai_call(self, prompt: str, cache_key: str):
        """Cache AI responses to avoid duplicate calls"""

        if cache_key in self.cache:
            return self.cache[cache_key]

        response = await self.call_openai(prompt)
        self.cache[cache_key] = response

        return response

    def batch_analyze(self, datasets: list) -> list:
        """Batch multiple analyses into single API call"""

        # Combine multiple data analyses into one prompt
        combined_prompt = self._build_batch_prompt(datasets)

        # Single API call
        results = self.call_openai(combined_prompt)

        # Split results
        return self._split_batch_results(results)
```

### 7.3 Error Handling

```python
async def safe_ai_call(prompt: str, fallback_content: str = None):
    """AI call with retry logic and fallback"""

    max_retries = 3

    for attempt in range(max_retries):
        try:
            response = await call_openai(prompt)
            return response

        except RateLimitError:
            # Wait and retry
            await asyncio.sleep(2 ** attempt)

        except Exception as e:
            logger.error(f"AI call failed: {e}")

            if attempt == max_retries - 1:
                # Return fallback content
                return fallback_content or "Content generation unavailable"
```

---

## 8. Monitoring and Evaluation

### 8.1 Metrics to Track

```python
class AIMetrics:
    """Track AI performance metrics"""

    metrics = {
        "api_calls": 0,
        "total_tokens": 0,
        "average_response_time": 0,
        "error_rate": 0,
        "user_satisfaction": 0,  # Based on ratings
        "edit_rate": 0  # How often users edit AI content
    }

    def track_call(self, tokens: int, response_time: float, success: bool):
        """Track individual API call"""

        self.metrics["api_calls"] += 1
        self.metrics["total_tokens"] += tokens

        # Update average response time
        n = self.metrics["api_calls"]
        self.metrics["average_response_time"] = (
            (self.metrics["average_response_time"] * (n-1) + response_time) / n
        )

        if not success:
            self.metrics["error_rate"] = (
                (self.metrics["error_rate"] * (n-1) + 1) / n
            )
```

---

## 9. Next Steps

1. **Implement Core AI Services**
   - Create `AIDataAnalyzer` class
   - Implement `AIContentGenerator`
   - Set up OpenAI integration

2. **Create Training Pipeline**
   - Set up database tables
   - Build knowledge base system
   - Implement feedback capture

3. **Test and Iterate**
   - Test with sample data
   - Gather user feedback
   - Refine prompts

4. **Optimize**
   - Implement caching
   - Add batch processing
   - Monitor costs

---

**This is a living document. Update as the AI system evolves.**
