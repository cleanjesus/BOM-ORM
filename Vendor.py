from orm_base import Base
from sqlalchemy import String, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List


class Vendor(Base):
    """A supplier of piece parts.  Vendors supply parts that we purchase
    from the outside rather than assembling ourselves."""
    __tablename__ = "vendors"
    name: Mapped[str] = mapped_column("name", String(80),
                                      CheckConstraint("LENGTH(name) >= 3",
                                                      name="vendors_name_length"),
                                      nullable=False, primary_key=True)
    # The list of piece parts supplied by this vendor.
    pieceParts: Mapped[List["PiecePart"]] = relationship(back_populates="vendor")

    def __init__(self, name: str):
        self.name = name

    def __str__(self):
        return f"Vendor: {self.name}"
