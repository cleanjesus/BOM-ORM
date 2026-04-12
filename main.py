import logging
from menu_definitions import menu_main, add_menu, delete_menu, list_menu, update_menu, report_menu, debug_select
from db_connection import engine, Session
from orm_base import metadata
# Note that until you import your SQLAlchemy declarative classes, such as Part, Python
# will not execute that code, and SQLAlchemy will be unaware of the mapped table.
from Vendor import Vendor
from Part import Part
from Assembly import Assembly
from PiecePart import PiecePart
from Usage import Usage
from Option import Option
from Menu import Menu
from pprint import pprint
from SQLAlchemyUtilities import check_unique


def add(sess: Session):
    add_action: str = ''
    while add_action != add_menu.last_action():
        add_action = add_menu.menu_prompt()
        exec(add_action)


def delete(sess: Session):
    delete_action: str = ''
    while delete_action != delete_menu.last_action():
        delete_action = delete_menu.menu_prompt()
        exec(delete_action)


def list_objects(sess: Session):
    list_action: str = ''
    while list_action != list_menu.last_action():
        list_action = list_menu.menu_prompt()
        exec(list_action)


def update(sess: Session):
    update_action: str = ''
    while update_action != update_menu.last_action():
        update_action = update_menu.menu_prompt()
        exec(update_action)


def reports(sess: Session):
    report_action: str = ''
    while report_action != report_menu.last_action():
        report_action = report_menu.menu_prompt()
        exec(report_action)


# -------------------- ADD FUNCTIONS --------------------

def add_vendor(sess: Session):
    """
    Prompt the user for the information for a new vendor and validate
    the input to make sure that we do not create any duplicates.
    :param sess: The connection to the database.
    :return:     None
    """
    violation = True
    while violation:
        name = input("Vendor name--> ")
        new_vendor = Vendor(name)
        violated_constraints = check_unique(Session, new_vendor)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    sess.add(new_vendor)


def add_assembly(sess: Session):
    """
    Prompt the user for the information for a new assembly and validate
    the input to make sure that we do not create any duplicates.
    :param sess: The connection to the database.
    :return:     None
    """
    violation = True
    while violation:
        number = input("Part number--> ")
        name = input("Part name--> ")
        new_assembly = Assembly(number, name)
        violated_constraints = check_unique(Session, new_assembly)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    sess.add(new_assembly)


def add_piece_part(sess: Session):
    """
    Prompt the user for the information for a new piece part and validate
    the input to make sure that we do not create any duplicates.
    :param sess: The connection to the database.
    :return:     None
    """
    print("Which vendor supplies this piece part?")
    vendor: Vendor = select_vendor(sess)
    violation = True
    while violation:
        number = input("Part number--> ")
        name = input("Part name--> ")
        new_piece_part = PiecePart(number, name, vendor)
        violated_constraints = check_unique(Session, new_piece_part)
        if len(violated_constraints) > 0:
            print('The following uniqueness constraints were violated:')
            pprint(violated_constraints)
            print('Please try again.')
        else:
            violation = False
    sess.add(new_piece_part)


def add_component(sess: Session):
    """
    Add a component part to an assembly with a given quantity.
    :param sess: The connection to the database.
    :return:     None
    """
    print("Select the assembly that will contain the component:")
    assembly: Assembly = select_assembly(sess)
    print("Select the component part to add to the assembly:")
    component: Part = select_part(sess)
    # Make sure this component is not already in this assembly.
    unique_usage: bool = False
    while not unique_usage:
        usage_count: int = sess.query(Usage).filter(
            Usage.assembliesPartsNumber == assembly.partsNumber,
            Usage.partsNumber == component.number).count()
        unique_usage = usage_count == 0
        if not unique_usage:
            print("That component is already in that assembly.  Try again.")
            print("Select the component part to add to the assembly:")
            component = select_part(sess)
    quantity = int(input("Quantity--> "))
    assembly.add_component(component, quantity)
    sess.add(assembly)
    sess.flush()


# -------------------- SELECT FUNCTIONS --------------------

