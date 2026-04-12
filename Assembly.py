from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped, relationship
from Part import Part
from typing import List


class Assembly(Part):
    """A part that we build ourselves from component parts.  An assembly
    can contain other assemblies as well as piece parts.  This is one of
    the two subclasses in the Part joined table inheritance hierarchy."""
    __tablename__ = "assemblies"
    partsNumber: Mapped[str] = mapped_column("parts_number", String(10),
                                             ForeignKey("parts.number",
                                                        ondelete="CASCADE"),
                                             primary_key=True)
    """We need to be able to delete the association class rows without using session.delete.
    The way that we will DISassociate a component Part from an Assembly is to delete an
    instance of this list of Usages that connects this Assembly to the component Part that
    we want to disassociate.  But to get that to work in the database, we need to configure
    the relationship such that breaking the association at this end propagates a
    deletion in the association table to go along with it."""
    components: Mapped[List["Usage"]] = relationship(back_populates="assembly",
                                                     cascade="all, save-update, delete-orphan",
                                                     foreign_keys="Usage.assembliesPartsNumber")
    __mapper_args__ = {"polymorphic_identity": "assembly"}

    def __init__(self, number: str, name: str):
        super().__init__(number, name)
        self.partsNumber = number

    def add_component(self, component_part, quantity: int):
        """Add a component part to this assembly with a given quantity.
        We are not actually adding a Part directly to the assembly.  Rather,
        we are adding an instance of Usage to the assembly.
        :param  component_part: The Part that is a component of this assembly.
        :param  quantity:       How many of this component part are needed.
        :return:                None
        """
        from Usage import Usage
        # Make sure that this assembly does not already have this component.
        for comp in self.components:
            if comp.partsNumber == component_part.number:
                return  # This assembly already has this component
        # Create the new instance of Usage to connect this Assembly to the supplied Part.
        usage = Usage(self, component_part, quantity)

    def remove_component(self, component_part):
        """Remove a component part from this assembly.
        :param component_part:  The Part to be removed from this assembly.
        :return:                None
        """
        for comp in self.components:
            if comp.partsNumber == component_part.number:
                self.components.remove(comp)
                return

    def __str__(self):
        return f"Assembly: {self.partsNumber} - {self.name}"
