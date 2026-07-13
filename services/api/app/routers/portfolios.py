from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, selectinload

from app.db import get_db
from app.dependencies import RequestContext, get_request_context
from app.models import Holding, Portfolio
from app.schemas import HoldingCreate, HoldingResponse, PortfolioCreate, PortfolioResponse


router = APIRouter(prefix="/v1/portfolios", tags=["portfolios"])


@router.get("", response_model=list[PortfolioResponse])
def list_portfolios(
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
) -> list[Portfolio]:
    return list(
        db.scalars(
            select(Portfolio)
            .options(selectinload(Portfolio.holdings))
            .where(Portfolio.workspace_id == context.workspace.id)
            .order_by(Portfolio.created_at.desc())
        ).unique()
    )


@router.post("", response_model=PortfolioResponse, status_code=status.HTTP_201_CREATED)
def create_portfolio(
    payload: PortfolioCreate,
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
) -> Portfolio:
    portfolio = Portfolio(
        workspace_id=context.workspace.id,
        name=payload.name.strip(),
        base_currency=payload.base_currency.upper(),
    )
    db.add(portfolio)
    db.commit()
    db.refresh(portfolio)
    return portfolio


@router.post(
    "/{portfolio_id}/holdings",
    response_model=HoldingResponse,
    status_code=status.HTTP_201_CREATED,
)
def add_holding(
    portfolio_id: str,
    payload: HoldingCreate,
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
) -> Holding:
    portfolio = db.scalar(
        select(Portfolio).where(
            Portfolio.id == portfolio_id,
            Portfolio.workspace_id == context.workspace.id,
        )
    )
    if portfolio is None:
        raise HTTPException(status_code=404, detail="Portfolio not found")

    holding = Holding(
        portfolio_id=portfolio.id,
        symbol=payload.symbol.upper().strip(),
        exchange=payload.exchange.upper().strip(),
        quantity=payload.quantity,
        average_price=payload.average_price,
    )
    db.add(holding)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Holding already exists in this portfolio")
    db.refresh(holding)
    return holding