def select_vendor(sess: Session) -> Vendor:
    """
    Prompt the user for a specific vendor by name.
    :param sess: The connection to the database.
    :return:     The selected vendor.
    """
    found: bool = False
    name: str = ''
    while not found:
        name = input("Vendor name--> ")
        name_count: int = sess.query(Vendor). \
            filter(Vendor.name == name).count()
        found = name_count == 1
        if not found:
            print("No vendor found by that name.  Try again.")
    return_vendor: Vendor = sess.query(Vendor). \
        filter(Vendor.name == name).first()
    return return_vendor


def select_part(sess: Session) -> Part:
    """
    Prompt the user for a specific part by part number.
    :param sess: The connection to the database.
    :return:     The selected part.
    """
    found: bool = False
    number: str = ''
    while not found:
        number = input("Part number--> ")
        number_count: int = sess.query(Part). \
            filter(Part.number == number).count()
        found = number_count == 1
        if not found:
            print("No part found with that number.  Try again.")
    return_part: Part = sess.query(Part). \
        filter(Part.number == number).first()
    return return_part


def select_assembly(sess: Session) -> Assembly:
    """
    Prompt the user for a specific assembly by part number.
    :param sess: The connection to the database.
    :return:     The selected assembly.
    """
    found: bool = False
    number: str = ''
    while not found:
        number = input("Assembly part number--> ")
        number_count: int = sess.query(Assembly). \
            filter(Assembly.partsNumber == number).count()
        found = number_count == 1
        if not found:
            print("No assembly found with that number.  Try again.")
    return_assembly: Assembly = sess.query(Assembly). \
        filter(Assembly.partsNumber == number).first()
    return return_assembly


# -------------------- DELETE FUNCTIONS --------------------

def delete_vendor(sess: Session):
    """
    Prompt the user for a vendor to delete.  Check for children first.
    :param sess: The connection to the database.
    :return:     None
    """
    vendor = select_vendor(sess)
    n_piece_parts = sess.query(PiecePart).filter(PiecePart.vendorsName == vendor.name).count()
    if n_piece_parts > 0:
        print(f"Sorry, there are {n_piece_parts} piece parts from that vendor.  Delete them first, "
              "then come back here to delete the vendor.")
    else:
        sess.delete(vendor)


def delete_part(sess: Session):
    """
    Prompt the user for a part to delete.  Check for usages first.
    :param sess: The connection to the database.
    :return:     None
    """
    part = select_part(sess)
    # Check if this part is used as a component in any assembly.
    n_used_in = sess.query(Usage).filter(Usage.partsNumber == part.number).count()
    if n_used_in > 0:
        print(f"Sorry, that part is used as a component in {n_used_in} assembly(ies).  "
              "Remove those usages first, then come back here to delete the part.")
        return
    # If it's an assembly, check if it has any components.
    if part.type == 'assembly':
        n_components = sess.query(Usage).filter(Usage.assembliesPartsNumber == part.number).count()
        if n_components > 0:
            print(f"Sorry, that assembly has {n_components} component(s).  "
                  "Remove those components first, then come back here to delete the assembly.")
            return
    sess.delete(part)


def delete_component(sess: Session):
    """
    Remove a component part from an assembly.
    :param sess: The current database session.
    :return:     None
    """
    print("Select the assembly to remove a component from:")
    assembly: Assembly = select_assembly(sess)
    print("Select the component part to remove:")
    component: Part = select_part(sess)
    assembly.remove_component(component)


# -------------------- UPDATE FUNCTIONS --------------------

def update_part(sess: Session):
    """
    Update the name of a part.
    :param sess: The connection to the database.
    :return:     None
    """
    part = select_part(sess)
    old_name = part.name
    new_name = input(f"Current name: '{old_name}'. New name--> ")
    # Check that the new name is not already taken.
    name_count: int = sess.query(Part).filter(Part.name == new_name).count()
    if name_count > 0:
        print("A part with that name already exists.  Update cancelled.")
    else:
        part.name = new_name
        print(f"Part name updated from '{old_name}' to '{new_name}'.")


