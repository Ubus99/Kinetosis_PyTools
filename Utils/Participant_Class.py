from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import select
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import Session
from sqlalchemy.orm import mapped_column

from Utils.Base import Base


class Participant(Base):
    __tablename__ = "Participant"

    id: Mapped[int] = mapped_column(primary_key=True)

    Archive_id: Mapped[str] = mapped_column(String)

    MSSQ: Mapped[int] = mapped_column(Integer)

    Method_1: Mapped[int] = mapped_column(Integer)
    SSQ_Pre_1: Mapped[int] = mapped_column(Integer)
    SSQ_Post_1: Mapped[int] = mapped_column(Integer)
    VPQ_1: Mapped[int] = mapped_column(Integer)

    Method_2: Mapped[int] = mapped_column(Integer)
    SSQ_Pre_2: Mapped[int] = mapped_column(Integer)
    SSQ_Post_2: Mapped[int] = mapped_column(Integer)
    VPQ_2: Mapped[int] = mapped_column(Integer)

    @staticmethod
    def load(session: Session, name: str) -> "Participant":
        with session as s:
            Participant.metadata.create_all(session.bind)
            result = s.execute(select(Participant).where(Participant.Archive_id == name))
            return result.scalars().first()
