from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from Part import Part


class PiecePart(Part):
    """A part that we purchase from an outside vendor rather than
    building ourselves.  Piece parts do not have any component parts.
    This is one of the two subclasses in the Part joined table
    inheritance hierarchy."""
    __tablename__ = "piece_parts"
    partsNumber: Mapped[str] = mapped_column("parts_number", String(10),
                                             ForeignKey("parts.number",
                                                        ondelete="CASCADE"),
                                             primary_key=True)
    vendorsName: Mapped[str] = mapped_column("vendors_name", String(80),
                                             ForeignKey("vendors.name"),
                                             nullable=False)
    # Reference from child to parent.
    vendor: Mapped["Vendor"] = relationship(back_populates="pieceParts")
    __mapper_args__ = {"polymorphic_identity": "piece_part"}

    def __init__(self, number: str, name: str, vendor):
        super().__init__(number, name)
        self.partsNumber = number
        self.vendor = vendor
        self.vendorsName = vendor.name

    def __str__(self):
        return f"PiecePart: {self.partsNumber} - {self.name} (vendor: {self.vendorsName})"
