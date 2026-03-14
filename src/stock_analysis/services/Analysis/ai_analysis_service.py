from openai import OpenAI
from pydantic import ValidationError
import logging
import openai
from stock_analysis.schemas.analysis import (
    AnalysisRequest,
    StockInsightResponse,
    RiskLevel,
    TrendSignal,
)
from stock_analysis.core.exceptions import (
    AIRateLimitError,
    AIResponseValidation,
    AIServiceUnavailable,
)


logger = logging.getLogger(__name__)


class AIAnalysisService:

    def __init__(self) -> None:
        self.client = OpenAI()

    def analyze_stock(self, request: AnalysisRequest) -> StockInsightResponse:
        logger.info(
            "Stock analysis requested | ticker=%s start=%s end=%s",
            request.ticker,
            request.start_date,
            request.end_date,
        )
        prompt = self._build_prompt(request)

        try:
            raw_data = self._call_llm_mock(prompt)
            logger.debug("Raw AI response received | ticker=%s", request.ticker)
            result = StockInsightResponse.model_validate(raw_data)
            logger.info(
                "Stock analysis completed | ticker=%s trend=%s risk=%s",
                request.ticker,
                result.trend,
                result.risk_level,
            )
            return result
        except ValidationError as e:
            raise AIResponseValidation("AI response schema invalid") from e
        except Exception as e:
            raise RuntimeError("AI service unavailable") from e

    def _build_prompt(self, request: AnalysisRequest) -> str:
        allowed_trends = [t.value for t in TrendSignal]
        allowed_risks = [r.value for r in RiskLevel]
        return (
            f"Analyze the stock {request.ticker} between {request.start_date} "
            f"and {request.end_date}.\n\n"
            "Return the result as valid JSON with the following fields:\n\n"
            f"trend: must be one of {allowed_trends}\n"
            f"risk_level: must be one of {allowed_risks}\n"
            "summary: short explanation of the trend\n"
            "key_signals: list of important signals\n"
            "explanations:write a clear paragraph explaining the analysis for a non-expert investor."
            "disclaimer: financial disclaimer\n"
        )

    def _call_llm(self, prompt: str) -> StockInsightResponse:
        try:
            response = self.client.responses.parse(
                model="gpt-4o-2024-08-06",
                input=prompt,
                text_format=StockInsightResponse,
            )
            event = response.output_parsed
            return event
        except openai.RateLimitError as e:
            raise AIRateLimitError from e
        except openai.APIConnectionError as e:
            raise AIServiceUnavailable from e
        except openai.APIError as e:
            raise AIServiceUnavailable from e

    def _call_llm_mock(self, prompt: str) -> StockInsightResponse:
        return StockInsightResponse(
            trend=TrendSignal.BULLISH,
            risk_level=RiskLevel.MEDIUM,
            summary="AAPL showed a strong upward trend in January 2025 due to positive earnings reports and market optimism.",
            key_signals=[
                "Positive earnings report",
                "Increased demand for Apple products",
                "General market uptrend",
            ],
            explanation=(
                "In January 2025, Apple's stock price experienced a robust uptrend. "
                "This bullish movement was mainly driven by a positive earnings report "
                "that exceeded market expectations, indicating strong financial performance "
                "and increased demand for Apple products such as iPhones and Macs. "
                "The overall market optimism around technology stocks also contributed "
                "to this trend, pushing AAPL higher. However, while the trend is positive, "
                "the market volatility suggests a medium risk level."
            ),
            disclaimer=(
                "This analysis is for informational purposes only and should not be "
                "considered investment advice. Stock investments involve risk."
            ),
        )


# start_date = date(2025, 1, 1)
# end_date = date(2025, 1, 31)

# request = AnalysisRequest(ticker="AAPL", start_date=start_date, end_date=end_date)

# print(request)

# test = AIAnalysisService()
# result = test.analyze_stock(request)
# print(result.model_dump_json(indent=2))
