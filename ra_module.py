# ra_module.py

import cx_Oracle
from rich.console import Console
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich import box
from rich.panel import Panel

# Initialize Rich Console
console = Console()


def execute_query(connection, query, params=None):
    """
    Executes a SQL query and displays the results in a formatted table.
    """
    try:
        cursor = connection.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        columns = [desc[0] for desc in cursor.description]
        table = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL_DOUBLE_HEAD)
        for col in columns:
            table.add_column(str(col))
        for row in cursor:
            table.add_row(*[str(item) if item is not None else "NULL" for item in row])
        console.print(table)
        cursor.close()
    except cx_Oracle.DatabaseError as e:
        error, = e.args
        console.print(f"[red]An error occurred: {error.message}[/red]")


def selection(connection):
    """
    Implements the Selection (σ) operation.
    Allows the user to select records from a table based on a condition.
    """
    console.print("[bold underline]Selection Operation[/bold underline]")
    # Get list of user tables
    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM user_tables")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()

    if not tables:
        console.print("[red]No tables found in the database.[/red]")
        return

    # Display tables and prompt user to select one
    table_menu = Panel(
        "\n".join([f"{i+1}. {tables[i]}" for i in range(len(tables))]),
        title="Select a Table",
        subtitle="Enter the number of the table",
        style="bold cyan",
        box=box.DOUBLE_EDGE
    )
    console.print(table_menu)
    try:
        choice = IntPrompt.ask("Your choice", choices=[str(i+1) for i in range(len(tables))])
        table_name = tables[int(choice)-1]
    except Exception:
        console.print("[red]Invalid input. Please enter a valid number.[/red]")
        return

    # Prompt for condition
    condition = Prompt.ask("Enter selection condition (e.g., 'Age > 30')")

    # Build and execute query
    query = f"SELECT * FROM {table_name} WHERE {condition}"
    execute_query(connection, query)


def projection(connection):
    """
    Implements the Projection (π) operation.
    Allows the user to select specific columns from a table.
    """
    console.print("[bold underline]Projection Operation[/bold underline]")
    # Get list of user tables
    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM user_tables")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()

    if not tables:
        console.print("[red]No tables found in the database.[/red]")
        return

    # Display tables and prompt user to select one
    table_menu = Panel(
        "\n".join([f"{i+1}. {tables[i]}" for i in range(len(tables))]),
        title="Select a Table",
        subtitle="Enter the number of the table",
        style="bold cyan",
        box=box.DOUBLE_EDGE
    )
    console.print(table_menu)
    try:
        choice = IntPrompt.ask("Your choice", choices=[str(i+1) for i in range(len(tables))])
        table_name = tables[int(choice)-1]
    except Exception:
        console.print("[red]Invalid input. Please enter a valid number.[/red]")
        return

    # Get columns of the selected table
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table_name} WHERE ROWNUM = 1")
    columns = [desc[0] for desc in cursor.description]
    cursor.close()

    # Prompt for columns to project
    console.print("Available columns:")
    for col in columns:
        console.print(f"- {col}")
    columns_to_project = Prompt.ask("Enter columns to project, separated by commas")

    # Build and execute query
    query = f"SELECT {columns_to_project} FROM {table_name}"
    execute_query(connection, query)


