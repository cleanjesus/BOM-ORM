from orm_base import Base
from sqlalchemy import String, CheckConstraint, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Part(Base):
    """A generic part.  Each part is categorized as either an Assembly
    (which we build from component parts) or a PiecePart (which we
    purchase from an outside vendor).  The two categories are mutually
    exclusive.  This is the superclass in a joined table inheritance
    hierarchy."""
    __tablename__ = "parts"
    number: Mapped[str] = mapped_column("number", String(10),
                                        CheckConstraint("LENGTH(number) >= 1",
                                                        name="parts_number_length"),
                                        nullable=False, primary_key=True)
    name: Mapped[str] = mapped_column("name", String(80),
                                      CheckConstraint("LENGTH(name) >= 3",
                                                      name="parts_name_length"),
                                      nullable=False)
    # Discriminator column for the joined table inheritance to distinguish
    # between Assembly and PiecePart rows.
    type: Mapped[str] = mapped_column("type", String(50), nullable=False)
    # A list of Usage instances where this part is used as a component
    # in some assembly.
    usedIn: Mapped[List["Usage"]] = relationship(back_populates="component",
                                                  foreign_keys="Usage.partsNumber")
    # __table_args__ can best be viewed as directives that we ask SQLAlchemy to
    # send to the database.  In this case, that we want a uniqueness constraint
    # on the part name.
    __table_args__ = (UniqueConstraint("name", name="parts_uk_01"),)
    __mapper_args__ = {"polymorphic_identity": "part",
                       "polymorphic_on": "type"}

    def __init__(self, number: str, name: str):
        self.number = number
        self.name = name

    def __str__(self):
        return f"Part: {self.number} - {self.name} ({self.type})"
