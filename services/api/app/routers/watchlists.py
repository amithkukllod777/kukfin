from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db import get_db
from app.dependencies import RequestContext, get_request_context
from app.models import WatchlistItem
from app.schemas import WatchlistItemCreate, WatchlistItemResponse


router = APIRouter(prefix="/v1/watchlist", tags=["watchlist"])


@router.get("", response_model=list[WatchlistItemResponse])
def list_watchlist(
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
) -> list[WatchlistItem]:
    return list(
        db.scalars(
            select(WatchlistItem)
            .where(WatchlistItem.workspace_id == context.workspace.id)
            .order_by(WatchlistItem.created_at.desc())
        )
    )


@router.post("", response_model=WatchlistItemResponse, status_code=status.HTTP_201_CREATED)
def add_watchlist_item(
    payload: WatchlistItemCreate,
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
) -> WatchlistItem:
    item = WatchlistItem(
        workspace_id=context.workspace.id,
        symbol=payload.symbol.upper().strip(),
        exchange=payload.exchange.upper().strip(),
        note=payload.note.strip() if payload.note else None,
    )
    db.add(item)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Instrument is already on the watchlist")
    db.refresh(item)
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_watchlist_item(
    item_id: str,
    context: RequestContext = Depends(get_request_context),
    db: Session = Depends(get_db),
) -> Response:
    item = db.scalar(
        select(WatchlistItem).where(
            WatchlistItem.id == item_id,
            WatchlistItem.workspace_id == context.workspace.id,
        )
    )
    if item is None:
        raise HTTPException(status_code=404, detail="Watchlist item not found")
    db.delete(item)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
