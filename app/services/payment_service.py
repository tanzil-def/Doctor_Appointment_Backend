from fastapi import HTTPException

from app.models.payment import Payment
from app.models.enums import PaymentStatus
from app.db.session import async_session
from app.utils.permissions import check_role


async def create_payment(user, appointment_id: int, amount: float, method: str):
    check_role(user, ["USER"])

    async with async_session() as session:
        payment = Payment(
            appointment_id=appointment_id,
            amount=amount,
            method=method,
            status=PaymentStatus.PENDING.value
        )
        session.add(payment)
        await session.commit()
        await session.refresh(payment)
        return payment


async def update_payment_status(user, payment_id: int, status: str):
    check_role(user.role, ["ADMIN"])

    async with async_session() as session:
        stmt = Payment.__table__.select().where(Payment.id == payment_id)
        result = await session.execute(stmt)
        payment = result.scalar_one_or_none()

        if not payment:
            raise HTTPException(status_code=404, detail="Payment not found")

        payment.status = status
        await session.commit()
        await session.refresh(payment)
        return payment
