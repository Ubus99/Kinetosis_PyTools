import pandas
from sqlalchemy import Float
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from Utils.Base import Base


class SSQ(Base):
    __tablename__ = "SSQ"

    id: Mapped[int] = mapped_column(primary_key=True)

    n: Mapped[float] = mapped_column(Float, nullable=False)
    o: Mapped[float] = mapped_column(Float, nullable=False)
    d: Mapped[float] = mapped_column(Float, nullable=False)
    ts: Mapped[float] = mapped_column(Float, nullable=False)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, n={self.n!r}, o={self.o!r}, p={self.p!r}, ts={self.ts!r})"

    def Series(self):
        return pandas.Series(
            {
                "n": self.n,
                "o": self.o,
                "d": self.d,
                "ts": self.ts
            }
        )