def union(connection):
    """
    Implements the Union operation.
    Combines rows from two tables with the same schema.
    Supports union on the same table with row range selection or on different tables with common columns.
    """
    console.print("[bold underline]Union Operation[/bold underline]")
    # Get list of user tables
    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM user_tables")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()

    if not tables:
        console.print("[red]No tables found in the database.[/red]")
        return

    # Display Union Options Menu
    union_options_menu = Panel(
        "\n".join([
            "1. Union on the Same Table with Row Range Selection",
            "2. Union on Different Tables with Common Columns",
            "3. Back to RA Operations Menu"
        ]),
        title="Union Operation Options",
        subtitle="Choose an option [1-3]",
        style="bold cyan",
        box=box.DOUBLE_EDGE
    )
    console.print(union_options_menu)
    try:
        choice = IntPrompt.ask("Your choice", choices=['1', '2', '3'])
    except Exception:
        console.print("[red]Invalid input. Please enter a valid number.[/red]")
        return

    if choice == 1:
        # Union on the Same Table with Row Range Selection
        console.print("[bold cyan]Union on the Same Table with Row Range Selection[/bold cyan]")
        # Display tables and prompt user to select one
        table_menu = Panel(
            "\n".join([f"{i+1}. {tables[i]}" for i in range(len(tables))]),
            title="Select a Table",
            subtitle="Enter the number of the table",
            style="bold cyan",
            box=box.DOUBLE_EDGE
        )
        console.print(table_menu)
        try:
            table_choice = IntPrompt.ask("Your choice", choices=[str(i+1) for i in range(len(tables))])
            table_name = tables[int(table_choice)-1]
        except Exception:
            console.print("[red]Invalid input. Please enter a valid number.[/red]")
            return

        # Prompt for row ranges
        console.print(f"Selected Table: {table_name}")
        try:
            range1 = Prompt.ask("Enter first row range (e.g., 1-7)")
            range2 = Prompt.ask("Enter second row range (e.g., 5-12)")
            start1, end1 = map(int, range1.split('-'))
            start2, end2 = map(int, range2.split('-'))
        except Exception:
            console.print("[red]Invalid row range format. Please enter in 'start-end' format (e.g., 1-7).[red]")
            return

        # Create Temporary Tables
        temp_table1 = f"temp_union_{table_name}_1"
        temp_table2 = f"temp_union_{table_name}_2"

        # Drop temp tables if they already exist in a single PL/SQL block
        drop_temp_tables_query = f"""
            BEGIN
                EXECUTE IMMEDIATE 'DROP TABLE {temp_table1}';
                EXECUTE IMMEDIATE 'DROP TABLE {temp_table2}';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -942 THEN
                        RAISE;
                    END IF;
            END;
        """
        try:
            cursor = connection.cursor()
            cursor.execute(drop_temp_tables_query)
            connection.commit()
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            console.print(f"[red]Error dropping temporary tables: {error.message}[/red]")
            cursor.close()
            return
        cursor.close()

        # Create Temp Table 1
        create_temp1_query = f"""
            CREATE TABLE {temp_table1} AS
            SELECT * FROM (
                SELECT a.*, ROW_NUMBER() OVER (ORDER BY ROWID) as rn
                FROM {table_name} a
            )
            WHERE rn BETWEEN {start1} AND {end1}
        """
        # Create Temp Table 2
        create_temp2_query = f"""
            CREATE TABLE {temp_table2} AS
            SELECT * FROM (
                SELECT a.*, ROW_NUMBER() OVER (ORDER BY ROWID) as rn
                FROM {table_name} a
            )
            WHERE rn BETWEEN {start2} AND {end2}
        """

        try:
            cursor = connection.cursor()
            cursor.execute(create_temp1_query)
            cursor.execute(create_temp2_query)
            connection.commit()
            console.print(f"[green]Temporary tables '{temp_table1}' and '{temp_table2}' created successfully.[/green]")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            console.print(f"[red]Error creating temporary tables: {error.message}[/red]")
            cursor.close()
            return
        cursor.close()

        # Perform Union
        union_query = f"SELECT * FROM {temp_table1} UNION SELECT * FROM {temp_table2}"
        console.print(f"[bold cyan]Executing Union on Temporary Tables: {temp_table1} ∪ {temp_table2}[/bold cyan]")
        execute_query(connection, union_query)

        # Optionally, drop temp tables after operation in a single PL/SQL block
        cleanup_temp_query = f"""
            BEGIN
                EXECUTE IMMEDIATE 'DROP TABLE {temp_table1}';
                EXECUTE IMMEDIATE 'DROP TABLE {temp_table2}';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -942 THEN
                        RAISE;
                    END IF;
            END;
        """
        try:
            cursor = connection.cursor()
            cursor.execute(cleanup_temp_query)
            connection.commit()
            console.print(f"[green]Temporary tables '{temp_table1}' and '{temp_table2}' dropped successfully.[/green]")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            console.print(f"[red]Error dropping temporary tables: {error.message}[/red]")
        cursor.close()

    elif choice == 2:
        # Union on Different Tables with Common Columns
        console.print("[bold cyan]Union on Different Tables with Common Columns[/bold cyan]")
        # Display tables and prompt user to select two
        table_menu = Panel(
            "\n".join([f"{i+1}. {tables[i]}" for i in range(len(tables))]),
            title="Select Two Different Tables for Union",
            subtitle="Enter the numbers of the tables separated by a comma (e.g., 1,2)",
            style="bold cyan",
            box=box.DOUBLE_EDGE
        )
        console.print(table_menu)
        try:
            choices = Prompt.ask("Your choices").split(',')
            if len(choices) != 2:
                raise ValueError
            table_name1 = tables[int(choices[0].strip())-1]
            table_name2 = tables[int(choices[1].strip())-1]
            if table_name1 == table_name2:
                console.print("[red]Please select two different tables for this option.[/red]")
                return
        except Exception:
            console.print("[red]Invalid input. Please enter two valid numbers separated by a comma.[/red]")
            return

        # Identify Common Columns
        cursor = connection.cursor()
        cursor.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{table_name1.upper()}'")
        columns1 = set([row[0] for row in cursor.fetchall()])
        cursor.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{table_name2.upper()}'")
        columns2 = set([row[0] for row in cursor.fetchall()])
        cursor.close()

        common_columns = columns1.intersection(columns2)
        non_common_columns1 = columns1 - common_columns
        non_common_columns2 = columns2 - common_columns

        if not common_columns:
            console.print("[red]No common columns found between the selected tables. Cannot perform union.[/red]")
            return

        # Inform user about non-common columns
        if non_common_columns1 or non_common_columns2:
            console.print("[yellow]Warning: The following columns are not common and will not be included in the union operation:[/yellow]")
            if non_common_columns1:
                console.print(f"[yellow]{table_name1} - {', '.join(non_common_columns1)}[/yellow]")
            if non_common_columns2:
                console.print(f"[yellow]{table_name2} - {', '.join(non_common_columns2)}[/yellow]")

        # Prompt user to confirm or adjust
        confirm = Prompt.ask("Do you want to proceed with the union on common columns? (yes/no)", default="yes")
        if confirm.lower() != 'yes':
            console.print("[red]Union operation cancelled.[/red]")
            return

        # Prepare columns for union
        common_columns_list = ', '.join(common_columns)

        # Perform Union
        union_query = f"SELECT {common_columns_list} FROM {table_name1} UNION SELECT {common_columns_list} FROM {table_name2}"
        console.print(f"[bold cyan]Executing Union on Common Columns: {table_name1} ∪ {table_name2}[/bold cyan]")
        execute_query(connection, union_query)

    elif choice == 3:
        # Back to RA Operations Menu
        return

    pause()


