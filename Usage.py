from orm_base import Base
from sqlalchemy import Integer, ForeignKey, CheckConstraint, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

# We canNOT import Assembly and Part here because Assembly and Part
# are both importing Usage.  So we have to go without the
# ability to validate the Assembly or Part class references in
# this class.  Otherwise, we get a circular import.
# from Assembly import Assembly
# from Part import Part


class Usage(Base):
    """The association class between Assembly and Part.  I resorted to using
    this style of implementing a Many to Many because I feel that it is the
    most versatile approach.  Each usage instance represents a usage of a
    component part within an assembly, along with the quantity needed."""
    __tablename__ = "usages"
    assembly: Mapped["Assembly"] = relationship(back_populates="components",
                                                foreign_keys="Usage.assembliesPartsNumber")
    assembliesPartsNumber: Mapped[str] = mapped_column("assemblies_parts_number", String(10),
                                                        ForeignKey("assemblies.parts_number"),
                                                        primary_key=True)
    component: Mapped["Part"] = relationship(back_populates="usedIn",
                                             foreign_keys="Usage.partsNumber")
    partsNumber: Mapped[str] = mapped_column("parts_number", String(10),
                                             ForeignKey("parts.number"),
                                             primary_key=True)
    quantity: Mapped[int] = mapped_column("quantity", Integer,
                                          CheckConstraint("quantity BETWEEN 1 AND 20",
                                                          name="usages_quantity_length"),
                                          nullable=False)

    def __init__(self, assembly, component, quantity: int):
        self.assembly = assembly
        self.assembliesPartsNumber = assembly.partsNumber
        self.component = component
        self.partsNumber = component.number
        self.quantity = quantity

    def __str__(self):
        return f"Usage- assembly: {self.assembliesPartsNumber} component: {self.partsNumber} qty: {self.quantity}"
