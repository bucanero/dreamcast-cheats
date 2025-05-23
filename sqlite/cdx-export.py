import sqlite3
import os

def export_rows_to_text_files(db_file, table_name, output_dir='output'):
    """
    Export each row from a SQLite table to individual text files.
    
    Args:
        db_file (str): Path to the SQLite database file
        table_name (str): Name of the table to export
        output_dir (str): Directory to save the text files (default: 'output')
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get table information
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [column[1] for column in cursor.fetchall()]
        
        # Get all rows from the table
        cursor.execute(f"SELECT id_game, name, region, description, LTRIM(code) FROM dc_games, dc_codes WHERE dc_games.id = dc_codes.id_game ORDER by name")
        rows = cursor.fetchall()
        
        mdi = open(os.path.join(output_dir, 'README.md'), 'w', encoding='utf-8')
        idx = 0
        
        # Export each row to a separate file
        for i, row in enumerate(rows, start=1):
            if idx != row[0]:
                idx = row[0]
                gname = row[1] + " (" + row[2] + ")"
                fname = gname.lower().replace(" ", "-").replace("/", "-").replace("*", "").replace(":", "").replace("?", "")
                filename = os.path.join(output_dir, f"{fname}.md")
                mdi.write(f"- [{gname}]({fname}.md)\r\n")
                f = open(filename, 'w', encoding='utf-8')
                f.write(f"# {gname}\r\n\r\n## Cheat Codes\r\n\r\n")

            f.write(f"## {row[3]}\r\n\r\n```\r\n{row[4]}\r\n```\r\n\r\n")
        
            print(f"Exported row {i} to {filename}")
        
        print(f"\nSuccessfully exported {len(rows)} rows from table '{table_name}'")
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Example usage
    database_file = "cdx.sqlite"    # Change to your database file
    table_to_export = "dc_games"    # Change to your table name
    
    export_rows_to_text_files(database_file, table_to_export)