def difference(connection):
    """
    Implements the Difference operation.
    Finds rows in the first table that are not in the second table.
    Supports difference on the same table with row range selection or on different tables with common columns.
    """
    console.print("[bold underline]Difference Operation[/bold underline]")
    # Get list of user tables
    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM user_tables")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()

    if not tables:
        console.print("[red]No tables found in the database.[/red]")
        return

    # Display Difference Options Menu
    difference_options_menu = Panel(
        "\n".join([
            "1. Difference on the Same Table with Row Range Selection",
            "2. Difference on Different Tables with Common Columns",
            "3. Back to RA Operations Menu"
        ]),
        title="Difference Operation Options",
        subtitle="Choose an option [1-3]",
        style="bold cyan",
        box=box.DOUBLE_EDGE
    )
    console.print(difference_options_menu)
    try:
        choice = IntPrompt.ask("Your choice", choices=['1', '2', '3'])
    except Exception:
        console.print("[red]Invalid input. Please enter a valid number.[/red]")
        return

    if choice == 1:
        # Difference on the Same Table with Row Range Selection
        console.print("[bold cyan]Difference on the Same Table with Row Range Selection[/bold cyan]")
        # Display tables and prompt user to select one
        table_menu = Panel(
            "\n".join([f"{i+1}. {tables[i]}" for i in range(len(tables))]),
            title="Select a Table",
            subtitle="Enter the number of the table",
            style="bold cyan",
            box=box.DOUBLE_EDGE
        )
        console.print(table_menu)
        try:
            table_choice = IntPrompt.ask("Your choice", choices=[str(i+1) for i in range(len(tables))])
            table_name = tables[int(table_choice)-1]
        except Exception:
            console.print("[red]Invalid input. Please enter a valid number.[/red]")
            return

        # Prompt for row ranges
        console.print(f"Selected Table: {table_name}")
        try:
            range1 = Prompt.ask("Enter first row range for Table1 (e.g., 1-7)")
            range2 = Prompt.ask("Enter second row range for Table2 (e.g., 5-12)")
            start1, end1 = map(int, range1.split('-'))
            start2, end2 = map(int, range2.split('-'))
        except Exception:
            console.print("[red]Invalid row range format. Please enter in 'start-end' format (e.g., 1-7).[red]")
            return

        # Create Temporary Tables
        temp_table1 = f"temp_diff_{table_name}_1"
        temp_table2 = f"temp_diff_{table_name}_2"

        # Drop temp tables if they already exist in a single PL/SQL block
        drop_temp_tables_query = f"""
            BEGIN
                EXECUTE IMMEDIATE 'DROP TABLE {temp_table1}';
                EXECUTE IMMEDIATE 'DROP TABLE {temp_table2}';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -942 THEN
                        RAISE;
                    END IF;
            END;
        """
        try:
            cursor = connection.cursor()
            cursor.execute(drop_temp_tables_query)
            connection.commit()
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            console.print(f"[red]Error dropping temporary tables: {error.message}[/red]")
            cursor.close()
            return
        cursor.close()

        # Create Temp Table 1
        create_temp1_query = f"""
            CREATE TABLE {temp_table1} AS
            SELECT * FROM (
                SELECT a.*, ROW_NUMBER() OVER (ORDER BY ROWID) as rn
                FROM {table_name} a
            )
            WHERE rn BETWEEN {start1} AND {end1}
        """
        # Create Temp Table 2
        create_temp2_query = f"""
            CREATE TABLE {temp_table2} AS
            SELECT * FROM (
                SELECT a.*, ROW_NUMBER() OVER (ORDER BY ROWID) as rn
                FROM {table_name} a
            )
            WHERE rn BETWEEN {start2} AND {end2}
        """

        try:
            cursor = connection.cursor()
            cursor.execute(create_temp1_query)
            cursor.execute(create_temp2_query)
            connection.commit()
            console.print(f"[green]Temporary tables '{temp_table1}' and '{temp_table2}' created successfully.[/green]")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            console.print(f"[red]Error creating temporary tables: {error.message}[/red]")
            cursor.close()
            return
        cursor.close()

        # Perform Difference (Table1 - Table2)
        difference_query = f"SELECT * FROM {temp_table1} MINUS SELECT * FROM {temp_table2}"
        console.print(f"[bold cyan]Executing Difference: {temp_table1} − {temp_table2}[/bold cyan]")
        execute_query(connection, difference_query)

        # Optionally, drop temp tables after operation in a single PL/SQL block
        cleanup_temp_query = f"""
            BEGIN
                EXECUTE IMMEDIATE 'DROP TABLE {temp_table1}';
                EXECUTE IMMEDIATE 'DROP TABLE {temp_table2}';
            EXCEPTION
                WHEN OTHERS THEN
                    IF SQLCODE != -942 THEN
                        RAISE;
                    END IF;
            END;
        """
        try:
            cursor = connection.cursor()
            cursor.execute(cleanup_temp_query)
            connection.commit()
            console.print(f"[green]Temporary tables '{temp_table1}' and '{temp_table2}' dropped successfully.[/green]")
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            console.print(f"[red]Error dropping temporary tables: {error.message}[/red]")
        cursor.close()

    elif choice == 2:
        # Difference on Different Tables with Common Columns
        console.print("[bold cyan]Difference on Different Tables with Common Columns[/bold cyan]")
        # Display tables and prompt user to select two
        table_menu = Panel(
            "\n".join([f"{i+1}. {tables[i]}" for i in range(len(tables))]),
            title="Select Two Different Tables for Difference",
            subtitle="Enter the numbers of the tables separated by a comma (e.g., 1,2)",
            style="bold cyan",
            box=box.DOUBLE_EDGE
        )
        console.print(table_menu)
        try:
            choices = Prompt.ask("Your choices").split(',')
            if len(choices) != 2:
                raise ValueError
            table_name1 = tables[int(choices[0].strip())-1]
            table_name2 = tables[int(choices[1].strip())-1]
            if table_name1 == table_name2:
                console.print("[red]Please select two different tables for this option.[/red]")
                return
        except Exception:
            console.print("[red]Invalid input. Please enter two valid numbers separated by a comma.[/red]")
            return

        # Identify Common Columns
        cursor = connection.cursor()
        cursor.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{table_name1.upper()}'")
        columns1 = set([row[0] for row in cursor.fetchall()])
        cursor.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{table_name2.upper()}'")
        columns2 = set([row[0] for row in cursor.fetchall()])
        cursor.close()

        common_columns = columns1.intersection(columns2)
        non_common_columns1 = columns1 - common_columns
        non_common_columns2 = columns2 - common_columns

        if not common_columns:
            console.print("[red]No common columns found between the selected tables. Cannot perform difference.[/red]")
            return

        # Inform user about non-common columns
        if non_common_columns1 or non_common_columns2:
            console.print("[yellow]Warning: The following columns are not common and will not be included in the difference operation:[/yellow]")
            if non_common_columns1:
                console.print(f"[yellow]{table_name1} - {', '.join(non_common_columns1)}[/yellow]")
            if non_common_columns2:
                console.print(f"[yellow]{table_name2} - {', '.join(non_common_columns2)}[/yellow]")

        # Prompt user to confirm or adjust
        confirm = Prompt.ask("Do you want to proceed with the difference on common columns? (yes/no)", default="yes")
        if confirm.lower() != 'yes':
            console.print("[red]Difference operation cancelled.[/red]")
            return

        # Prepare columns for difference
        common_columns_list = ', '.join(common_columns)

        # Perform Difference (Table1 - Table2)
        difference_query = f"SELECT {common_columns_list} FROM {table_name1} MINUS SELECT {common_columns_list} FROM {table_name2}"
        console.print(f"[bold cyan]Executing Difference: {table_name1} − {table_name2}[/bold cyan]")
        execute_query(connection, difference_query)

    elif choice == 3:
        # Back to RA Operations Menu
        return

    pause()