def update_composition(sess: Session):
    """
    Update the quantity of a component part in an assembly.
    :param sess: The connection to the database.
    :return:     None
    """
    print("Select the assembly:")
    assembly: Assembly = select_assembly(sess)
    print("Select the component part:")
    component: Part = select_part(sess)
    usage: Usage = sess.query(Usage).filter(
        Usage.assembliesPartsNumber == assembly.partsNumber,
        Usage.partsNumber == component.number).first()
    if usage is None:
        print("That component is not in that assembly.")
    else:
        old_qty = usage.quantity
        new_qty = int(input(f"Current quantity: {old_qty}. New quantity--> "))
        if new_qty < 1 or new_qty > 20:
            print("Quantity must be between 1 and 20.  Update cancelled.")
        else:
            usage.quantity = new_qty
            print(f"Quantity updated from {old_qty} to {new_qty}.")


# -------------------- LIST FUNCTIONS --------------------

def list_parts(sess: Session):
    """
    List all parts currently in the database.
    :param sess: The current connection to the database.
    :return:     None
    """
    parts: [Part] = list(sess.query(Part).order_by(Part.number))
    for part in parts:
        print(part)


def list_vendors(sess: Session):
    """
    List all vendors currently in the database.
    :param sess: The current connection to the database.
    :return:     None
    """
    vendors: [Vendor] = list(sess.query(Vendor).order_by(Vendor.name))
    for vendor in vendors:
        print(vendor)


def list_compositions(sess: Session):
    """
    List all usages (compositions) currently in the database.
    :param sess: The current connection to the database.
    :return:     None
    """
    usages: [Usage] = list(sess.query(Usage).order_by(Usage.assembliesPartsNumber,
                                                       Usage.partsNumber))
    for usage in usages:
        print(usage)


def report_vendor(sess: Session):
    """
    Report out the data in a selected vendor row.
    :param sess: The connection to the database.
    :return:     None
    """
    vendor = select_vendor(sess)
    print(f"Vendor Name: {vendor.name}")
    print(f"Piece parts supplied: {len(vendor.pieceParts)}")
    for pp in vendor.pieceParts:
        print(f"  {pp.partsNumber} - {pp.name}")


def report_part(sess: Session):
    """
    Report out the data in a selected part row.
    :param sess: The connection to the database.
    :return:     None
    """
    part = select_part(sess)
    print(f"Part Number: {part.number}")
    print(f"Part Name: {part.name}")
    print(f"Type: {part.type}")
    if part.type == 'piece_part':
        print(f"Vendor: {part.vendorsName}")
    elif part.type == 'assembly':
        usages = sess.query(Usage).filter(
            Usage.assembliesPartsNumber == part.number).all()
        print(f"Components: {len(usages)}")
        for usage in usages:
            print(f"  {usage.partsNumber} - {usage.component.name} (qty: {usage.quantity})")


def report_composition(sess: Session):
    """
    Report out the data in a selected usage/composition row.
    :param sess: The connection to the database.
    :return:     None
    """
    print("Select the assembly:")
    assembly = select_assembly(sess)
    print("Select the component:")
    component = select_part(sess)
    usage = sess.query(Usage).filter(
        Usage.assembliesPartsNumber == assembly.partsNumber,
        Usage.partsNumber == component.number).first()
    if usage is None:
        print("No such composition found.")
    else:
        print(f"Assembly: {usage.assembliesPartsNumber} - {usage.assembly.name}")
        print(f"Component: {usage.partsNumber} - {usage.component.name}")
        print(f"Quantity: {usage.quantity}")


# -------------------- REPORT FUNCTIONS --------------------

def hierarchy_report(sess: Session):
    """
    Starting at any point in the part composition hierarchy, report out the
    breakdown in hierarchical format with indentation.
    :param sess: The connection to the database.
    :return:     None
    """
    print("Select the starting part for the hierarchy report:")
    part = select_part(sess)
    print_hierarchy(sess, part, 0)


def print_hierarchy(sess: Session, part: Part, depth: int):
    """
    Recursively print the part composition hierarchy.
    :param sess:    The connection to the database.
    :param part:    The current part in the hierarchy.
    :param depth:   The current depth for indentation (tabs).
    :return:        None
    """
    print(f"{'	' * depth}{part.number} - {part.name}")
    # If this part is an assembly, find its components and recurse.
    if part.type == 'assembly':
        usages = sess.query(Usage).filter(
            Usage.assembliesPartsNumber == part.number
        ).order_by(Usage.partsNumber).all()
        for usage in usages:
            print_hierarchy(sess, usage.component, depth + 1)


