
class Validation:
    def __init__(self):
        pass

    async def isSQLInjectionContent(self,data):
        # Common SQL injection patterns
        sql_injection_patterns = ["drop table", "delete from", "update", "insert into", "select * from","DROP TABLE", "DELETE FROM", "UPDATE", "INSERT INTO", "SELECT * FROM", "--", "//", "||", ":", ";"]

        lower_data = data.lower()

        for pattern in sql_injection_patterns:
            if pattern.lower() in lower_data:
                return True
        return False