def cartesian_product(connection):
    """
    Implements the Cartesian Product operation.
    Creates a Cartesian product of two tables.
    """
    console.print("[bold underline]Cartesian Product Operation[/bold underline]")
    # Get list of user tables
    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM user_tables")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()

    if len(tables) < 2:
        console.print("[red]At least two tables are required for cartesian product operation.[/red]")
        return

    # Display tables and prompt user to select two
    table_menu = Panel(
        "\n".join([f"{i+1}. {tables[i]}" for i in range(len(tables))]),
        title="Select Two Tables",
        subtitle="Enter the numbers of the tables separated by a comma (e.g., 1,2)",
        style="bold cyan",
        box=box.DOUBLE_EDGE
    )
    console.print(table_menu)
    try:
        choices = Prompt.ask("Your choices").split(',')
        if len(choices) != 2:
            raise ValueError
        table_name1 = tables[int(choices[0].strip())-1]
        table_name2 = tables[int(choices[1].strip())-1]
    except Exception:
        console.print("[red]Invalid input. Please enter two valid numbers separated by a comma.[/red]")
        return

    # Build and execute query
    query = f"SELECT * FROM {table_name1} CROSS JOIN {table_name2}"
    console.print(f"[bold cyan]Executing Cartesian Product: {table_name1} * {table_name2}[/bold cyan]")
    execute_query(connection, query)

    pause()