def max_components_report(sess: Session):
    """
    List each assembly part number, part name, and number of component parts,
    but only for those assemblies that have the greatest number of component parts.
    :param sess: The connection to the database.
    :return:     None
    """
    from sqlalchemy import func
    # Count components for each assembly.
    component_counts = sess.query(
        Usage.assembliesPartsNumber,
        func.count(Usage.partsNumber).label('component_count')
    ).group_by(Usage.assembliesPartsNumber).all()

    if len(component_counts) == 0:
        print("No assemblies with components found.")
        return

    # Find the maximum count.
    max_count = max(row.component_count for row in component_counts)
    print(f"\nAssemblies with the most component parts ({max_count} components):")
    print("-" * 60)

    # List all assemblies that have the max count.
    for row in component_counts:
        if row.component_count == max_count:
            assembly = sess.query(Assembly).filter(
                Assembly.partsNumber == row.assembliesPartsNumber).first()
            print(f"  {assembly.partsNumber} - {assembly.name}: "
                  f"{row.component_count} component(s)")


# -------------------- BOILERPLATE DATA --------------------

def boilerplate(sess: Session):
    """
    Add boilerplate data initially to jump start the testing.  Remember that there is no
    checking of this data, so only run this option once from the console, or you will
    get a uniqueness constraint violation from the database.
    :param sess: The session that's open.
    :return:     None
    """
    # ---- Vendors ----
    helical = Vendor('Helical International')
    plates = Vendor('Plates R Us')
    wholey = Vendor('Wholey Rollers')
    jack = Vendor('Jack Daniels Belts')
    engine_acc = Vendor('Engine Accessories')
    comp_usa = Vendor('Comp USA')
    unharnessed = Vendor('Unharnessed at Large')
    get_grip = Vendor('Get a Grip')
    telegraph = Vendor('Telegraph Inc.')
    radio = Vendor('Radio Shack')
    starbucks = Vendor('Starbucks')
    michaels = Vendor('Michaels')
    osh = Vendor('OSH')
    sess.add_all([helical, plates, wholey, jack, engine_acc, comp_usa,
                  unharnessed, get_grip, telegraph, radio, starbucks, michaels, osh])
    sess.flush()

    # ---- Assemblies (parts we build ourselves) ----
    motorcycle = Assembly('0', 'Motorcycle')
    engine = Assembly('1', 'Engine')
    transmission = Assembly('1.1', 'Transmission')
    clutch = Assembly('1.1.1', 'Clutch')
    variator = Assembly('1.1.2', 'Variator')
    head = Assembly('1.2', 'Head')
    battery = Assembly('1.3', 'Battery')
    starter = Assembly('1.3.2', 'Starter')
    stator = Assembly('1.3.2.1', 'Stator')
    frame = Assembly('2', 'Frame')
    handlebars = Assembly('2.1', 'Handlebars')
    throttle = Assembly('2.1.2', 'Throttle')
    seat = Assembly('2.2', 'Seat')
    headlight = Assembly('2.3', 'Headlight')
    sess.add_all([motorcycle, engine, transmission, clutch, variator, head,
                  battery, starter, stator, frame, handlebars, throttle, seat, headlight])
    sess.flush()

    # ---- Piece Parts (parts we purchase from vendors) ----
    springs = PiecePart('1.1.1.1', 'Springs', helical)
    torque = PiecePart('1.1.1.2', 'Torque', plates)
    rollers = PiecePart('1.1.2.1', 'Rollers', wholey)
    belt = PiecePart('1.1.3', 'Belt', jack)
    pistons = PiecePart('1.2.1', 'Pistons', engine_acc)
    rings = PiecePart('1.2.2', 'Rings', engine_acc)
    ecu = PiecePart('1.3.1', 'ECU', comp_usa)
    stator_wiring = PiecePart('1.3.2.1.1', 'Stator Wiring', unharnessed)
    grips = PiecePart('2.1.1', 'Grips', get_grip)
    throttle_cables = PiecePart('2.1.2.1', 'Throttle Cables', telegraph)
    kill_switch = PiecePart('2.1.3', 'Kill Switch', radio)
    foam = PiecePart('2.2.1', 'Foam', starbucks)
    fabric = PiecePart('2.2.2', 'Fabric', michaels)
    bulb = PiecePart('2.3.1', 'Bulb', osh)
    headlight_wiring = PiecePart('2.3.2', 'Headlight Wiring', unharnessed)
    sess.add_all([springs, torque, rollers, belt, pistons, rings, ecu,
                  stator_wiring, grips, throttle_cables, kill_switch,
                  foam, fabric, bulb, headlight_wiring])
    sess.flush()

    # ---- Usages (composition: assembly -> component with quantity) ----
    # Motorcycle components
    sess.add(Usage(motorcycle, engine, 1))
    sess.add(Usage(motorcycle, frame, 1))
    # Engine components
    sess.add(Usage(engine, transmission, 1))
    sess.add(Usage(engine, head, 2))      # 2 heads
    sess.add(Usage(engine, battery, 1))
    # Transmission components
    sess.add(Usage(transmission, clutch, 1))
    sess.add(Usage(transmission, variator, 1))
    sess.add(Usage(transmission, belt, 1))
    # Clutch components
    sess.add(Usage(clutch, springs, 4))   # 4 springs
    sess.add(Usage(clutch, torque, 1))
    # Variator components
    sess.add(Usage(variator, rollers, 5))  # 5 rollers
    # Head components
    sess.add(Usage(head, pistons, 2))     # 2 pistons
    sess.add(Usage(head, rings, 2))       # 2 rings
    # Battery components
    sess.add(Usage(battery, ecu, 1))
    sess.add(Usage(battery, starter, 1))
    # Starter components
    sess.add(Usage(starter, stator, 1))
    # Stator components
    sess.add(Usage(stator, stator_wiring, 1))
    # Frame components
    sess.add(Usage(frame, handlebars, 1))
    sess.add(Usage(frame, seat, 1))
    sess.add(Usage(frame, headlight, 1))
    # Handlebars components
    sess.add(Usage(handlebars, grips, 2))  # 2 grips
    sess.add(Usage(handlebars, throttle, 1))
    sess.add(Usage(handlebars, kill_switch, 1))
    # Throttle components
    sess.add(Usage(throttle, throttle_cables, 1))
    # Seat components
    sess.add(Usage(seat, foam, 1))
    sess.add(Usage(seat, fabric, 1))
    # Headlight components
    sess.add(Usage(headlight, bulb, 1))
    sess.add(Usage(headlight, headlight_wiring, 1))
    sess.flush()
    print("Boilerplate data loaded successfully.")


