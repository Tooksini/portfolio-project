def fetch_all_projects(conn):
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM projects")
    projects = cursor.fetchall()
    cursor.close()
    return projects