def natural_join(connection):
    """
    Implements the Natural Join (⨝) operation.
    Performs a natural join on two tables based on common columns.
    """
    console.print("[bold underline]Natural Join Operation[/bold underline]")
    # Get list of user tables
    cursor = connection.cursor()
    cursor.execute("SELECT table_name FROM user_tables")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()

    if len(tables) < 2:
        console.print("[red]At least two tables are required for natural join operation.[/red]")
        return

    # Display tables and prompt user to select two
    table_menu = Panel(
        "\n".join([f"{i+1}. {tables[i]}" for i in range(len(tables))]),
        title="Select Two Tables",
        subtitle="Enter the numbers of the tables separated by a comma (e.g., 1,2)",
        style="bold cyan",
        box=box.DOUBLE_EDGE
    )
    console.print(table_menu)
    try:
        choices = Prompt.ask("Your choices").split(',')
        if len(choices) != 2:
            raise ValueError
        table_name1 = tables[int(choices[0].strip())-1]
        table_name2 = tables[int(choices[1].strip())-1]
    except Exception:
        console.print("[red]Invalid input. Please enter two valid numbers separated by a comma.[/red]")
        return

    # Find common columns
    cursor = connection.cursor()
    cursor.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{table_name1.upper()}'")
    columns1 = set([row[0] for row in cursor.fetchall()])
    cursor.execute(f"SELECT column_name FROM user_tab_columns WHERE table_name = '{table_name2.upper()}'")
    columns2 = set([row[0] for row in cursor.fetchall()])
    cursor.close()

    common_columns = columns1.intersection(columns2)
    if not common_columns:
        console.print("[red]No common columns found for natural join.[/red]")
        return

    # Build and execute query
    query = f"SELECT * FROM {table_name1} NATURAL JOIN {table_name2}"
    console.print(f"[bold cyan]Executing Natural Join: {table_name1} ⨝ {table_name2}[/bold cyan]")
    execute_query(connection, query)

    pause()