def session_rollback(sess):
    """
    Give the user a chance to roll back to the most recent commit point.
    :param sess: The connection to the database.
    :return:     None
    """
    confirm_menu = Menu('main', 'Please select one of the following options:', [
        Option("Yes, I really want to roll back this session", "sess.rollback()"),
        Option("No, I hit this option by mistake", "pass")
    ])
    exec(confirm_menu.menu_prompt())


if __name__ == '__main__':
    print('Starting off')
    logging.basicConfig()
    # use the logging factory to create our first logger.
    # for more logging messages, set the level to logging.DEBUG.
    # logging_action will be the text string name of the logging level, for instance 'logging.INFO'
    logging_action = debug_select.menu_prompt()
    # eval will return the integer value of whichever logging level variable name the user selected.
    logging.getLogger("sqlalchemy.engine").setLevel(eval(logging_action))
    # use the logging factory to create our second logger.
    # for more logging messages, set the level to logging.DEBUG.
    logging.getLogger("sqlalchemy.pool").setLevel(eval(logging_action))

    metadata.drop_all(bind=engine)  # start with a clean slate while in development

    # Create whatever tables are called for by our "Entity" classes.
    metadata.create_all(bind=engine)

    with Session() as sess:
        main_action: str = ''
        while main_action != menu_main.last_action():
            main_action = menu_main.menu_prompt()
            print('next action: ', main_action)
            exec(main_action)
        sess.commit()
    print('Ending normally')
