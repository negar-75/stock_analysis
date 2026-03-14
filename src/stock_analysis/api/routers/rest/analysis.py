from fastapi import APIRouter, Query
from typing import Annotated
from stock_analysis.schemas.analysis import AnalysisRequest, StockInsightResponse
from stock_analysis.services.Analysis.ai_analysis_service import AIAnalysisService


router = APIRouter()


@router.get("/analyze")
def get_LLM_analyze(param: Annotated[AnalysisRequest, Query()]) -> str:
    response = AIAnalysisService().analyze_stock(param)
    return response.explanation