def ra_operations(connection):
    """
    Displays the RA operations menu and handles user input.
    """
    while True:
        ra_menu = Panel(
            "\n".join([
                "Relational Algebra Operations",
                "----------------------------------------",
                "1. Selection",
                "2. Projection",
                "3. Union",
                "4. Difference",
                "5. Cartesian Product",
                "6. Natural Join",
                "7. Back to Main Menu",
                "----------------------------------------"
            ]),
            title="RA Operations Menu",
            subtitle="Choose an option [1-7]",
            style="bold cyan",
            box=box.DOUBLE_EDGE
        )
        console.print(ra_menu)
        try:
            choice = IntPrompt.ask("Your choice", default=7)
        except Exception:
            console.print("[red]Invalid input. Please enter a number between 1 and 7.[/red]")
            continue

        console.print("\n")
        if choice == 1:
            selection(connection)
        elif choice == 2:
            projection(connection)
        elif choice == 3:
            union(connection)
        elif choice == 4:
            difference(connection)
        elif choice == 5:
            cartesian_product(connection)
        elif choice == 6:
            natural_join(connection)
        elif choice == 7:
            break
        else:
            console.print("[red]Invalid option. Please try again.[/red]")

        pause()


def pause():
    """
    Pauses the program until the user presses Enter.
    """
    console.print("\nPress [bold cyan]Enter[/bold cyan] to continue...")
    input()