from datetime import datetime, timezone
from typing import List, Tuple


def invest_donations_into_projects(
    target,
    sources: List,
) -> Tuple[List, List]:
    """
    Функция распределяет инвестиции между целевым объектом и источниками.
    """
    now = datetime.now(timezone.utc)

    target_left = target.full_amount - target.invested_amount

    updated_sources = []

    for source in sources:
        if target_left <= 0:
            break

        source_left = source.full_amount - source.invested_amount

        if source_left <= 0:
            continue

        invest_amount = min(target_left, source_left)

        target.invested_amount += invest_amount
        source.invested_amount += invest_amount

        target_left -= invest_amount

        if target.invested_amount == target.full_amount:
            target.fully_invested = True
            target.close_date = now

        if source.invested_amount == source.full_amount:
            source.fully_invested = True
            source.close_date = now

        updated_sources.append(source)

    return target, updated_sources
