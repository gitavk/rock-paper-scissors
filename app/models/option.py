from sqlalchemy import Column, ForeignKey, Integer, String, Table, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


beats = Table(
    "beats",
    Base.metadata,
    Column("option_id", Integer, ForeignKey("options.id"), index=True),
    Column("beat_id", Integer, ForeignKey("options.id")),
    UniqueConstraint("option_id", "beat_id", name="unique_beats"),
)


class Option(Base):
    __tablename__ = "options"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    beats = relationship(
        "Option",
        secondary=beats,
        primaryjoin=id == beats.c.option_id,
        secondaryjoin=id == beats.c.beat_id,
    )
