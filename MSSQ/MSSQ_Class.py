from sqlalchemy import Boolean
from sqlalchemy import Float
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from Utils.Base import Base


class MSSQ(Base):
    __tablename__ = "MSSQ"

    id: Mapped[int] = mapped_column(primary_key=True)

    valid: Mapped[bool] = mapped_column(Boolean, nullable=False)
    mssq: Mapped[float] = mapped_column(Float, nullable=False)
    pct: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, valid={self.valid!r}, mssq={self.mssq!r}, pct={self.pct!r})"
